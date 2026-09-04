$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $venvPython)) { py -m venv (Join-Path $root ".venv") }
& $venvPython -m pip install -r (Join-Path $root "requirements.txt") -r (Join-Path $root "requirements-build.txt")
& $venvPython -m PyInstaller --noconfirm --clean (Join-Path $root "DailyReport.spec")
if ($LASTEXITCODE -ne 0) { throw "EXE build failed." }
$exe = Join-Path $root "dist\DailyReport.exe"
Write-Host "Ready: $exe"
Write-Host ("Size: {0:N1} MB" -f ((Get-Item $exe).Length / 1MB))

