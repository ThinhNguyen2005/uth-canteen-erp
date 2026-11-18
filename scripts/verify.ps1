$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
$failed = $false
Write-Host 'Compose syntax (example values, no secrets printed):'
docker compose --env-file .env.example config --quiet
if ($LASTEXITCODE -ne 0) { $failed = $true; Write-Host 'FAIL: Compose syntax' } else { Write-Host 'PASS: Compose syntax' }
foreach ($path in @('.env', 'config/odoo.conf')) {
    git check-ignore -q --no-index $path
    if ($LASTEXITCODE -ne 0) { $failed = $true; Write-Host "FAIL: $path is not ignored" }
    else { Write-Host "PASS: $path is ignored" }
    $tracked = @(git ls-files -- $path)
    if ($tracked.Count -gt 0) { $failed = $true; Write-Host "FAIL: $path is tracked" }
}
docker info --format '{{.ServerVersion}}' 2>$null | Out-Null
if ($LASTEXITCODE -ne 0) { Write-Host 'BLOCKED: Docker Engine unavailable; runtime checks not run.'; if ($failed) { exit 1 } else { exit 2 } }
docker compose ps --status running --services | Out-String | Tee-Object -Variable running | Write-Host
if ($LASTEXITCODE -ne 0 -or $running -notmatch '(?m)^db\s*$' -or $running -notmatch '(?m)^odoo\s*$') { Write-Host 'BLOCKED: services are not running; runtime checks not run.'; if ($failed) { exit 1 } else { exit 2 } }
docker compose exec -T db sh -c 'pg_isready -U "$POSTGRES_USER" -d postgres'
if ($LASTEXITCODE -ne 0) { $failed = $true; Write-Host 'FAIL: PostgreSQL readiness' } else { Write-Host 'PASS: PostgreSQL readiness' }
try { $response = Invoke-WebRequest -Uri 'http://127.0.0.1:8069/web/login' -UseBasicParsing -TimeoutSec 15; Write-Host "PASS: HTTP $($response.StatusCode)" }
catch { $failed = $true; Write-Host "FAIL: HTTP $($_.Exception.Message)" }
Write-Host 'BLOCKED: addon install and upgrade require an explicitly selected disposable database; see docs/setup.md.'
if ($failed) { exit 1 } else { exit 2 }
