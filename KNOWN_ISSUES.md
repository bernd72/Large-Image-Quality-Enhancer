# Known issues and limitations / Bekannte Fehler und Einschränkungen

## Deutsch

### Windows-Version: Probleme bei langen Verzeichnispfaden

**Beobachtung:** Die Windows-EXE funktioniert nach Angaben des Entwicklers unter Windows 11 auch vollständig **ohne Internetverbindung**. Beim Entpacken oder Ausführen aus einem tief verschachtelten Verzeichnis kam es allerdings zu Problemen. Lange Pfade innerhalb des Installationsordners können die Nutzung beeinträchtigen.

**Vorläufige Lösung:** Das Programm in einen Ordner mit kurzem Pfad entpacken und von dort starten, zum Beispiel `C:\LIQE\` oder `C:\ImageEnhancer\`. Sehr tief verschachtelte Unterordner vermeiden.

**Status:** Bekannte, vom Entwickler berichtete Einschränkung. Die genaue Ursache, eine mögliche Pfadlängengrenze und die betroffenen Dateien wurden noch nicht systematisch untersucht. Ein Zusammenhang mit Windows-Pfadlängenbegrenzungen ist möglich, aber noch nicht bestätigt. Die korrekte Funktion bei beliebigen Verzeichnispfaden kann daher derzeit nicht zugesichert werden.

Der Offlinebetrieb bezieht sich auf die **Nutzung einer bereits lauffähigen Windows-EXE**. Das Einrichten der Entwicklungsumgebung oder Erstellen der EXE kann Internetzugang erfordern.

### Sicherheitsaspekt: große und fremde Bilddateien

**Beobachtung im Quellcode:** Die Python-Versionen 3.3 und Windows v4.1.1 setzen `Image.MAX_IMAGE_PIXELS = None`. Dadurch wird die standardmäßige Schutzprüfung von Pillow gegen ungewöhnlich große/dekomprimiert sehr speicherintensive Bilddateien ausgeschaltet. Das ist **kein bestätigter Absturz bei den bisher getesteten Insta360-X5-Fotos**, aber ein vermeidbares Risiko bei unbekannten oder manipulierten Eingabebildern.

**Bis zur Fehlerbehebung:** Nur vertrauenswürdige JPEG-Dateien verarbeiten. Künftig sollten sichere, ausdrücklich dokumentierte Grenzwerte für Pixelzahl, Dateigröße und Arbeitsspeicher umgesetzt werden, ohne große Panoramen pauschal auszuschließen.

### Prüfungen externer Modelldownloads

Das automatische Windows-Bauskript kontrolliert die Dateigrößen, aber aktuell nur für `scunet_color_real_psnr.onnx` auch eine feste SHA-256-Prüfsumme. Für `DPRNet_1024.tflite` und `scunet_color_real_psnr.onnx.data` fehlt noch eine fest hinterlegte Prüfsumme. Daher ist die vollständige Integrität aller heruntergeladenen Modellgewichte noch nicht kryptografisch abgesichert. Die genaue Herkunft und Lizenz jeder Modelldatei sind zusätzlich zu prüfen. Siehe [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## English

### Windows edition: problems with long directory paths

**Observation:** According to developer testing, the Windows executable works on Windows 11 **without an internet connection**. However, problems were encountered when extracting or running the application from a deeply nested directory. Long paths within the application folder may interfere with its operation.

**Workaround:** Extract the application to a short folder path and run it from there, for example `C:\LIQE\` or `C:\ImageEnhancer\`. Avoid deeply nested directories.

**Status:** Known limitation reported by the developer. The root cause, any exact path-length threshold, and the affected files have not yet been systematically determined. Windows path-length restrictions are one possibility, but that has not been confirmed. Reliable operation from arbitrary directory depths is therefore not guaranteed.

Offline operation refers to **running an existing, working Windows executable**. Setting up the development environment or building the EXE may still require internet access.

### Security: very large or untrusted images

**Source-code observation:** Python v3.3 and Windows v4.1.1 both set `Image.MAX_IMAGE_PIXELS = None`, disabling Pillow's normal oversized/decompression-bomb image check. This is **not a confirmed failure on the tested X5 JPEGs**, but may expose the application to excessive resource consumption when processing unknown or crafted images. **Workaround:** only process trusted JPEGs until explicit input-size and resource limits are implemented.

### Third-party download integrity

The automatic Windows build script checks the minimum sizes of the required model files, but has a fixed SHA-256 check only for `scunet_color_real_psnr.onnx`. The DPRNet TFLite file and SCUNet external `.onnx.data` weights are not yet hash-pinned. Confirm the source, rights, and integrity of model artifacts independently; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
