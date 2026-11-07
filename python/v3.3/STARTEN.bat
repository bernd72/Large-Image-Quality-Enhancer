@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title Insta360 X5 - DPRNet KI Optimierer

echo ==============================================
echo Insta360 X5 - DPRNet + SCUNet KI Optimierer v3.3
echo ==============================================
echo.
echo Pruefe eine geeignete Python-Version ...

set "PY_EXEC="
where py >nul 2>&1
if not errorlevel 1 (
    for %%V in (3.12 3.13 3.14 3.11 3.10) do (
        py -%%V -c "import sys; sys.exit(0 if sys.maxsize > 2**32 else 1)" >nul 2>&1
        if not errorlevel 1 (
            set "PY_EXEC=py -%%V"
            goto :python_found
        )
    )
)

rem Fallback fuer eine kompatible Python-Installation im PATH ohne py-Launcher.
where python >nul 2>&1
if not errorlevel 1 (
    python -c "import sys; sys.exit(0 if sys.maxsize > 2**32 and (3,10) <= sys.version_info[:2] <= (3,14) else 1)" >nul 2>&1
    if not errorlevel 1 (
        set "PY_EXEC=python"
        goto :python_found
    )
)

echo.
echo FEHLER: Keine unterstuetzte 64-Bit-Python-Version gefunden.
echo Python 3.15 wird von der benoetigten Bibliothek ai-edge-litert
echo noch nicht unterstuetzt.
echo.
echo Bitte Python 3.12 fuer Windows 64-Bit zusaetzlich installieren:
echo https://www.python.org/downloads/release/python-31210/
echo.
echo Dein vorhandenes Python muss nicht deinstalliert werden.
echo Danach diese STARTEN.bat erneut ausfuehren.
goto :fail

:python_found
echo Gefunden: %PY_EXEC%
%PY_EXEC% --version

rem Nur die lokale .venv pruefen und gegebenenfalls neu erzeugen.
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" -c "import sys; sys.exit(0 if sys.maxsize > 2**32 and (3,10) <= sys.version_info[:2] <= (3,14) else 1)" >nul 2>&1
    if errorlevel 1 (
        echo.
        echo Alte Programmumgebung benutzt eine inkompatible Python-Version.
        echo Erstelle die Programmumgebung neu ...
        rmdir /s /q ".venv"
        if exist ".venv" goto :fail
    )
)

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo Erstelle lokale Python-Umgebung ...
    %PY_EXEC% -m venv ".venv"
    if errorlevel 1 goto :fail
)

rem Selbst bei einer alten ready.txt wird die tatsaechliche Installation geprueft.
".venv\Scripts\python.exe" -c "import numpy, PIL, cv2; from ai_edge_litert.interpreter import Interpreter; import onnxruntime" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installiere Python-Bibliotheken fuer diese kompatible Python-Version ...
    ".venv\Scripts\python.exe" -m pip install --disable-pip-version-check -r "requirements.txt"
    if errorlevel 1 goto :fail
    ".venv\Scripts\python.exe" -c "import numpy, PIL, cv2; from ai_edge_litert.interpreter import Interpreter; import onnxruntime"
    if errorlevel 1 goto :fail
)

echo.
echo Starte die KI-Anwendung ...
".venv\Scripts\python.exe" "x5_dprnet.py"
if errorlevel 1 goto :fail
exit /b 0

:fail
echo.
echo Der Start wurde abgebrochen. Bitte die Meldung oben beachten.
pause
exit /b 1
