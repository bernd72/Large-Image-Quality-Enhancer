@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Insta360 X5 AI - Build Windows EXE
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0BAUE_WINDOWS_EXE.ps1"
if errorlevel 1 (
    echo.
    echo EXE build failed. See error message above.
    pause
    exit /b 1
)
echo.
echo EXE application folder has been created.
pause
