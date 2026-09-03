# Run this script from an elevated PowerShell after PostgreSQL has been installed.
$ErrorActionPreference = "Stop"
$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$psql = Get-ChildItem "C:\Program Files\PostgreSQL\*\bin\psql.exe" |
    Sort-Object FullName -Descending |
    Select-Object -First 1

if (-not $psql) {
    throw "PostgreSQL not found. Install it first: winget install --id PostgreSQL.PostgreSQL.18 --exact"
}

$appPassword = Read-Host "Password for daily_reports_app"
$env:PGPASSWORD = Read-Host "Password for postgres"
$escapedPassword = $appPassword.Replace("'", "''")

function Invoke-Psql {
    param([Parameter(Mandatory = $true)][string[]]$Arguments)
    $result = & $psql.FullName @Arguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
        throw ($result -join [Environment]::NewLine)
    }
    return $result
}

$roleExists = Invoke-Psql @("-U", "postgres", "-h", "127.0.0.1", "-tAc", "SELECT 1 FROM pg_roles WHERE rolname='daily_reports_app'")
if ($roleExists -ne "1") {
    Invoke-Psql @("-U", "postgres", "-h", "127.0.0.1", "-v", "ON_ERROR_STOP=1", "-c", "CREATE USER daily_reports_app WITH PASSWORD '$escapedPassword'") | Out-Host
} else {
    Invoke-Psql @("-U", "postgres", "-h", "127.0.0.1", "-v", "ON_ERROR_STOP=1", "-c", "ALTER USER daily_reports_app WITH PASSWORD '$escapedPassword'") | Out-Host
}
$dbExists = Invoke-Psql @("-U", "postgres", "-h", "127.0.0.1", "-tAc", "SELECT 1 FROM pg_database WHERE datname='daily_reports'")
if ($dbExists -ne "1") {
    Invoke-Psql @("-U", "postgres", "-h", "127.0.0.1", "-v", "ON_ERROR_STOP=1", "-c", "CREATE DATABASE daily_reports OWNER daily_reports_app ENCODING 'UTF8'") | Out-Host
}
Remove-Item Env:PGPASSWORD

Write-Host "Database and application role are ready. Copy .env.example to .env and set POSTGRES_PASSWORD."
