@echo off
setlocal DisableDelayedExpansion
title 4. GUI - Minimal Control Panel - Ai Team
color 0B
echo Starting Minimal GUI - No manual file nonsense needed...
python gui.py
if %ERRORLEVEL% NEQ 0 (
    py gui.py
)
pause
