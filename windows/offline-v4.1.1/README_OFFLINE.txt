INSTA360 X5 – OFFLINE KI-OPTIMIERER v4.1 (eigenstaendige EXE-Version)
================================================================

ZIEL
DPRNet + SCUNet, Vergleich, 360-Export, Stapelverarbeitung und Restzeit,
OHNE Internetverbindung auf dem Ziel-PC. Keine Proxy-/Zertifikatabfragen.
Die bisherige Python-Version 3.3 und die fruehere Proxy-Version bleiben unberuehrt.

AUTOMATISCHER WEG (AUCH OHNE VORHER INSTALLIERTES PYTHON)
1. GitHub-Repository herunterladen (Code -> Download ZIP), z. B. nach C:\LIQE entpacken.
2. In windows\offline-v4.1.1 die Datei ALLES_AUTOMATISCH_BAUEN.bat starten.
3. Den Download von Python 3.12 (falls nicht vorhanden) und den externen
   DPRNet-/SCUNet-Modellen bestaetigen. Die Lizenzbedingungen der Modelle gelten.
4. Das Skript laedt fehlende Dateien, richtet die Werkzeuge ein und startet
   automatisch den EXE-Bau. Ein Internetzugang ist dafuer beim ersten Mal erforderlich.
5. Die Ausgabe liegt unter dist\Insta360_X5_KI_Offline\.
   Den kompletten Ordner auf den Ziel-PC kopieren; dort ist kein Python noetig.

Python wird bei Bedarf lokal im Benutzerprofil installiert, nicht systemweit
und ohne PATH-Aenderung. Es ist damit keine Python-VORINSTALLATION noetig.
Das ist keine Garantie fuer Administratorfreiheit in verwalteten Firmen-PCs.
Der automatisierte Build muss noch auf einem frischen Windows-PC erprobt werden.
Bei Proxy-407-Fehlern oder Netzsperren ggf. Python und Modelle manuell beschaffen.
PowerShell prueft die digitale Signatur des Python-Installers; Zertifikats-
pruefungen werden nicht deaktiviert.

WICHTIG
Dieses Baupaket enthaelt noch KEINE fertige Windows-EXE und KEINE KI-Gewichte.
Beim MANUELLEN Bau muessen die Modelle als KOPIEN in models\ abgelegt werden.
Beim neuen automatischen Bau werden sie nach Zustimmung direkt geladen.

MODELLDATEIEN (aus deinem bereits funktionierenden v3.3-Ordner):
models\DPRNet_1024.tflite
models\scunet_color_real_psnr.onnx
models\scunet_color_real_psnr.onnx.data
Optional: models\DPRNet_512.tflite

Bitte kein altes SCUNet-.pth statt der .onnx/.onnx.data-Dateien verwenden.
Die Modelldateien werden im fertigen portablen Programmordner mitgefuehrt.
Auf dem Ziel-PC sucht die EXE sie ausschliesslich lokal im models-Ordner.

MANUELLES BAUEN AUF DEINEM WINDOWS-RECHNER (ALTERNATIVE)
1. Dieses ZIP in einen eigenen, NEUEN Ordner entpacken.
2. Die obigen Modell-Dateien aus dem bisherigen v3.3-Ordner in den NEUEN
   Unterordner models kopieren (NICHT verschieben).
3. Python 3.12 (64 Bit) auf dem BAU-Rechner bereitstellen:
   https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.exe
4. BAUE_WINDOWS_EXE.bat doppelt anklicken.
   - Das Skript prueft ZUERST alle Modell-Dateien.
   - Nur BEIM BAUEN werden Python-Pakete und PyInstaller benoetigt.
   - Bei Proxy-Problemen kannst du in der Build-Umgebung PIP_PROXY und
     PIP_CERT setzen, oder ein lokales Verzeichnis "wheelhouse" mit
     den passenden Windows-Python-3.12-x64-Wheel-Dateien fuellen.
   - Beim EXE-Bau werden KEINE Proxy/Zertifikat-Dialoge mehr abgefragt.
5. Die Ausgabe liegt im eigenen Ordner:
   dist\Insta360_X5_KI_Offline\Insta360_X5_KI_Offline.exe
6. Die ZIP-Datei Insta360_X5_KI_Offline_Portable.zip wird optional erstellt.

BETRIEB AUF EINEM ANDEREN PC OHNE INTERNET
- Den GESAMTEN Ordner dist\Insta360_X5_KI_Offline kopieren oder das
  fertige Portable-ZIP vollstaendig entpacken.
- Insta360_X5_KI_Offline.exe doppelt anklicken.
- WEDER Python NOCH Internet NOCH eine Proxy-/Zertifikatkonfiguration
  werden auf dem Ziel-PC benoetigt.
- Alle Bildverarbeitungsschritte erfolgen lokal; es gibt in dieser
  Programmversion KEINE Download- oder Netzwerkfunktionen.
- Die Modelle im Unterordner models nicht loeschen oder umbenennen.
- Bearbeitete Bilder werden lokal gespeichert. Bei optionalem Ueberschreiben
  kann eine Sicherungskopie erstellt werden.
- Den Programmordner am besten an einem Ort mit Schreibzugriff ablegen,
  z. B. D:\Apps\Insta360_X5_KI_Offline.

TECHNISCHE HINWEISE
- EXE und Bibliotheken sind fuer Windows 64 Bit konzipiert.
- Wie bisher erfolgt die Modellberechnung auf der CPU; Vollbild-SCUNet kann
  bei rund 71 MP sehr lange dauern.
- Das Baupaket wurde unter Linux statisch/simulierend getestet; der
  native Windows-Bau und die echte KI-Inferenz muessen auf Windows
  abschliessend getestet werden.
- Unternehmensrichtlinien koennen das Ausfuehren unbekannter, nicht signierter
  EXE-Dateien blockieren. Die EXE ist nicht digital signiert.

QUELLEN / MODELL-LIZENZEN
DPRNet: Raspberry Pi Ltd., AI_enhance, BSD-2-Clause
  https://github.com/raspberrypi/AI_enhance
SCUNet: Architektur https://github.com/cszn/SCUNet
  ONNX-Gewichte siehe Heliosoph/scunet-onnx (dessen Lizenz beachten)
Vor Weitergabe an andere Personen die jeweiligen Lizenzen pruefen.
