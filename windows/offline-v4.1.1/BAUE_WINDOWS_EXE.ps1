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
    Write-Host "ERROR: $message" -ForegroundColor Red
    exit $code
}
Write-Host '======================================================='
Write-Host 'Insta360 X5 AI v4.1.1 - OFFLINE EXE build'
Write-Host '======================================================='
Write-Host 'The existing v3.3 edition and proxy EXE v4.0 remain unchanged.'
Write-Host 'The finished EXE requires no model downloads, proxy, or certificate prompts.'
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
        Fail "Model missing: models\$($entry.name). First copy it from your existing v3.3 installation." 2
    }
    $size = (Get-Item -LiteralPath $p).Length
    if ($size -lt $entry.min) {
        Fail "Model file too small or incomplete: $($entry.name) ($size bytes)" 2
    }
    if ($entry.name -like '*.tflite') {
        $f = [System.IO.File]::OpenRead($p)
        try {
            $bytes = New-Object byte[] 8
            $count = $f.Read($bytes, 0, 8)
        } finally { $f.Dispose() }
        if ($count -ne 8 -or [System.Text.Encoding]::ASCII.GetString($bytes,4,4) -ne 'TFL3') {
            Fail "Not a valid TFLite model: $($entry.name)" 2
        }
    }
    Write-Host ("Model found: {0} ({1:N1} MB)" -f $entry.name,($size / 1MB))
}
$extra = Join-Path $models 'DPRNet_512.tflite'
if (Test-Path -LiteralPath $extra -PathType Leaf) {
    Write-Host 'Optional DPRNet_512.tflite model is available.'
}

# The automatic build launcher can pass a private per-user Python installation.
# Without this argument, the existing py -3.12 workflow remains unchanged.
$pythonCommand = 'py'
$pythonCommandArgs = @('-3.12')
if ($PythonExe) {
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
        Fail "The supplied Python executable does not exist: $PythonExe" 3
    }
    $pythonCommand = $PythonExe
    $pythonCommandArgs = @()
}
try {
    & $pythonCommand @pythonCommandArgs -c 'import sys; assert sys.version_info[:2] == (3, 12) and sys.maxsize > 2**32; print(sys.version)'
}
catch { Fail 'Python 3.12 (64-bit) is missing or cannot run. Use AUTO_BUILD_WINDOWS_EXE.bat.' 3 }
if ($LASTEXITCODE -ne 0) { Fail 'Python 3.12 (64-bit) is missing or cannot run.' 3 }

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    Write-Host 'Creating a private build environment...'
    & $pythonCommand @pythonCommandArgs -m venv $venv
    if ($LASTEXITCODE -ne 0) { Fail 'Failed to create build environment.' 3 }
}
Write-Host ''
Write-Host 'Checking installed Python packages...'
# PowerShell 5.1 kann doppelte Anfuehrungszeichen in -c an Python verlieren.
# Deshalb enthaelt dieser Python-Pruefcode KEINE inneren Anfuehrungszeichen.
$checkCode = 'import numpy, PIL, cv2, onnxruntime, tkinter; from ai_edge_litert.interpreter import Interpreter; import PyInstaller'
& $python -c $checkCode
$needInstall = ($LASTEXITCODE -ne 0)
if ($needInstall) {
    Write-Host 'Installing missing Python packages required for building the EXE.'
    Write-Host 'Existing PIP_PROXY/PIP_CERT environment variables are used by pip.'
    $wheelhouse = Join-Path $project 'wheelhouse'
    $installArgs = @('-m','pip','install','--disable-pip-version-check')
    if ((Test-Path $wheelhouse) -and @(Get-ChildItem -Path $wheelhouse -Filter '*.whl' -File).Count -gt 0) {
        Write-Host 'Local wheelhouse found: package installation will not require internet.'
        $installArgs += @('--no-index','--find-links',$wheelhouse)
    }
    $installArgs += @('-r',(Join-Path $source 'requirements.txt'),'pyinstaller>=6.14,<7')
    & $python @installArgs
    if ($LASTEXITCODE -ne 0) {
        Fail 'Package installation failed. Building may require internet access, PIP_PROXY, or a local wheelhouse.' 4
    }
    & $python -c $checkCode
    if ($LASTEXITCODE -ne 0) { Fail 'A required Python package cannot be imported.' 4 }
} else {
    Write-Host 'All required packages are already installed. No download needed.' -ForegroundColor Green
}
Write-Host 'All required runtime libraries are available' -ForegroundColor Green

# Das spec-Verzeichnis beim allerersten Bau explizit anlegen.
$specDir = Join-Path $project 'spec'
New-Item -ItemType Directory -Force -Path $specDir | Out-Null
Write-Host 'Building portable Windows EXE (PyInstaller onedir)...'
Push-Location $source
try {
    & $python -m PyInstaller --noconfirm --clean --onedir --windowed --name $appName `
      --distpath $distRoot --workpath (Join-Path $project 'build') --specpath (Join-Path $project 'spec') `
      --collect-all ai_edge_litert --collect-all onnxruntime --collect-all cv2 `
      --hidden-import tkinter --hidden-import x5_denoise --hidden-import x5_batch --hidden-import x5_i18n `
      x5_dprnet.py
    if ($LASTEXITCODE -ne 0) { Fail 'PyInstaller failed to create the Windows EXE.' 5 }
} finally { Pop-Location }
$exe = Join-Path $exeDir ($appName + '.exe')
if (-not (Test-Path -LiteralPath $exe -PathType Leaf)) { Fail 'The expected EXE was not created.' 5 }

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
    if ($a -ne $b) { Fail "Model file was not copied completely: $($entry.name)" 6 }
}

$portableZip = Join-Path $project 'Insta360_X5_KI_Offline_Portable.zip'
try {
    if (Test-Path $portableZip) { Remove-Item $portableZip -Force }
    Compress-Archive -Path (Join-Path $exeDir '*') -DestinationPath $portableZip -CompressionLevel Optimal
    Write-Host "Portable ZIP: $portableZip"
} catch {
    Write-Host 'Could not create the portable ZIP. The EXE folder was created successfully.' -ForegroundColor Yellow
}
Write-Host ''
Write-Host 'DONE: Windows EXE ready for fully offline operation.' -ForegroundColor Green
Write-Host $exe
Write-Host 'Copy the ENTIRE dist application folder to the destination Windows PC.'
Write-Host 'The destination PC needs no Python, proxy settings, certificates, or internet access.'
exit 0
