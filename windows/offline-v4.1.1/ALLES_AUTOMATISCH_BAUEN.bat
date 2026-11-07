@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Large Image Quality Enhancer - automatischer Windows-Bau
echo ========================================================
echo Large Image Quality Enhancer - Windows-Bau ohne Python-Vorinstallation
echo ========================================================
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0SETUP_UND_BAU.ps1"
if errorlevel 1 (
  echo.
  echo Der automatische Bau konnte nicht abgeschlossen werden.
  echo Hinweise stehen in der Fehlermeldung oben.
  pause
  exit /b 1
)
echo.
echo Der Bauvorgang ist abgeschlossen.
pause
exit /b 0
