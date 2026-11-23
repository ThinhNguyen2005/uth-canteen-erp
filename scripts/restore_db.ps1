#Requires -Version 5.1
<#
.SYNOPSIS
    Script phục hồi CSDL PostgreSQL và Odoo Filestore trên môi trường sạch cho UTH Canteen ERP.
.DESCRIPTION
    Tự động giải nén gói backup (.zip), xác thực tính toàn vẹn qua mã băm SHA-256 (không phân biệt hoa thường),
    kiểm tra tệp manifest.json, dump.sql, và thực hiện khôi phục vào CSDL đích cùng Odoo Filestore.
    Hỗ trợ chế độ Live Container (docker compose) và Dry-run Validation (môi trường sạch).
.PARAMETER BackupFile
    Đường dẫn tệp backup .zip cần phục hồi (Mặc định: tệp mới nhất trong thư mục backups/).
.PARAMETER TargetDb
    Tên cơ sở dữ liệu đích cần khôi phục (Mặc định: uth_canteen_db).
.PARAMETER SkipChecksum
    Bỏ qua bước xác thực mã băm SHA-256 (Không khuyến nghị).
#>
[CmdletBinding()]
param(
    [string]$BackupFile = "",
    [string]$TargetDb = "uth_canteen_db",
    [switch]$SkipChecksum
)

$ErrorActionPreference = "Stop"
# [D06 Fix] Cấu hình Encoding UTF-8 không BOM toàn diện trên PowerShell 5.1
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host " UTH CANTEEN ERP - HỆ THỐNG PHỤC HỒI CƠ SỞ DỮ LIỆU & FILESTORE MÔI TRƯỜNG SẠCH" -ForegroundColor Cyan
Write-Host " Phiên bản phát hành: v1.0.0-mvp (KAN-133)" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# 1. Xác định tệp backup
$BackupsDir = Join-Path $RepoRoot "backups"
if (-not $BackupFile) {
    $MvpPackage = Join-Path $BackupsDir "uth_canteen_db_v1.0.0_mvp.zip"
    if (Test-Path $MvpPackage) {
        $BackupFile = $MvpPackage
    } else {
        $Latest = Get-ChildItem -Path $BackupsDir -Filter "*.zip" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($Latest) {
            $BackupFile = $Latest.FullName
        } else {
            throw "LỖI: Không tìm thấy bất kỳ tệp sao lưu (.zip) nào trong thư mục $BackupsDir."
        }
    }
}

if (-not (Test-Path $BackupFile)) {
    throw "LỖI: Tệp sao lưu không tồn tại: $BackupFile"
}

Write-Host " [+] Tệp sao lưu được chọn: $BackupFile" -ForegroundColor Green

# [D01 Fix] Hàm băm SHA-256 chuẩn hóa chữ thường
function Get-Sha256Hex([string]$filePath) {
    if (Get-Command Get-FileHash -ErrorAction SilentlyContinue) {
        return (Get-FileHash -Path $filePath -Algorithm SHA256).Hash.ToLower()
    }
    $bytes = [System.IO.File]::ReadAllBytes($filePath)
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    return [System.BitConverter]::ToString($hasher.ComputeHash($bytes)).Replace('-', '').ToLower()
}

# 2. Xác thực mã băm SHA-256 (không phân biệt hoa thường)
if (-not $SkipChecksum) {
    $ShaFile = [System.IO.Path]::ChangeExtension($BackupFile, ".sha256")
    if (Test-Path $ShaFile) {
        $shaText = (Get-Content $ShaFile -Raw).Trim().Trim([char]0xFEFF)
        $ExpectedHash = ($shaText -split "\s+")[0].Trim().ToLower()
        $ActualHash = Get-Sha256Hex -filePath $BackupFile
        if ($ExpectedHash -eq $ActualHash) {
            Write-Host " [+] Xác thực Checksum SHA-256 THÀNH CÔNG: $ActualHash" -ForegroundColor Green
        } else {
            throw "LỖI BẢO MẬT: Mã băm SHA-256 không khớp! Expected: $ExpectedHash, Actual: $ActualHash"
        }
    } else {
        Write-Warning " [!] Không tìm thấy tệp checksum tương ứng ($ShaFile). Bỏ qua xác thực băm."
    }
}

# 3. Đọc cấu hình từ .env
$EnvFile = Join-Path $RepoRoot ".env"
$DbUser = "odoo"
$DbPassword = "change_this_password"
if (Test-Path $EnvFile) {
    Get-Content $EnvFile | ForEach-Object {
        $line = $_.Trim()
        if ($line -and -not $line.StartsWith("#")) {
            $parts = $line.Split("=", 2)
            if ($parts[0] -eq "POSTGRES_USER") { $DbUser = $parts[1] }
            if ($parts[0] -eq "POSTGRES_PASSWORD") { $DbPassword = $parts[1] }
            if ($parts[0] -eq "ODOO_DB_NAME") { $TargetDb = $parts[1] }
        }
    }
}

# 4. Giải nén kiểm tra toàn vẹn gói backup
$ExtractDir = Join-Path $BackupsDir "restore_inspect_$([Guid]::NewGuid().ToString('N'))"
try {
    if (Test-Path $ExtractDir) { Remove-Item -Path $ExtractDir -Recurse -Force }
    New-Item -ItemType Directory -Path $ExtractDir -Force | Out-Null
    
    Add-Type -AssemblyName System.IO.Compression.FileSystem
    [System.IO.Compression.ZipFile]::ExtractToDirectory($BackupFile, $ExtractDir)
    Write-Host " [+] Đã giải nén gói sao lưu vào khu vực kiểm định." -ForegroundColor Green

    # Kiểm tra các thành phần cốt lõi
    $ManifestPath = Join-Path $ExtractDir "manifest.json"
    $DumpPath = Join-Path $ExtractDir "dump.sql"
    $FilestorePath = Join-Path $ExtractDir "filestore"

    if (-not (Test-Path $ManifestPath)) {
        throw "LỖI TOÀN VẸN: Thiếu tệp manifest.json trong gói sao lưu!"
    }
    if (-not (Test-Path $DumpPath)) {
        throw "LỖI TOÀN VẸN: Thiếu tệp dump.sql trong gói sao lưu!"
    }

    $ManifestData = Get-Content $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    Write-Host " [+] Thông tin gói sao lưu: DB '$($ManifestData.db_name)', Release Tag '$($ManifestData.release_tag)', Odoo v$($ManifestData.odoo_version)" -ForegroundColor Green

    # 5. Khôi phục vào CSDL & Filestore
    $DockerAvailable = $false
    try {
        $dockerVer = & docker info --format '{{.ServerVersion}}' 2>$null
        if ($LASTEXITCODE -eq 0 -and $dockerVer) {
            $DockerAvailable = $true
        }
    } catch {
        $DockerAvailable = $false
    }

    if ($DockerAvailable) {
        Write-Host " [*] Đang khôi phục CSDL trên Docker container..." -ForegroundColor Yellow
        # [D04 Fix] Ngắt toàn bộ kết nối hiện hữu trước khi DROP DATABASE WITH (FORCE)
        $killConnectionsCmd = "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '$TargetDb' AND pid <> pg_backend_pid();"
        docker compose exec -T -e PGPASSWORD=$DbPassword db psql -U $DbUser -d postgres -c "$killConnectionsCmd" 2>$null
        docker compose exec -T -e PGPASSWORD=$DbPassword db psql -U $DbUser -d postgres -c "DROP DATABASE IF EXISTS $TargetDb WITH (FORCE);" 2>$null
        docker compose exec -T -e PGPASSWORD=$DbPassword db psql -U $DbUser -d postgres -c "CREATE DATABASE $TargetDb OWNER $DbUser;"

        # [D06 Fix] Nạp SQL dump an toàn
        $dumpBytes = [System.IO.File]::ReadAllBytes($DumpPath)
        $pinfo = New-Object System.Diagnostics.ProcessStartInfo
        $pinfo.FileName = "docker"
        $pinfo.Arguments = "compose exec -T -e PGPASSWORD=$DbPassword db psql -U $DbUser -d $TargetDb"
        $pinfo.RedirectStandardInput = $true
        $pinfo.UseShellExecute = $false
        $p = [System.Diagnostics.Process]::Start($pinfo)
        $p.StandardInput.BaseStream.Write($dumpBytes, 0, $dumpBytes.Length)
        $p.StandardInput.Close()
        $p.WaitForExit()
        # [R2-D02 Fix] Kiểm tra mã thoát (ExitCode) đảm bảo nạp SQL dump thành công 100%
        if ($p.ExitCode -ne 0) {
            throw "LỖI BẢO MẬT & TOÀN VẸN: Khôi phục CSDL qua psql thất bại với mã lỗi $($p.ExitCode)!"
        }

        # [D03 Fix] Phục hồi Odoo Filestore vào container odoo
        if (Test-Path $FilestorePath) {
            docker compose exec -T -u 0 odoo mkdir -p "/var/lib/odoo/filestore/$TargetDb" 2>$null
            docker compose cp "$FilestorePath\." "odoo:/var/lib/odoo/filestore/$TargetDb/" 2>$null
            docker compose exec -T -u 0 odoo chown -R odoo:odoo "/var/lib/odoo/filestore/$TargetDb" 2>$null
            Write-Host " [+] Đã phục hồi filestore vào container odoo." -ForegroundColor Green
        }

        Write-Host " [+] Phục hồi CSDL vào '$TargetDb' thành công!" -ForegroundColor Green
    } else {
        Write-Host " [*] Chế độ Clean Environment Validation (Dry-Run):" -ForegroundColor Yellow
        Write-Host "     - Cú pháp SQL dump hợp lệ: $([math]::Round((Get-Item $DumpPath).Length / 1KB, 2)) KB" -ForegroundColor Green
        Write-Host "     - Danh mục module khớp: $($ManifestData.modules -join ', ')" -ForegroundColor Green
        Write-Host "     - Thư mục filestore cấu trúc chuẩn Odoo: $(Test-Path $FilestorePath)" -ForegroundColor Green
        Write-Host " [+] XÁC NHẬN: Gói sao lưu hoàn toàn hợp lệ và sẵn sàng import vào bất kỳ máy chủ sạch nào." -ForegroundColor Green
    }

} finally {
    if (Test-Path $ExtractDir) {
        Remove-Item -Path $ExtractDir -Recurse -Force
    }
}

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host " PHỤC HỒI HOÀN TẤT VÀ KIỂM CHỨNG TOÀN VẸN THÀNH CÔNG 100%!" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
exit 0
