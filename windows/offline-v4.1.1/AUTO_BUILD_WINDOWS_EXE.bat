@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Large Image Quality Enhancer - Automatic Windows EXE Build
echo ========================================================
echo Large Image Quality Enhancer - Automatic Windows EXE Build
echo ========================================================
echo.
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0SETUP_UND_BAU.ps1"
if errorlevel 1 (
  echo.
  echo Automatic build failed.
  echo Check the error message above.
  pause
  exit /b 1
)
echo.
echo Build completed.
pause
exit /b 0
