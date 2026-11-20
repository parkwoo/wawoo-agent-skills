# Windows PowerShell からプレビュー（WSL のファイルを配信）
# 用法: エクスプローラで skills\website を開き、PowerShell で .\preview.ps1
# または: wsl bash -lc "cd /home/git/workspace/skills/website && ./preview.sh"

$ErrorActionPreference = "Stop"
$Port = if ($env:PORT) { $env:PORT } else { 8765 }
$Here = $PSScriptRoot

Write-Host "WSL 経由でプレビューサーバを起動します (port $Port)..." -ForegroundColor Cyan
Write-Host "ブラウザ: http://localhost:$Port/" -ForegroundColor Green
Write-Host "終了: Ctrl+C" -ForegroundColor Yellow
Write-Host ""

$wslPath = wsl wslpath -a $Here 2>$null
if (-not $wslPath) {
    Write-Host "WSL が見つかりません。Cursor 内ターミナルで次を実行してください:" -ForegroundColor Red
    Write-Host "  cd skills/website && bash ./preview.sh"
    exit 1
}

wsl bash -lc "cd '$wslPath' && PORT=$Port exec ./preview.sh"