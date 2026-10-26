$ErrorActionPreference = 'Stop'
$projectPath = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $projectPath '.venv\Scripts\python.exe'
if (!(Test-Path -LiteralPath $pythonPath)) {
    python -m venv (Join-Path $projectPath '.venv')
}
& $pythonPath -m pip install -r (Join-Path $projectPath 'backend\requirements-dev.txt')
Push-Location (Join-Path $projectPath 'backend\template-runtime')
try { npm.cmd ci --ignore-scripts --no-audit --no-fund } finally { Pop-Location }
Push-Location (Join-Path $projectPath 'frontend')
try { npm.cmd ci --no-audit --no-fund } finally { Pop-Location }
$logPath = Join-Path $projectPath '.local-logs'
New-Item -ItemType Directory -Path $logPath -Force | Out-Null
$backendProcess = Start-Process -FilePath $pythonPath -ArgumentList '-m','uvicorn','main:app','--host','127.0.0.1','--port','8000' -WorkingDirectory (Join-Path $projectPath 'backend') -RedirectStandardOutput (Join-Path $logPath 'backend.log') -RedirectStandardError (Join-Path $logPath 'backend-errors.log') -WindowStyle Hidden -PassThru
$nodePath = (Get-Command node.exe).Source
$frontendProcess = Start-Process -FilePath $nodePath -ArgumentList 'node_modules/vite/bin/vite.js','--host','127.0.0.1','--port','5173' -WorkingDirectory (Join-Path $projectPath 'frontend') -RedirectStandardOutput (Join-Path $logPath 'frontend.log') -RedirectStandardError (Join-Path $logPath 'frontend-errors.log') -WindowStyle Hidden -PassThru
@{backend=$backendProcess.Id;frontend=$frontendProcess.Id} | ConvertTo-Json | Set-Content (Join-Path $logPath 'processes.json')
Write-Host 'Snap2Ship: http://127.0.0.1:5173 | API: http://127.0.0.1:8000/health'
Write-Host "Logs and process IDs: $logPath"
