param([string]$PythonExe = '')
# Eigenstaendiger EXE-Bau fuer Windows x64; die FERTIGE EXE arbeitet vollständig OFFLINE.
# Keine Proxy-/Zertifikatsdialoge im Programm und keine Modell-Downloads zur Laufzeit.
# Nur beim BAUEN koennen Python-Pakete aus dem Internet benoetigt werden.
$ErrorActionPreference = 'Stop'
$project = $PSScriptRoot
$source = Join-Path $project 'source'
$models = Join-Path $project 'models'
$venv = Join-Path $project '.buildvenv'
$python = Join-Path $venv 'Scripts\python.exe'
$appName = 'Insta360_X5_KI_Offline'
$distRoot = Join-Path $project 'dist'
$exeDir = Join-Path $distRoot $appName

function Fail($message, $code=1) {
    Write-Host "FEHLER: $message" -ForegroundColor Red
    exit $code
}
Write-Host '======================================================='
Write-Host 'Insta360 X5 KI v4.1.1 - EXE fuer den OFFLINE-Betrieb'
Write-Host '======================================================='
Write-Host 'Die alte Version 3.3 und die Proxy-EXE v4.0 bleiben unveraendert.'
Write-Host 'Keine Modell-Downloads, Proxy- oder Zertifikatsabfragen in der EXE.'
Write-Host ''

# Zuerst Modell-Dateien pruefen, damit keine Pakete unnoetig geladen werden.
$required = @(
    @{ name='DPRNet_1024.tflite'; min=50000 },
    @{ name='scunet_color_real_psnr.onnx'; min=100000 },
    @{ name='scunet_color_real_psnr.onnx.data'; min=30000000 }
)
foreach($entry in $required) {
    $p = Join-Path $models $entry.name
    if (-not (Test-Path -LiteralPath $p -PathType Leaf)) {
        Fail "Modell fehlt: models\$($entry.name). Erst aus deiner vorhandenen v3.3-Installation kopieren." 2
    }
    $size = (Get-Item -LiteralPath $p).Length
    if ($size -lt $entry.min) {
        Fail "Modelldatei zu klein oder unvollstaendig: $($entry.name) ($size Bytes)" 2
    }
    if ($entry.name -like '*.tflite') {
        $f = [System.IO.File]::OpenRead($p)
        try {
            $bytes = New-Object byte[] 8
            $count = $f.Read($bytes, 0, 8)
        } finally { $f.Dispose() }
        if ($count -ne 8 -or [System.Text.Encoding]::ASCII.GetString($bytes,4,4) -ne 'TFL3') {
            Fail "Kein gueltiges TFLite-Modell: $($entry.name)" 2
        }
    }
    Write-Host ("Modell vorhanden: {0} ({1:N1} MB)" -f $entry.name,($size / 1MB))
}
$extra = Join-Path $models 'DPRNet_512.tflite'
if (Test-Path -LiteralPath $extra -PathType Leaf) {
    Write-Host 'Optionales Modell DPRNet_512.tflite ist vorhanden.'
}

# The automatic build launcher can pass a private per-user Python installation.
# Without this argument, the existing py -3.12 workflow remains unchanged.
$pythonCommand = 'py'
$pythonCommandArgs = @('-3.12')
if ($PythonExe) {
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
        Fail "Die uebergebene Python-Datei fehlt: $PythonExe" 3
    }
    $pythonCommand = $PythonExe
    $pythonCommandArgs = @()
}
try {
    & $pythonCommand @pythonCommandArgs -c 'import sys; assert sys.version_info[:2] == (3, 12) and sys.maxsize > 2**32; print(sys.version)'
}
catch { Fail 'Python 3.12 (64 Bit) fehlt oder startet nicht. Nutze AUTO_BUILD_WINDOWS_EXE.bat.' 3 }
if ($LASTEXITCODE -ne 0) { Fail 'Python 3.12 (64 Bit) fehlt oder startet nicht.' 3 }

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    Write-Host 'Erstelle eigene Build-Umgebung ...'
    & $pythonCommand @pythonCommandArgs -m venv $venv
    if ($LASTEXITCODE -ne 0) { Fail 'Erstellen der Build-Umgebung fehlgeschlagen.' 3 }
}
Write-Host ''
Write-Host 'Pruefe vorhandene Python-Bibliotheken ...'
# PowerShell 5.1 kann doppelte Anfuehrungszeichen in -c an Python verlieren.
# Deshalb enthaelt dieser Python-Pruefcode KEINE inneren Anfuehrungszeichen.
$checkCode = 'import numpy, PIL, cv2, onnxruntime, tkinter; from ai_edge_litert.interpreter import Interpreter; import PyInstaller'
& $python -c $checkCode
$needInstall = ($LASTEXITCODE -ne 0)
if ($needInstall) {
    Write-Host 'Installiere fehlende Python-Bibliotheken fuer den EXE-Bau.'
    Write-Host 'Vorhandene PIP_PROXY/PIP_CERT-Umgebungsvariablen werden von pip verwendet.'
    $wheelhouse = Join-Path $project 'wheelhouse'
    $installArgs = @('-m','pip','install','--disable-pip-version-check')
    if ((Test-Path $wheelhouse) -and @(Get-ChildItem -Path $wheelhouse -Filter '*.whl' -File).Count -gt 0) {
        Write-Host 'Lokales Wheelhouse gefunden: Paketinstallation erfolgt ohne Internet.'
        $installArgs += @('--no-index','--find-links',$wheelhouse)
    }
    $installArgs += @('-r',(Join-Path $source 'requirements.txt'),'pyinstaller>=6.14,<7')
    & $python @installArgs
    if ($LASTEXITCODE -ne 0) {
        Fail 'Paketinstallation fehlgeschlagen. Nur zum EXE-Bau sind ggf. Internet, PIP_PROXY oder ein lokales wheelhouse erforderlich.' 4
    }
    & $python -c $checkCode
    if ($LASTEXITCODE -ne 0) { Fail 'Eine benoetigte Python-Bibliothek ist nicht startfaehig.' 4 }
} else {
    Write-Host 'Alle Bibliotheken sind bereits installiert. Kein erneuter Download erforderlich.' -ForegroundColor Green
}
Write-Host 'Alle Laufzeitbibliotheken OK' -ForegroundColor Green

# Das spec-Verzeichnis beim allerersten Bau explizit anlegen.
$specDir = Join-Path $project 'spec'
New-Item -ItemType Directory -Force -Path $specDir | Out-Null
Write-Host 'Erstelle vollstaendige Windows-EXE (PyInstaller onedir) ...'
Push-Location $source
try {
    & $python -m PyInstaller --noconfirm --clean --onedir --windowed --name $appName `
      --distpath $distRoot --workpath (Join-Path $project 'build') --specpath (Join-Path $project 'spec') `
      --collect-all ai_edge_litert --collect-all onnxruntime --collect-all cv2 `
      --hidden-import tkinter --hidden-import x5_denoise --hidden-import x5_batch `
      x5_dprnet.py
    if ($LASTEXITCODE -ne 0) { Fail 'PyInstaller konnte die Windows-EXE nicht erstellen.' 5 }
} finally { Pop-Location }
$exe = Join-Path $exeDir ($appName + '.exe')
if (-not (Test-Path -LiteralPath $exe -PathType Leaf)) { Fail 'Die erwartete EXE wurde nicht erstellt.' 5 }

# KI-Gewichte werden NICHT in die EXE hineingepackt; sie liegen daneben und
# koennen ohne Internet zu jeder Zeit verwendet werden.
$outModels = Join-Path $exeDir 'models'
New-Item -ItemType Directory -Force -Path $outModels | Out-Null
foreach ($entry in $required) {
    Copy-Item -LiteralPath (Join-Path $models $entry.name) -Destination (Join-Path $outModels $entry.name) -Force
}
if (Test-Path -LiteralPath $extra -PathType Leaf) {
    Copy-Item -LiteralPath $extra -Destination (Join-Path $outModels 'DPRNet_512.tflite') -Force
}
Copy-Item -LiteralPath (Join-Path $project 'README_OFFLINE.txt') -Destination (Join-Path $exeDir 'README_OFFLINE.txt') -Force

# Pruefen, ob die Kopien vollstaendig sind.
foreach ($entry in $required) {
    $a = (Get-Item -LiteralPath (Join-Path $models $entry.name)).Length
    $b = (Get-Item -LiteralPath (Join-Path $outModels $entry.name)).Length
    if ($a -ne $b) { Fail "Modelldatei wurde nicht vollstaendig kopiert: $($entry.name)" 6 }
}

$portableZip = Join-Path $project 'Insta360_X5_KI_Offline_Portable.zip'
try {
    if (Test-Path $portableZip) { Remove-Item $portableZip -Force }
    Compress-Archive -Path (Join-Path $exeDir '*') -DestinationPath $portableZip -CompressionLevel Optimal
    Write-Host "Transport-ZIP: $portableZip"
} catch {
    Write-Host 'Transport-ZIP konnte nicht geschrieben werden. Der EXE-Ordner ist trotzdem fertig.' -ForegroundColor Yellow
}
Write-Host ''
Write-Host 'FERTIG: Windows-EXE fuer vollstaendig lokalen Betrieb.' -ForegroundColor Green
Write-Host $exe
Write-Host 'Den GESAMTEN dist-Programmordner auf den anderen Windows-PC kopieren.'
Write-Host 'Kein Python, kein Proxy, keine Zertifikate, kein Internet auf dem ZIEL-PC erforderlich.'
exit 0
