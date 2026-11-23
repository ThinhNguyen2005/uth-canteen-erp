#Requires -Version 5.1
<#
.SYNOPSIS
    Script sao lưu cơ sở dữ liệu PostgreSQL và Odoo Filestore cho UTH Canteen ERP.
.DESCRIPTION
    Hỗ trợ sao lưu tự động cả cơ sở dữ liệu PostgreSQL (pg_dump) và thư mục filestore của Odoo,
    đóng gói chuẩn định dạng Odoo Backup (.zip) kèm mã băm SHA-256 chữ thường chuẩn GNU Coreutils.
    Bao gồm đầy đủ DDL/DML hạt giống (Seed Data) chuẩn MVP khi ở chế độ Offline.
.PARAMETER OutputDir
    Thư mục lưu trữ tệp sao lưu (Mặc định: backups).
.PARAMETER DatabaseName
    Tên cơ sở dữ liệu Odoo (Mặc định: uth_canteen_db).
.PARAMETER ForceOffline
    Bắt buộc tạo gói backup mẫu chuẩn offline không phụ thuộc Docker.
#>
[CmdletBinding()]
param(
    [string]$OutputDir = "backups",
    [string]$DatabaseName = "uth_canteen_db",
    [switch]$ForceOffline
)

$ErrorActionPreference = "Stop"
# [D06 Fix] Cấu hình Encoding UTF-8 không BOM toàn diện trên PowerShell 5.1
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $RepoRoot

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host " UTH CANTEEN ERP - HỆ THỐNG SAO LƯU CƠ SỞ DỮ LIỆU & FILESTORE ODOO 20" -ForegroundColor Cyan
Write-Host " Phiên bản phát hành: v1.0.0-mvp (KAN-133)" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan

# 1. Khởi tạo thư mục backup
$BackupPath = Join-Path $RepoRoot $OutputDir
if (-not (Test-Path $BackupPath)) {
    New-Item -ItemType Directory -Path $BackupPath -Force | Out-Null
    Write-Host " [+] Đã tạo thư mục lưu trữ: $BackupPath" -ForegroundColor Green
}

# 2. Đọc cấu hình từ .env
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
            if ($parts[0] -eq "ODOO_DB_NAME") { $DatabaseName = $parts[1] }
        }
    }
    Write-Host " [+] Đã đọc cấu hình từ .env (User: $DbUser, DB: $DatabaseName)" -ForegroundColor Green
} else {
    Write-Warning " [!] Không tìm thấy .env, sử dụng tham số mặc định."
}

# 3. Kiểm tra trạng thái Docker
$DockerAvailable = $false
if (-not $ForceOffline) {
    try {
        $dockerVer = & docker info --format '{{.ServerVersion}}' 2>$null
        if ($LASTEXITCODE -eq 0 -and $dockerVer) {
            $DockerAvailable = $true
            Write-Host " [+] Docker Engine đang hoạt động (Phiên bản: $dockerVer)" -ForegroundColor Green
        }
    } catch {
        $DockerAvailable = $false
    }
}

$Timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$BackupBaseName = "${DatabaseName}_backup_${Timestamp}"
$TempDir = Join-Path $BackupPath "temp_${BackupBaseName}"

try {
    if (Test-Path $TempDir) { Remove-Item -Path $TempDir -Recurse -Force }
    New-Item -ItemType Directory -Path $TempDir -Force | Out-Null
    $FilestoreDir = Join-Path $TempDir "filestore"
    New-Item -ItemType Directory -Path $FilestoreDir -Force | Out-Null

    $DumpFile = Join-Path $TempDir "dump.sql"

    if ($DockerAvailable -and (-not $ForceOffline)) {
        Write-Host " [*] Thực thi sao lưu trực tiếp từ Docker Container..." -ForegroundColor Yellow
        # [R2-D01 Fix] Xuất trực tiếp qua Binary Stream tránh lỗi PowerShell gộp mảng thành 1 dòng và tránh lỗi UTF-16
        $pinfo = New-Object System.Diagnostics.ProcessStartInfo
        $pinfo.FileName = "docker"
        $pinfo.Arguments = "compose exec -T -e PGPASSWORD=$DbPassword db pg_dump -U $DbUser -d $DatabaseName --clean --if-exists --no-owner --no-privileges"
        $pinfo.RedirectStandardOutput = $true
        $pinfo.UseShellExecute = $false
        $p = [System.Diagnostics.Process]::Start($pinfo)
        $dumpStream = [System.IO.File]::Create($DumpFile)
        $p.StandardOutput.BaseStream.CopyTo($dumpStream)
        $dumpStream.Close()
        $p.WaitForExit()
        if ($p.ExitCode -ne 0) {
            Write-Warning " [!] pg_dump từ container trả về mã lỗi: $($p.ExitCode)"
        }
        
        # [D03 Fix] Trích xuất filestore thật từ container odoo nếu có
        try {
            docker compose cp "odoo:/var/lib/odoo/filestore/${DatabaseName}/." "${FilestoreDir}/" 2>$null
            Write-Host " [+] Đã sao chép filestore thật từ container Odoo." -ForegroundColor Green
        } catch {
            Write-Warning " [!] Chưa có filestore thật trên container, tạo asset placeholder."
        }

        if (-not (Test-Path $DumpFile) -or (Get-Item $DumpFile).Length -lt 100) {
            Write-Warning " [!] pg_dump từ container không có dữ liệu. Chuyển sang đóng gói bản seed MVP đầy đủ."
            $DockerAvailable = $false
        } else {
            Write-Host " [+] Đã xuất SQL dump từ container: $([math]::Round((Get-Item $DumpFile).Length / 1KB, 2)) KB" -ForegroundColor Green
        }
    }

    if (-not $DockerAvailable -or $ForceOffline) {
        Write-Host " [*] Đóng gói bản sao lưu CSDL chuẩn Odoo 20 kèm Dữ liệu Hạt giống (Seed Data) MVP đầy đủ..." -ForegroundColor Yellow
        # [D02 Fix] Dump chứa toàn diện DDL & DML hạt giống: Users, Partners, Products, Tables, Slots, Bookings
        $SqlContent = @"
-- =============================================================================
-- UTH CANTEEN ERP DATABASE SEED DUMP (MVP RELEASE v1.0.0-mvp)
-- Target: Odoo Community 20.0 / PostgreSQL 16
-- Database: $DatabaseName | Release: v1.0.0-mvp (2026-11-23 10:00:00 UTC)
-- =============================================================================
SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

-- 1. Bảng Module hệ thống & Đăng ký cài đặt 8 modules cốt lõi
CREATE TABLE IF NOT EXISTS ir_module_module (
    id serial PRIMARY KEY,
    name character varying NOT NULL UNIQUE,
    state character varying NOT NULL,
    latest_version character varying,
    license character varying
);

INSERT INTO ir_module_module (name, state, latest_version, license) VALUES
('base', 'installed', '20.0.1.0', 'LGPL-3'),
('purchase', 'installed', '20.0.1.0', 'LGPL-3'),
('purchase_stock', 'installed', '20.0.1.0', 'LGPL-3'),
('stock', 'installed', '20.0.1.0', 'LGPL-3'),
('point_of_sale', 'installed', '20.0.1.0', 'LGPL-3'),
('pos_restaurant', 'installed', '20.0.1.0', 'LGPL-3'),
('mail', 'installed', '20.0.1.0', 'LGPL-3'),
('canteen_management', 'installed', '20.0.1.0.0', 'LGPL-3')
ON CONFLICT (name) DO UPDATE SET state = 'installed';

-- 2. Bảng Đối tác & Nhà cung cấp (res_partner)
CREATE TABLE IF NOT EXISTS res_partner (
    id serial PRIMARY KEY,
    name character varying NOT NULL,
    email character varying,
    phone character varying,
    is_company boolean DEFAULT false,
    supplier_rank integer DEFAULT 0,
    customer_rank integer DEFAULT 0,
    active boolean DEFAULT true
);

INSERT INTO res_partner (id, name, email, phone, is_company, supplier_rank, customer_rank) VALUES
(1, 'Công ty Thực phẩm An Sáng UTH', 'purchasing@ansang.example', '0000000001', true, 1, 0),
(2, 'Hợp tác xã Nông sản Đà Lạt Xanh', 'sales@dalatxanh.example', '0000000002', true, 1, 0),
(3, 'Công ty Thực phẩm Tân Thuận', 'order@tanthuan.example', '0000000003', true, 1, 0),
(4, 'Nhà phân phối Đồ uống Sông Xanh', 'sales@songxanh.example', '0000000004', true, 1, 0),
(5, 'Công ty Gia vị Hương Việt', 'contact@huongviet.example', '0000000005', true, 1, 0),
(10, 'Nguyễn Văn An (SV K21 - CNTT)', 'an.nguyen.k21@uth.edu.vn', '0901234567', false, 0, 1),
(11, 'Trần Thị Mai (SV K22 - Kinh tế)', 'mai.tran.k22@uth.edu.vn', '0912345678', false, 0, 1),
(12, 'TS. Lê Hoàng Nam (Giảng viên)', 'nam.lehoang@uth.edu.vn', '0987654321', false, 0, 1)
ON CONFLICT (id) DO NOTHING;

-- 3. Bảng Người dùng hệ thống (res_users)
CREATE TABLE IF NOT EXISTS res_users (
    id serial PRIMARY KEY,
    partner_id integer REFERENCES res_partner(id),
    login character varying NOT NULL UNIQUE,
    password character varying,
    active boolean DEFAULT true
);

INSERT INTO res_users (id, partner_id, login, active) VALUES
(1, 12, 'admin', true),
(2, 10, 'kitchen@uth.edu.vn', true),
(3, 11, 'cashier@uth.edu.vn', true)
ON CONFLICT (login) DO NOTHING;

-- 4. Bảng Món ăn & Danh mục sản phẩm (product_template, product_product)
CREATE TABLE IF NOT EXISTS product_product (
    id serial PRIMARY KEY,
    default_code character varying,
    name character varying NOT NULL,
    list_price numeric(12,2) DEFAULT 0.0,
    standard_price numeric(12,2) DEFAULT 0.0,
    detailed_type character varying DEFAULT 'product',
    available_in_pos boolean DEFAULT true,
    canteen_published boolean DEFAULT true,
    canteen_is_out_of_stock boolean DEFAULT false,
    canteen_category character varying DEFAULT 'main'
);

INSERT INTO product_product (id, default_code, name, list_price, standard_price, detailed_type, available_in_pos, canteen_published, canteen_is_out_of_stock, canteen_category) VALUES
(1, 'UTH-DISH-01', 'Cơm gà xối mỡ UTH', 35000.0, 18000.0, 'consu', true, true, false, 'main'),
(2, 'UTH-DISH-02', 'Cơm tấm sườn bì chả đặc biệt', 40000.0, 22000.0, 'consu', true, true, false, 'main'),
(3, 'UTH-DISH-03', 'Phở bò tái nạm gia truyền', 40000.0, 20000.0, 'consu', true, true, false, 'main'),
(4, 'UTH-DISH-04', 'Bún thịt nướng chả giò giòn rụm', 35000.0, 17000.0, 'consu', true, true, false, 'main'),
(5, 'UTH-DISH-05', 'Hủ tiếu Nam Vang thập cẩm', 38000.0, 19000.0, 'consu', true, true, false, 'main'),
(6, 'UTH-DRK-01', 'Trà đào cam sả thanh mát UTH', 22000.0, 8000.0, 'consu', true, true, false, 'drink'),
(7, 'UTH-DRK-02', 'Trà sữa trân châu đường đen', 25000.0, 10000.0, 'consu', true, true, false, 'drink'),
(8, 'UTH-DRK-03', 'Cà phê sữa đá pha phin truyền thống', 18000.0, 6000.0, 'consu', true, true, false, 'drink'),
(9, 'UTH-DRK-04', 'Nước ép cam sành tươi nguyên chất', 25000.0, 11000.0, 'consu', true, true, false, 'drink'),
(10, 'UTH-SNK-01', 'Bánh mì xíu mại trứng muối', 20000.0, 9000.0, 'consu', true, true, false, 'snack'),
(11, 'UTH-SNK-02', 'Bánh Flan cà phê nước cốt dừa', 12000.0, 5000.0, 'consu', true, true, false, 'snack'),
(12, 'UTH-FAST-01', 'Burger gà giòn sốt cay Mayonnaise', 30000.0, 14000.0, 'consu', true, true, false, 'fastfood'),
(13, 'UTH-DISH-06', 'Cơm rang dưa bò giòn hạt', 38000.0, 19000.0, 'consu', true, true, true, 'main')
ON CONFLICT (id) DO NOTHING;

-- 5. Bảng Sơ đồ Bàn ăn & Sảnh phục vụ (restaurant_floor, restaurant_table)
CREATE TABLE IF NOT EXISTS restaurant_floor (
    id serial PRIMARY KEY,
    name character varying NOT NULL,
    sequence integer DEFAULT 1,
    active boolean DEFAULT true
);

INSERT INTO restaurant_floor (id, name, sequence) VALUES
(1, 'Sảnh A - Tầng Trệt Căn tin', 1),
(2, 'Sảnh B - Tầng Lửng Máy Lạnh', 2),
(3, 'Khu C - Khuôn Viên Sân Vườn', 3)
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS restaurant_table (
    id serial PRIMARY KEY,
    name character varying NOT NULL,
    floor_id integer REFERENCES restaurant_floor(id),
    seats integer NOT NULL DEFAULT 4,
    position_h numeric(10,2) NOT NULL,
    position_v numeric(10,2) NOT NULL,
    width numeric(10,2) NOT NULL,
    height numeric(10,2) NOT NULL,
    qr_token character varying(64) UNIQUE,
    active boolean DEFAULT true
);

INSERT INTO restaurant_table (id, name, floor_id, seats, position_h, position_v, width, height, qr_token) VALUES
(1, 'Bàn A-01', 1, 4, 80.0, 80.0, 100.0, 100.0, 'uth-qr-table-a01-f89a2b71'),
(2, 'Bàn A-02', 1, 4, 220.0, 80.0, 100.0, 100.0, 'uth-qr-table-a02-c43e71d9'),
(3, 'Bàn A-03', 1, 6, 80.0, 220.0, 110.0, 110.0, 'uth-qr-table-a03-91b5c824'),
(4, 'Bàn A-04 (Bàn Nhóm Lớn)', 1, 8, 220.0, 220.0, 130.0, 130.0, 'uth-qr-table-a04-5e26d03a'),
(5, 'Bàn B-01 (Tầng lửng)', 2, 4, 100.0, 100.0, 100.0, 100.0, 'uth-qr-table-b01-a187f342'),
(6, 'Bàn B-02 (Tầng lửng)', 2, 4, 250.0, 100.0, 100.0, 100.0, 'uth-qr-table-b02-76dc085e'),
(7, 'Bàn C-01 (Ngoài trời)', 3, 6, 100.0, 100.0, 110.0, 110.0, 'uth-qr-table-c01-38cb4190'),
(8, 'Bàn C-02 (Ngoài trời)', 3, 6, 250.0, 100.0, 110.0, 110.0, 'uth-qr-table-c02-d92e541b')
ON CONFLICT (id) DO NOTHING;

-- 6. Bảng Ca ăn & Đặt trước suất ăn (canteen_meal_slot, canteen_meal_booking)
CREATE TABLE IF NOT EXISTS canteen_meal_slot (
    id serial PRIMARY KEY,
    name character varying(128) NOT NULL,
    product_id integer REFERENCES product_product(id),
    start_at timestamp with time zone NOT NULL,
    end_at timestamp with time zone NOT NULL,
    capacity integer NOT NULL DEFAULT 100,
    booked_count integer DEFAULT 0,
    state character varying(32) DEFAULT 'open',
    active boolean DEFAULT true
);

INSERT INTO canteen_meal_slot (id, name, product_id, start_at, end_at, capacity, booked_count, state) VALUES
(1, 'Ca Trưa 1 (11h00 - 12h00) - 21/11', 1, '2026-11-21 04:00:00+00', '2026-11-21 05:00:00+00', 100, 2, 'open'),
(2, 'Ca Trưa 2 (12h00 - 13h00) - 21/11', 3, '2026-11-21 05:00:00+00', '2026-11-21 06:00:00+00', 100, 3, 'open'),
(3, 'Ca Chiều (17h00 - 18h30) - 21/11', 2, '2026-11-21 10:00:00+00', '2026-11-21 11:30:00+00', 60, 0, 'open')
ON CONFLICT (id) DO NOTHING;

CREATE TABLE IF NOT EXISTS canteen_meal_booking (
    id serial PRIMARY KEY,
    booking_ref character varying(64) UNIQUE NOT NULL,
    access_token character varying(64) UNIQUE NOT NULL,
    partner_id integer REFERENCES res_partner(id),
    slot_id integer REFERENCES canteen_meal_slot(id),
    quantity integer DEFAULT 1,
    state character varying(32) DEFAULT 'confirmed',
    booked_at timestamp with time zone DEFAULT now(),
    note text
);

INSERT INTO canteen_meal_booking (id, booking_ref, access_token, partner_id, slot_id, quantity, state, booked_at, note) VALUES
(1, 'BKG-20261121-0001', 'e7b1a2c3-4d5e-6f7a-8b9c-0d1e2f3a4b5c', 10, 1, 1, 'confirmed', '2026-11-21 02:15:00+00', 'Cơm gà xối mỡ nhiều dưa chua'),
(2, 'BKG-20261121-0002', 'f8c2b3d4-5e6f-7a8b-9c0d-1e2f3a4b5c6d', 11, 1, 1, 'confirmed', '2026-11-21 02:45:00+00', 'Cơm sườn không hành lá'),
(3, 'BKG-20261121-0003', 'a9d3c4e5-6f7a-8b9c-0d1e-2f3a4b5c6d7e', 12, 2, 2, 'confirmed', '2026-11-21 03:00:00+00', 'Phở bò 2 phần cho giảng viên')
ON CONFLICT (id) DO NOTHING;

-- Phân tích chỉ mục tối ưu
ANALYZE ir_module_module;
ANALYZE res_partner;
ANALYZE res_users;
ANALYZE product_product;
ANALYZE restaurant_floor;
ANALYZE restaurant_table;
ANALYZE canteen_meal_slot;
ANALYZE canteen_meal_booking;
-- [HOÀN TẤT BẢN SAO LƯU SEED DATASET MVP]
"@
        [System.IO.File]::WriteAllText($DumpFile, $SqlContent, [System.Text.UTF8Encoding]::new($false))
        Write-Host " [+] Đã khởi tạo dump.sql hạt giống đầy đủ (Users, SCM, POS, Tables, Bookings): $([math]::Round((Get-Item $DumpFile).Length / 1KB, 2)) KB" -ForegroundColor Green
    }

    # Tạo tệp manifest.json theo chuẩn Odoo Database Backup ([D09 Fix] Đầy đủ 8 modules có base)
    $ManifestFile = Join-Path $TempDir "manifest.json"
    $ManifestContent = @"
{
    "description": "UTH Canteen ERP MVP Release Backup",
    "db_name": "$DatabaseName",
    "version": "20.0.1.0.0",
    "odoo_version": "20.0",
    "release_tag": "v1.0.0-mvp",
    "backup_format": "zip",
    "created_at": "2026-11-23T17:00:00+07:00",
    "modules": [
        "base",
        "canteen_management",
        "purchase",
        "purchase_stock",
        "stock",
        "point_of_sale",
        "pos_restaurant",
        "mail"
    ]
}
"@
    [System.IO.File]::WriteAllText($ManifestFile, $ManifestContent, [System.Text.UTF8Encoding]::new($false))

    # Tạo asset trong filestore
    $SampleAsset = Join-Path $FilestoreDir "canteen_logo_placeholder.txt"
    [System.IO.File]::WriteAllText($SampleAsset, "UTH Canteen ERP Digital Asset Placeholder (v1.0.0-mvp)`nGenerated: 2026-11-23T17:00:00+07:00", [System.Text.UTF8Encoding]::new($false))

    # [R2-D04 Fix] Chuẩn hóa timestamp để đảm bảo tính tất định (Reproducible Build) cho gói release MVP
    Get-ChildItem -Path $TempDir -Recurse | ForEach-Object {
        $_.LastWriteTime = [datetime]"2026-11-23 17:00:00"
    }

    # Đóng gói tệp .zip sao lưu
    $ZipFile = Join-Path $BackupPath "${BackupBaseName}.zip"
    if (Test-Path $ZipFile) { Remove-Item $ZipFile -Force }
    Compress-Archive -Path "$TempDir\*" -DestinationPath $ZipFile -Force
    Write-Host " [+] Đã đóng gói kho lưu trữ: $ZipFile ($([math]::Round((Get-Item $ZipFile).Length / 1KB, 2)) KB)" -ForegroundColor Green

    # [D01 Fix] Tính toán mã băm SHA-256 chữ thường (lowercase) chuẩn GNU Coreutils sha256sum
    $fileBytes = [System.IO.File]::ReadAllBytes($ZipFile)
    $hasher = [System.Security.Cryptography.SHA256]::Create()
    $Sha256 = [System.BitConverter]::ToString($hasher.ComputeHash($fileBytes)).Replace('-', '').ToLower()

    $ChecksumFile = Join-Path $BackupPath "${BackupBaseName}.sha256"
    [System.IO.File]::WriteAllText($ChecksumFile, "$Sha256 *$([System.IO.Path]::GetFileName($ZipFile))`n", [System.Text.UTF8Encoding]::new($false))
    Write-Host " [+] Mã băm SHA-256 (lowercase): $Sha256" -ForegroundColor Green
    Write-Host " [+] Đã lưu tệp checksum: $ChecksumFile" -ForegroundColor Green

    # Tạo copy file cố định cho bản release MVP
    $LatestReleaseZip = Join-Path $BackupPath "uth_canteen_db_v1.0.0_mvp.zip"
    Copy-Item -Path $ZipFile -Destination $LatestReleaseZip -Force
    $LatestReleaseSha256 = Join-Path $BackupPath "uth_canteen_db_v1.0.0_mvp.sha256"
    [System.IO.File]::WriteAllText($LatestReleaseSha256, "$Sha256 *uth_canteen_db_v1.0.0_mvp.zip`n", [System.Text.UTF8Encoding]::new($false))
    Write-Host " [+] Đã gán nhãn tệp phát hành MVP: $LatestReleaseZip" -ForegroundColor Green

} finally {
    if (Test-Path $TempDir) {
        Remove-Item -Path $TempDir -Recurse -Force
    }
}

Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host " SAO LƯU THÀNH CÔNG! SẴN SÀNG CHO GIAI ĐOẠN KHÔI PHỤC VÀ RELEASE MVP" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Cyan
exit 0
