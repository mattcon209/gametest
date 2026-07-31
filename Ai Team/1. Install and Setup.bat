@echo off
setlocal EnableDelayedExpansion
:: FIX (Audit13): pin CWD to this script's folder so relative paths work
cd /d "%~dp0"
title 1. INSTALL and SETUP - Ai Team
color 0A

echo ================================================
echo  1. INSTALL AND SETUP - AI GAME DEV TEAM
echo  This will INSTALL and CONFIGURE, NOT start team
echo  Run this ONCE, then use 2. Start Team
echo ================================================
echo.

net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Not running as Admin - install may still work but may need Admin
)

echo [1/7] Checking Python...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where py >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Python not found. Installing via winget...
        winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
        timeout /t 20 >nul
        set PATH=!PATH!;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts
    ) else (
        echo Python launcher py found
    )
) else (
    echo Python found
)

echo [2/7] Checking Ollama...
where ollama >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Ollama not in PATH, adding common locations...
    set PATH=!PATH!;%LOCALAPPDATA%\Programs\Ollama;%ProgramFiles%\Ollama
    where ollama >nul 2>&1
    if !ERRORLEVEL! NEQ 0 (
        echo Installing Ollama via winget...
        winget install Ollama.Ollama --silent --accept-package-agreements --accept-source-agreements
        timeout /t 15 >nul
        set PATH=!PATH!;%LOCALAPPDATA%\Programs\Ollama;%ProgramFiles%\Ollama
    )
)

where ollama >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Ollama still not found. Close CMD and reopen, or reboot.
    pause
) else (
    ollama --version
)

echo [3/7] Starting Ollama service...
start /B ollama serve >nul 2>&1
timeout /t 5 >nul

echo [4/7] Creating folder structure...
mkdir output\code 2>nul
mkdir output\lore 2>nul
mkdir output\art 2>nul
mkdir output\qa 2>nul
mkdir output\audio 2>nul
mkdir build\engine 2>nul
mkdir build\systems 2>nul
mkdir build\assets 2>nul
mkdir build\content 2>nul
mkdir builds 2>nul
mkdir roles 2>nul
mkdir docs 2>nul
mkdir tools 2>nul

echo [5/7] Creating default files if missing...
if not exist "5. GDD.md" (
    echo Creating default 5. GDD.md...
    echo # GAME DESIGN DOCUMENT > "5. GDD.md"
    echo PROJECT: My Game >> "5. GDD.md"
)
if not exist INBOX.txt echo. > INBOX.txt
if not exist MEMORY.md echo # Studio Memory > MEMORY.md
if not exist tasks.json echo [] > tasks.json
if not exist logs.txt echo # Log start > logs.txt
if not exist live_status.txt echo Idle > live_status.txt

echo [6/7] Pulling AI Models - 6 models ~53GB - Keep PC on!
echo This needs internet ONCE. After this, 100 percent offline.
ollama pull qwen3:14b
ollama pull devstral:24b
ollama pull qwen2.5-coder:14b
ollama pull gemma3:12b
ollama pull deepseek-r1:14b
ollama pull gemma3:4b

echo [7/7] Verifying...
ollama list
where python
python --version 2>nul || py --version


echo.
echo [OPTIONAL] Compiler check for non-Python projects
echo   Your GDD's LANGUAGE field decides what build/run.bat will call.
echo   Python needs nothing extra. Other languages need a toolchain:
where g++ >nul 2>&1    && (echo   [OK] g++ found    - C++ builds can run) || (echo   [--] g++ MISSING  - C++: winget install -e --id MSYS2.MSYS2  ^(then pacman -S mingw-w64-ucrt-x86_64-gcc^))
where dotnet >nul 2>&1 && (echo   [OK] dotnet found - C# builds can run)  || (echo   [--] dotnet MISSING - C#: winget install -e --id Microsoft.DotNet.SDK.8)
where cargo >nul 2>&1  && (echo   [OK] cargo found  - Rust builds can run) || (echo   [--] cargo MISSING  - Rust: winget install -e --id Rustlang.Rustup)
where node >nul 2>&1   && (echo   [OK] node found   - JS/TS builds can run) || (echo   [--] node MISSING   - JS/TS: winget install -e --id OpenJS.NodeJS.LTS)
echo   Install only what your project needs, then REOPEN this window.
echo.
echo ================================================
echo  SETUP COMPLETE - 6 models installed
echo ================================================
pause
