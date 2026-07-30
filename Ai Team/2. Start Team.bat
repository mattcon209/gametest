@echo off
setlocal EnableDelayedExpansion
title 2. START TEAM - Live Scrolling Log - Ai Team
color 0B

echo ================================================
echo  2. START TEAM - AUTONOMOUS GAME STUDIO v6
echo  This IS the live scrolling log you asked for
echo  Leave this window open - it updates in real-time
echo ================================================
echo.

:: Refresh PATH to find ollama after install
set PATH=%PATH%;%LOCALAPPDATA%\Programs\Ollama;%ProgramFiles%\Ollama

where ollama >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Ollama not found! Run 1. Install and Setup.bat first
    echo Trying full path...
    if exist "%LOCALAPPDATA%\Programs\Ollama\ollama.exe" (
        set ollama_exe=%LOCALAPPDATA%\Programs\Ollama\ollama.exe
        "!LOCALAPPDATA!\Programs\Ollama\ollama.exe" --version
    ) else (
        pause
        exit /b
    )
) else (
    set ollama_exe=ollama
)

where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where py >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Python not found! Install Python 3.11
        pause
        exit /b
    ) else (
        set PYTHON=py
    )
) else (
    set PYTHON=python
)

if not exist studio.py (
    echo [ERROR] studio.py missing in %CD%
    pause
    exit /b
)

echo Starting Ollama background service if not already running...
start /B !ollama_exe! serve >nul 2>&1
timeout /t 3 >nul

echo.
echo GDD Prompt File (File #5): "%CD%\5. GDD.md"
echo Output Folder: "%CD%\output\"
echo Logs: "%CD%\logs.txt"
echo Memory: "%CD%\MEMORY.md"
echo.
echo Controls (from phone or second CMD):
echo   - Edit "5. GDD.md" and SAVE - team re-plans automatically
echo   - echo New idea ^> INBOX.txt  - send order to Director
echo   - echo pause ^> PAUSE  - pause team
echo   - del PAUSE  - resume team
echo   - Ctrl+C  - stop team (remembers via files)
echo.
echo ================================================
echo LIVE LOG BELOW - REAL TIME SCROLLING:
echo ================================================
echo.

!PYTHON! studio.py

echo.
echo ================================================
echo POST-RUN SMOKE CHECK (audits 3/4 recommendation):
echo ================================================
if exist tools\smoke_check.py (
    !PYTHON! tools\smoke_check.py
) else (
    echo smoke_check.py not found - skipping
)

echo.
echo ================================================
echo Team stopped. All progress saved in tasks.json + MEMORY.md
echo Your 4 top files:
echo  1. Install and Setup.bat - Setup
echo  2. Start Team.bat - This file (live log)
echo  3. Live Log Viewer.bat - Second monitor viewer
echo  5. GDD.md - Your prompt file
echo Run this file again to resume where left off.
echo ================================================
pause
