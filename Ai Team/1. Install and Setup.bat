@echo off
setlocal DisableDelayedExpansion
title 1. INSTALL and SETUP - Ai Team
color 0A

echo ================================================
echo  1. INSTALL AND SETUP - AI GAME DEV TEAM
echo  This will INSTALL and CONFIGURE, NOT start team
echo  Run this ONCE, then use 2. Start Team
echo ================================================
echo.

:: Check admin - not required but warn
net session >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [WARNING] Not running as Admin - install may still work but may need Admin
    echo Right click - Run as admin if it fails
)

echo [1/7] Checking Python...
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    where py >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Python not found. Installing via winget...
        winget install Python.Python.3.11 --silent --accept-package-agreements --accept-source-agreements
        echo Waiting for Python install...
        timeout /t 20 >nul
        set PATH=%PATH%;%LOCALAPPDATA%\Programs\Python\Python311;%LOCALAPPDATA%\Programs\Python\Python311\Scripts
    ) else (
        echo Python launcher py found
    )
) else (
    echo Python found
)

echo [2/7] Checking Ollama - The Model Switcher...
where ollama >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Ollama not in PATH, adding common locations...
    set PATH=%PATH%;%LOCALAPPDATA%\Programs\Ollama;%ProgramFiles%\Ollama;%LOCALAPPDATA%\Programs\Ollama

    where ollama >nul 2>&1
    if %ERRORLEVEL% NEQ 0 (
        echo Ollama not found. Installing via winget...
        winget install Ollama.Ollama --silent --accept-package-agreements --accept-source-agreements
        echo Waiting 15 sec for Ollama install...
        timeout /t 15 >nul
        set PATH=%PATH%;%LOCALAPPDATA%\Programs\Ollama;%ProgramFiles%\Ollama
    )
)

where ollama >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Ollama still not found in PATH. Please close CMD and reopen, or reboot, then run again.
    echo Or use full path: %LOCALAPPDATA%\Programs\Ollama\ollama.exe list
    pause
) else (
    echo Ollama found:
    ollama --version
)

echo [3/7] Starting Ollama service in background...
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
    echo Creating default 5. GDD.md prompt file...
    echo # GAME DESIGN DOCUMENT - Edit this file anytime > "5. GDD.md"
    echo # This is file #4 - Your Prompt File - Team watches this constantly >> "5. GDD.md"
    echo # Edit and SAVE this file - Coordinator AURA will auto re-plan >> "5. GDD.md"
    echo PROJECT: My Game >> "5. GDD.md"
    echo GENRE: Your genre here >> "5. GDD.md"
) else (
    echo Found existing 5. GDD.md - keeping it
)
if exist "GDD.md" (
    if not exist "5. GDD.md" (
        echo Migrating legacy GDD.md to 5. GDD.md...
        move "GDD.md" "5. GDD.md" >nul
    )
)
if not exist INBOX.txt (
    echo. > INBOX.txt
)
if not exist MEMORY.md (
    echo # Studio Memory > MEMORY.md
)
if not exist tasks.json (
    echo [] > tasks.json
)
if not exist logs.txt (
    echo # Log start > logs.txt
)
if not exist live_status.txt (
    echo Idle > live_status.txt
)

echo [6/7] Pulling AI Models - BIG DOWNLOAD 50GB TOTAL - Keep PC on!
echo This needs internet ONCE. After this, 100 percent offline.
echo If this fails, run the ollama pull commands manually.
echo.

echo   - Pulling qwen3:14b (Director AURA) - 9GB...
ollama pull qwen3:14b

echo   - Pulling devstral:24b (Lead Programmer FORGE) - 14GB BIGGEST...
ollama pull devstral:24b

echo   - Pulling qwen2.5-coder:14b (Gameplay SPARK) - 8.8GB...
ollama pull qwen2.5-coder:14b

echo   - Pulling gemma3:12b (Writer LORE + Artist PIXEL) - 7.8GB...
ollama pull gemma3:12b

echo   - Pulling deepseek-r1:14b (QA GLITCH) - 9.5GB...
ollama pull deepseek-r1:14b

echo   - Pulling gemma3:4b (Audio AUDIO) - 3.3GB...
ollama pull gemma3:4b

echo.
echo [7/7] Verifying install...
ollama list
echo.
where python
python --version 2>nul || py --version
echo.

echo ================================================
echo  SETUP COMPLETE - NOT STARTING TEAM
echo ================================================
echo  What was installed:
echo   - Ollama (model switcher/manager)
echo   - Python (if missing)
echo   - 6 AI Models (53GB) in C:\Users\%USERNAME%\.ollama\models
echo.
echo  Next steps:
echo   1. Edit 5. GDD.md - Your prompt file - Describe your game
echo   2. Double-click 2. Start Team.bat - Starts team + live log
echo   3. Optional: Double-click 3. Live Log Viewer.bat
echo.
echo  To control from phone while running:
echo   echo Add boss fish ^> INBOX.txt
echo   echo pause ^> PAUSE
echo   del PAUSE
echo ================================================
pause
