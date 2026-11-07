@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Insta360 X5 KI - eigene Windows EXE bauen
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0BAUE_WINDOWS_EXE.ps1"
if errorlevel 1 (
    echo.
    echo Der EXE-Bau konnte nicht abgeschlossen werden. Meldung oben beachten.
    pause
    exit /b 1
)
echo.
echo EXE-Programmordner wurde erstellt.
pause
