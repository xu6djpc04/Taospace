# fix_typeless.ps1 - Restart Typeless and Windows text input services
# Run when Typeless stops inserting text. Replaces rebooting.
# Usage: powershell -ExecutionPolicy Bypass -File .\output\fix_typeless.ps1
#
# 設計：只有「重啟服務 / 關閉舊 Typeless」需要管理員權限，這部分丟給隱藏的
# 提權子行程做；啟動 Typeless 一定要用「一般權限」，否則 Windows UIPI 隔離
# 會讓 Typeless 無法把文字插入一般權限的 app（即「不出字」的元凶之一）。

param([switch]$ServicesOnly)

$exe = "$env:LOCALAPPDATA\Programs\Typeless\Typeless.exe"

if ($ServicesOnly) {
    # === 提權子行程：只做需要管理員權限的事，做完自動結束（視窗隱藏） ===
    Get-Process TextInputHost, ctfmon -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Start-Sleep -Milliseconds 800
    Start-Process ctfmon.exe -ErrorAction SilentlyContinue
    Restart-Service -Name Audiosrv -Force -ErrorAction SilentlyContinue
    Restart-Service -Name AudioEndpointBuilder -Force -ErrorAction SilentlyContinue
    Get-Process Typeless -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    exit
}

# === 原始（一般權限）行程 ===
Write-Host "[1/3] Restarting input/audio services + closing Typeless (elevated)..."
Start-Process powershell -Verb RunAs -Wait -WindowStyle Hidden `
    -ArgumentList "-NoProfile -ExecutionPolicy Bypass -File `"$PSCommandPath`" -ServicesOnly"

Start-Sleep -Milliseconds 800
Write-Host "[2/3] Launching Typeless (normal user privilege)..."
if (Test-Path $exe) {
    explorer.exe $exe
    Write-Host "    Started: $exe"
} else {
    Write-Host "    Typeless.exe not found at expected path. Please open it manually."
}

Write-Host "[3/3] Done. Try dictating now."
