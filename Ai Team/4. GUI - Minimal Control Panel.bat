@echo off
setlocal EnableDelayedExpansion
title 4. GUI - Minimal Control Panel - Ai Team
color 0B

:: FIX (Audit13): pin the working directory to this script's folder. Launching
:: the .bat from anywhere other than the Ai Team folder (shortcut, Explorer
:: quirk, admin shell) made every relative path resolve elsewhere and the GUI
:: appeared "not to work at all".
cd /d "%~dp0"

echo Starting Minimal GUI...
echo Folder: %CD%
echo.

where python >nul 2>&1
if !ERRORLEVEL! EQU 0 (
    set "PYEXE=python"
) else (
    where py >nul 2>&1
    if !ERRORLEVEL! EQU 0 (
        set "PYEXE=py"
    ) else (
        echo [ERROR] Python not found on PATH.
        echo Run "1. Install and Setup.bat" first, then reopen this window.
        pause
        exit /b 1
    )
)

if not exist "gui.py" (
    echo [ERROR] gui.py not found in %CD%
    echo Keep this .bat inside the Ai Team folder.
    pause
    exit /b 1
)

!PYEXE! gui.py
if !ERRORLEVEL! NEQ 0 (
    echo.
    echo ================================================
    echo GUI exited with an error ^(code !ERRORLEVEL!^).
    echo The traceback is ABOVE this line - read it before closing.
    echo Common cause: Python installed without tkinter.
    echo   Reinstall Python 3.11+ and tick "tcl/tk and IDLE".
    echo ================================================
)
pause
