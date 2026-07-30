@echo off
setlocal DisableDelayedExpansion
title 3. LIVE LOG VIEWER - Real-Time Monitor
color 0E

echo ================================================
echo  3. LIVE LOG VIEWER - Active Scrolling Log
echo  Shows real-time updates from team
echo  Keep this on second monitor
echo ================================================
echo.
echo Watching: logs.txt + live_status.txt
echo This window auto-scrolls as team works
echo Press Ctrl+C to close viewer (team keeps running)
echo.
echo ================================================

if not exist logs.txt (
    echo logs.txt not found yet. Start team with 2. Start Team.bat first
    pause
    exit /b
)

powershell -Command "Write-Host '=== LIVE TAIL - Last 50 lines, following new entries ===' -ForegroundColor Cyan; Get-Content -Path 'logs.txt' -Tail 50 -Wait"
