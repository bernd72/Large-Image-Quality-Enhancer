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
        Write-Host ("Bereits vorhanden: " + (Split-Path $Dest -Leaf))
        return
    }
    if (Test-Path -LiteralPath $Dest) {
        Write-Host ("Vorhandene Datei ist unvollstaendig / unerwartet: " + $Dest) -ForegroundColor Yellow
        Remove-Item -LiteralPath $Dest -Force
    }
    New-Item -Path (Split-Path $Dest -Parent) -ItemType Directory -Force | Out-Null
    $part = $Dest + '.download'
    for ($attempt = 1; $attempt -le 3; $attempt++) {
        try {
            if (Test-Path -LiteralPath $part) { Remove-Item -LiteralPath $part -Force }
            Write-Host ("Lade: " + (Split-Path $Dest -Leaf) + " (Versuch $attempt/3)")
            Invoke-WebRequest -Uri $Url -OutFile $part -UseBasicParsing -TimeoutSec 600 -MaximumRedirection 10
            if (-not (Assert-File $part $MinBytes $ExpectedSha256)) {
                throw 'Datei zu klein oder SHA256-Pruefung fehlgeschlagen.'
            }
            Move-Item -LiteralPath $part -Destination $Dest -Force
            $mb = [math]::Round((Get-Item -LiteralPath $Dest).Length / 1MB, 1)
            Write-Host ("Download OK: " + (Split-Path $Dest -Leaf) + " ($mb MB)") -ForegroundColor Green
            return
        } catch {
            Write-Host ("Download fehlgeschlagen: " + $_.Exception.Message) -ForegroundColor Yellow
            if ($attempt -eq 3) {
                throw ("Download gescheitert: " + $Url + ". Bitte Internet-/Proxy-Zugang pruefen oder die Datei manuell im vorgesehenen Ordner ablegen.")
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
Write-Host 'Large Image Quality Enhancer - automatischer EXE-Bau'
Write-Host '----------------------------------------------------'
Write-Host 'Dieses Skript kann Python 3.12, Python-Bibliotheken und KI-Modelle herunterladen.'
Write-Host 'Python wird bei Bedarf nur fuer den aktuellen Benutzer eingerichtet.'
Write-Host 'Der PATH wird nicht geaendert; Administratorrechte sind normalerweise nicht noetig.'
Write-Host 'Die fertige EXE benoetigt anschliessend weder Python noch Internet.'
Write-Host ''
if ($root.Length -gt 95) {
    Write-Warning 'Sehr langer Verzeichnispfad. Bitte ggf. nach C:\LIQE entpacken.'
}
if (-not [Environment]::Is64BitOperatingSystem) { throw 'Windows 64 Bit wird benoetigt.' }

# An existing Python installation can be used; otherwise install into LocalAppData.
$usePython = ''
if (Test-Python312 $privatePython) {
    $usePython = $privatePython
    Write-Host 'Geeignete private Python-Installation bereits vorhanden.'
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    if (Test-Python312 'py' @('-3.12')) {
        Write-Host 'Python 3.12 ist bereits installiert. Keine Neuinstallation noetig.'
    }
}
if (-not $usePython) {
    $hasPy = $false
    if (Get-Command py -ErrorAction SilentlyContinue) {
        $hasPy = Test-Python312 'py' @('-3.12')
    }
    if (-not $hasPy) {
        Write-Host ''
        Write-Host 'Python 3.12 wird vom offiziellen python.org-Server geladen.'
        Write-Host 'Es wird lokal fuer den Benutzer installiert (ohne PATH-Aenderung).'
        $answer = Read-Host 'Python jetzt automatisch installieren? [J/n]'
        if ($answer -match '^[nN]') { throw 'Abbruch: Python 3.12 wird zum Erstellen einer EXE benoetigt.' }
        Fetch-File $pythonUrl $pythonInstaller 20000000
        $signature = Get-AuthenticodeSignature -LiteralPath $pythonInstaller
        if ($signature.Status -ne 'Valid' -or
            -not $signature.SignerCertificate -or
            $signature.SignerCertificate.Subject -notmatch 'Python Software Foundation') {
            throw 'Sicherheitspruefung fehlgeschlagen: Python-Installer hat keine gueltige PSF-Signatur.'
        }
        Write-Host 'Signatur des offiziellen Python-Installers geprueft.'
        New-Item -Path $privateDir -ItemType Directory -Force | Out-Null
        $args = ('/quiet InstallAllUsers=0 TargetDir="{0}" Include_pip=1 Include_tcltk=1 Include_dev=1 Include_launcher=0 Include_test=0 Include_doc=0 Shortcuts=0 AssociateFiles=0 PrependPath=0 AppendPath=0' -f $privateDir)
        $proc = Start-Process -FilePath $pythonInstaller -ArgumentList $args -Wait -PassThru
        if ($proc.ExitCode -ne 0 -or -not (Test-Python312 $privatePython)) {
            throw ("Die lokale Python-Installation ist fehlgeschlagen (Exit-Code " + $proc.ExitCode + "). Windows-Sicherheitsrichtlinien oder ein Proxy koennten den Installer blockieren.")
        }
        $usePython = $privatePython
        Write-Host 'Python wurde lokal eingerichtet.' -ForegroundColor Green
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
    Write-Host 'Die folgenden trainierten Modelle fehlen:'
    $missing | ForEach-Object { Write-Host (' - ' + $_.Name) }
    Write-Host 'Quellen: raspberrypi/AI_enhance (BSD-2-Clause), Heliosoph/scunet-onnx (Apache-2.0).'
    Write-Host 'Die Dateien sind urheberrechtlich fremd und unterliegen ihren eigenen Bedingungen.'
    Write-Host 'Informationen: THIRD_PARTY_NOTICES.md im Hauptverzeichnis des Repositories.'
    $consent = Read-Host 'Diese Modell-Dateien direkt beim jeweiligen Anbieter herunterladen? [J/n]'
    if ($consent -match '^[nN]') {
        throw 'Es fehlen KI-Modelle. Kopiere die drei Dateien manuell nach models und starte erneut.'
    }
    foreach ($model in $missing) {
        Fetch-File $model.Url (Join-Path $models $model.Name) $model.Min $model.Hash
    }
}
Write-Host 'Alle erforderlichen Modelle sind vorhanden.' -ForegroundColor Green

$builder = Join-Path $root 'BAUE_WINDOWS_EXE.ps1'
Write-Host ''
Write-Host 'Starte jetzt die EXE-Erstellung. Das kann mehrere Minuten dauern.'
if ($usePython) {
    & $builder -PythonExe $usePython
} else {
    & $builder
}
if ($LASTEXITCODE -ne 0) { throw ('EXE-Erstellung fehlgeschlagen (Exit-Code ' + $LASTEXITCODE + ').') }
Write-Host ''
Write-Host ('Fertig! Portable Anwendung: ' + (Join-Path $root 'dist\Insta360_X5_KI_Offline')) -ForegroundColor Green
Write-Host 'Der komplette dist-Unterordner muss auf den Ziel-PC kopiert werden.'
