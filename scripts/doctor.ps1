$ErrorActionPreference = 'Continue'
Set-Location (Join-Path $PSScriptRoot '..')
Write-Host 'Git:'
git status --short --branch
Write-Host 'Docker and Compose:'
docker --version
docker compose version
docker info --format '{{.ServerVersion}}'
if ($LASTEXITCODE -ne 0) { Write-Warning 'BLOCKED: Docker Engine unavailable; container conflicts cannot be checked.' }
else { docker ps --format 'table {{.Names}}\t{{.Ports}}' }
Write-Host 'Listeners on port 8069:'
$listeners = Get-NetTCPConnection -LocalPort 8069 -State Listen -ErrorAction SilentlyContinue
if ($listeners) { $listeners | Select-Object LocalAddress, LocalPort, OwningProcess | Format-Table }
else { Write-Host 'No listener detected.' }
Write-Host 'Codex:'
if (Get-Command codex -ErrorAction SilentlyContinue) { codex --version } else { Write-Warning 'Codex CLI unavailable.' }
