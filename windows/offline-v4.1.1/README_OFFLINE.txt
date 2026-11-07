INSTA360 X5 – OFFLINE KI-OPTIMIERER v4.1.1 (eigenstaendige EXE-Version)
================================================================

ZIEL
DPRNet + SCUNet, Vergleich, 360-Export, Stapelverarbeitung und Restzeit,
OHNE Internetverbindung auf dem Ziel-PC. Keine Proxy-/Zertifikatabfragen.
Die bisherige Python-Version 3.3 und die fruehere Proxy-Version bleiben unberuehrt.

BILDFORMATE (QUELLCODESTAND 07.11.2026)
Die harte 2:1-Beschraenkung ist im Quellcode entfernt.
Auch uebliche JPG-Fotos in 4:3, 3:2, quadratisch und Hochformat sind
jetzt fuer Einzelbild- und Stapelverarbeitung vorgesehen.
Die Aufloesung und das Seitenverhaeltnis der Ausgabedatei bleiben erhalten.
Fuer 2:1-Panoramen bleibt die spezielle Rand-/Nahtbehandlung erhalten.
Der neue Bildformat-Code ist mit echten KI-Modellen und Windows 11 noch
nicht vollstaendig getestet. Bestehende EXE-Dateien enthalten die Aenderung
erst nach einem vollstaendigen Neubau mit den aktualisierten Quellen.
Eingaben bleiben JPG/JPEG; HEIC, RAW und PNG sind nicht direkt unterstuetzt.

HINWEIS ZUR SPRACHE DES BAUPROGRAMMS
Die Startdatei AUTO_BUILD_WINDOWS_EXE.bat sowie die Meldungen und Rueckfragen
beim automatischen Bau sind nun auf Englisch. Die fertige Anwendung hat davon
unabhaengig eine Deutsch/Englisch-Umschaltung in der grafischen Oberflaeche.
Der englische Bauablauf wurde noch nicht auf englischem Windows erprobt.

AUTOMATISCHER WEG (AUCH OHNE VORHER INSTALLIERTES PYTHON)
1. GitHub-Repository herunterladen (Code -> Download ZIP), z. B. nach C:\LIQE entpacken.
2. In windows\offline-v4.1.1 die Datei AUTO_BUILD_WINDOWS_EXE.bat starten.
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

SPRACHE DER PROGRAMMOBERFLAECHE (NEU IM AKTUELLEN QUELLCODE)
- Oben im Programmfenster gibt es die Auswahl Sprache / Language.
- Hier kann zwischen Deutsch und English ohne Neustart umgeschaltet werden.
- Die Uebersetzungen sind offline enthalten; kein Download noetig.
- Bereits zuvor erstellte EXE-Dateien muessen mit dem aktualisierten Quellcode
  neu gebaut werden, damit die Sprachauswahl vorhanden ist.
- Diese GUI-Aenderung wurde noch nicht unter Windows praktisch erprobt.

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
- Bekannter Fehler laut Entwicklertests: Die Bildverarbeitung funktioniert derzeit
  nur bei einem Breiten-Hoehen-Verhaeltnis von 2:1 (z. B. 11904 x 5952).
  Bei anderen Seitenverhaeltnissen tritt eine Fehlermeldung auf - sowohl
  bei Einzelbildern als auch in der Stapelverarbeitung. Ursache noch offen.
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

SICHERHEIT / NOCH OFFENE PRUEFUNGEN
- Im Quellcode steht Image.MAX_IMAGE_PIXELS = None. Dadurch entfällt die
  Pillow-Schutzpruefung fuer extrem grosse / manipulierte Bilddateien.
  Bis zu einer eigenen Eingabevalidierung nur vertraute JPEGs verarbeiten.
- Das automatische Skript prueft die Groesse aller Modelldateien. Eine feste
  SHA-256-Pruefsumme ist derzeit nur fuer das SCUNet-ONNX-Hauptmodell hinterlegt,
  nicht fuer DPRNet und die SCUNet-.onnx.data-Datei.
- Die SCUNet-ONNX-Konvertierung wird beim automatischen Bau von Heliosoph auf
  Hugging Face heruntergeladen, nicht unmittelbar vom urspruenglichen
  SCUNet-Projekt. Modell-Lizenz und Weitergaberechte individuell pruefen.
- Das gesamte Build-Skript wurde noch nicht auf einem frischen Windows-11-PC
  praktisch durchgetestet. Keine Funktionsgarantie fuer diesen Buildpfad.
