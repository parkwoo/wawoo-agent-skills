# Windows から UI mock を開く（WSL 内で http.server）
# 用法: cd <repo>\workspace\skills\website  →  .\preview-ui.ps1

$ErrorActionPreference = "Stop"
$Port = if ($env:PORT) { $env:PORT } else { 8765 }
$Here = $PSScriptRoot

Write-Host ""
Write-Host "WSL で preview-ui.sh を起動します (port $Port)..." -ForegroundColor Cyan
Write-Host "浏览器请打开: http://localhost:$Port/" -ForegroundColor Green
Write-Host "打不开时试 WSL IP（启动后脚本会打印）" -ForegroundColor Yellow
Write-Host "保持此窗口不关 · Ctrl+C 结束" -ForegroundColor Yellow
Write-Host ""

$wslPath = wsl wslpath -a $Here 2>$null
if (-not $wslPath) {
  Write-Host "未检测到 WSL。请在 Cursor 终端（WSL）里执行:" -ForegroundColor Red
  Write-Host "  cd /home/git/workspace/skills/website && ./preview-ui.sh"
  exit 1
}

wsl bash -lc "cd '$wslPath' && chmod +x preview-ui.sh && PORT=$Port exec ./preview-ui.sh"