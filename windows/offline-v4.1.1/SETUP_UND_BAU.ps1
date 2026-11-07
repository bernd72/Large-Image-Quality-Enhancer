# Bootstrap for Windows 11 x64: downloads dependencies, then calls the existing EXE builder.
# It requires no PRE-EXISTING Python, but installs a private per-user Python if needed.
# Downloads occur only during build; the final application remains offline.
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$root = $PSScriptRoot
$models = Join-Path $root 'models'
$cache = Join-Path $root '.download-cache'
$privateDir = Join-Path $env:LOCALAPPDATA 'LIQE\Python312'
$privatePython = Join-Path $privateDir 'python.exe'
$pythonInstaller = Join-Path $cache 'python-3.12.10-amd64.exe'
$pythonUrl = 'https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe'

function Assert-File {
    param([string]$File, [long]$MinBytes, [string]$ExpectedSha256 = '')
    if (-not (Test-Path -LiteralPath $File -PathType Leaf)) { return $false }
    if ((Get-Item -LiteralPath $File).Length -lt $MinBytes) { return $false }
    if ($ExpectedSha256) {
        $hash = (Get-FileHash -LiteralPath $File -Algorithm SHA256).Hash
        if ($hash -ine $ExpectedSha256) { return $false }
    }
    return $true
}

function Fetch-File {
    param([string]$Url, [string]$Dest, [long]$MinBytes, [string]$ExpectedSha256 = '')
    if (Assert-File $Dest $MinBytes $ExpectedSha256) {
        Write-Host ("Already present: " + (Split-Path $Dest -Leaf))
        return
    }
    if (Test-Path -LiteralPath $Dest) {
        Write-Host ("Existing file is incomplete or unexpected: " + $Dest) -ForegroundColor Yellow
        Remove-Item -LiteralPath $Dest -Force
    }
    New-Item -Path (Split-Path $Dest -Parent) -ItemType Directory -Force | Out-Null
    $part = $Dest + '.download'
    for ($attempt = 1; $attempt -le 3; $attempt++) {
        try {
            if (Test-Path -LiteralPath $part) { Remove-Item -LiteralPath $part -Force }
            Write-Host ("Downloading: " + (Split-Path $Dest -Leaf) + " (attempt $attempt/3)")
            Invoke-WebRequest -Uri $Url -OutFile $part -UseBasicParsing -TimeoutSec 600 -MaximumRedirection 10
            if (-not (Assert-File $part $MinBytes $ExpectedSha256)) {
                throw 'File too small or SHA-256 verification failed.'
            }
            Move-Item -LiteralPath $part -Destination $Dest -Force
            $mb = [math]::Round((Get-Item -LiteralPath $Dest).Length / 1MB, 1)
            Write-Host ("Download OK: " + (Split-Path $Dest -Leaf) + " ($mb MB)") -ForegroundColor Green
            return
        } catch {
            Write-Host ("Download failed: " + $_.Exception.Message) -ForegroundColor Yellow
            if ($attempt -eq 3) {
                throw ("Download failed after 3 attempts: " + $Url + ". Check internet/proxy access or place the file manually in the specified folder.")
            }
            Start-Sleep -Seconds (2 * $attempt)
        } finally {
            if (Test-Path -LiteralPath $part) { Remove-Item -LiteralPath $part -Force }
        }
    }
}

function Test-Python312 {
    param([string]$Exe, [string[]]$Args = @())
    try {
        & $Exe @Args -c 'import sys; assert sys.version_info[:2] == (3, 12) and sys.maxsize > 2**32' 2>$null
        return ($LASTEXITCODE -eq 0)
    } catch { return $false }
}

Write-Host ''
Write-Host 'Large Image Quality Enhancer - automatic EXE build'
Write-Host '----------------------------------------------------'
Write-Host 'This script can download Python 3.12, Python packages, and AI models.'
Write-Host 'If needed, Python is installed for the current user only.'
Write-Host 'The PATH is not modified; administrator rights are normally not required.'
Write-Host 'The finished EXE requires neither Python nor internet access.'
Write-Host ''
if ($root.Length -gt 95) {
    Write-Warning 'Directory path is very long. Consider extracting to C:\LIQE.'
}
if (-not [Environment]::Is64BitOperatingSystem) { throw '64-bit Windows is required.' }

# An existing Python installation can be used; otherwise install into LocalAppData.
$usePython = ''
if (Test-Python312 $privatePython) {
    $usePython = $privatePython
    Write-Host 'A suitable private Python installation is already available.'
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    if (Test-Python312 'py' @('-3.12')) {
        Write-Host 'Python 3.12 is already installed. No reinstallation is needed.'
    }
}
if (-not $usePython) {
    $hasPy = $false
    if (Get-Command py -ErrorAction SilentlyContinue) {
        $hasPy = Test-Python312 'py' @('-3.12')
    }
    if (-not $hasPy) {
        Write-Host ''
        Write-Host 'Python 3.12 will be downloaded from the official python.org server.'
        Write-Host 'It will be installed for the current user without changing PATH.'
        $answer = Read-Host 'Install Python automatically now? [Y/n]'
        if ($answer -match '^[nN]') { throw 'Cancelled: Python 3.12 is required to build the EXE.' }
        Fetch-File $pythonUrl $pythonInstaller 20000000
        $signature = Get-AuthenticodeSignature -LiteralPath $pythonInstaller
        if ($signature.Status -ne 'Valid' -or
            -not $signature.SignerCertificate -or
            $signature.SignerCertificate.Subject -notmatch 'Python Software Foundation') {
            throw 'Security check failed: the Python installer has no valid PSF signature.'
        }
        Write-Host 'Official Python installer signature verified.'
        New-Item -Path $privateDir -ItemType Directory -Force | Out-Null
        $args = ('/quiet InstallAllUsers=0 TargetDir="{0}" Include_pip=1 Include_tcltk=1 Include_dev=1 Include_launcher=0 Include_test=0 Include_doc=0 Shortcuts=0 AssociateFiles=0 PrependPath=0 AppendPath=0' -f $privateDir)
        $proc = Start-Process -FilePath $pythonInstaller -ArgumentList $args -Wait -PassThru
        if ($proc.ExitCode -ne 0 -or -not (Test-Python312 $privatePython)) {
            throw ("Private Python installation failed (exit code " + $proc.ExitCode + "). Windows security policies or a proxy might be blocking the installer.")
        }
        $usePython = $privatePython
        Write-Host 'Python was installed for the current user.' -ForegroundColor Green
    }
}

# Models are downloaded from their own upstream hosting, not copied into GitHub.
$manifest = @(
    @{ Name='DPRNet_1024.tflite'; Url='https://raw.githubusercontent.com/raspberrypi/AI_enhance/main/DPRNet_1024.tflite'; Min=50000; Hash='' },
    @{ Name='scunet_color_real_psnr.onnx'; Url='https://huggingface.co/Heliosoph/scunet-onnx/resolve/main/scunet_color_real_psnr.onnx?download=true'; Min=100000; Hash='231be201ab413dbc999d7951caa9844846b93a12a40a41e037d6b5888ed4e88c' },
    @{ Name='scunet_color_real_psnr.onnx.data'; Url='https://huggingface.co/Heliosoph/scunet-onnx/resolve/main/scunet_color_real_psnr.onnx.data?download=true'; Min=30000000; Hash='' }
)
$missing = @($manifest | Where-Object { -not (Assert-File (Join-Path $models $_.Name) $_.Min $_.Hash) })
if ($missing.Count -gt 0) {
    Write-Host ''
    Write-Host 'The following pretrained models are missing:'
    $missing | ForEach-Object { Write-Host (' - ' + $_.Name) }
    Write-Host 'Sources: raspberrypi/AI_enhance (BSD-2-Clause), Heliosoph/scunet-onnx (Apache-2.0).'
    Write-Host 'These third-party files are subject to their respective license terms.'
    Write-Host 'See THIRD_PARTY_NOTICES.md in the repository root for details.'
    $consent = Read-Host 'Download these model files directly from their providers? [Y/n]'
    if ($consent -match '^[nN]') {
        throw 'AI models are missing. Copy the three files into the models folder manually and retry.'
    }
    foreach ($model in $missing) {
        Fetch-File $model.Url (Join-Path $models $model.Name) $model.Min $model.Hash
    }
}
Write-Host 'All required model files are present.' -ForegroundColor Green

$builder = Join-Path $root 'BAUE_WINDOWS_EXE.ps1'
Write-Host ''
Write-Host 'Starting the EXE build. This may take several minutes.'
if ($usePython) {
    & $builder -PythonExe $usePython
} else {
    & $builder
}
if ($LASTEXITCODE -ne 0) { throw ('EXE build failed (exit code ' + $LASTEXITCODE + ').') }
Write-Host ''
Write-Host ('Done! Portable application: ' + (Join-Path $root 'dist\Insta360_X5_KI_Offline')) -ForegroundColor Green
Write-Host 'Copy the entire dist application folder to the destination PC.'
