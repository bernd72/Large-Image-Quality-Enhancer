# Known issues and limitations / Bekannte Fehler und Einschränkungen

## Deutsch

### Seitenverhältnis 2:1: Fehler im Quellcode behoben, Windows-EXE noch ungetestet

**Ursache ermittelt (07.11.2026):** Der Export und die Stapelverarbeitung enthielten ausdrückliche 2:1-Prüfungen. Auch die SCUNet-Rauschunterdrückung setzte Panorama-Randbedingungen voraus. Diese Sperren wurden in **Windows v4.1.1 und Python v3.3** aus dem Quellcode entfernt. Die DPRNet-Vorbereitung erhält bei normalen Fotos das Seitenverhältnis durch Einpassen mit Randpixeln, entfernt anschließend die Ränder aus dem Korrekturfeld und behält die native Ausgabegröße bei.

**Status:** Für 3:2-, 4:3-, quadratische und Hochformat-JPEGs stehen neue Regressionstests mit simulierten Modellaufrufen im Repository. Ein vollständiger Test mit echten KI-Modellgewichten bzw. einer neu gebauten Windows-EXE ist **noch offen**. Frühere EXE-Dateien enthalten die Behebung nicht; bitte neu bauen. Es werden weiterhin nur JPG/JPEG als Eingaben angeboten. 2:1-Panoramen behalten die spezielle Nahtbehandlung.


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

### Aspect ratio 2:1: source-code issue fixed; updated Windows EXE not yet tested

**Root cause identified (2026-11-07):** Export and batch paths contained explicit 2:1 restrictions, and SCUNet used panorama-specific horizontal wrapping. These constraints have been removed in the **Windows v4.1.1 and Python v3.3 source code**. For ordinary photos, DPRNet input uses aspect-preserving fitting with replicated edge padding, then crops the resulting gain field back to the photo area; the exported image retains the input pixel dimensions.

**Verification still needed:** Mock-model regression tests have been added for 3:2, 4:3, square and portrait JPEGs. A full run with actual model weights and a rebuilt Windows EXE **has not been verified**. Existing EXE builds must be rebuilt. Input remains JPEG/JPG; 2:1 panoramas retain special seam handling.


### Windows edition: problems with long directory paths

**Observation:** According to developer testing, the Windows executable works on Windows 11 **without an internet connection**. However, problems were encountered when extracting or running the application from a deeply nested directory. Long paths within the application folder may interfere with its operation.

**Workaround:** Extract the application to a short folder path and run it from there, for example `C:\LIQE\` or `C:\ImageEnhancer\`. Avoid deeply nested directories.

**Status:** Known limitation reported by the developer. The root cause, any exact path-length threshold, and the affected files have not yet been systematically determined. Windows path-length restrictions are one possibility, but that has not been confirmed. Reliable operation from arbitrary directory depths is therefore not guaranteed.

Offline operation refers to **running an existing, working Windows executable**. Setting up the development environment or building the EXE may still require internet access.

### Security: very large or untrusted images

**Source-code observation:** Python v3.3 and Windows v4.1.1 both set `Image.MAX_IMAGE_PIXELS = None`, disabling Pillow's normal oversized/decompression-bomb image check. This is **not a confirmed failure on the tested X5 JPEGs**, but may expose the application to excessive resource consumption when processing unknown or crafted images. **Workaround:** only process trusted JPEGs until explicit input-size and resource limits are implemented.

### Third-party download integrity

The automatic Windows build script checks the minimum sizes of the required model files, but has a fixed SHA-256 check only for `scunet_color_real_psnr.onnx`. The DPRNet TFLite file and SCUNet external `.onnx.data` weights are not yet hash-pinned. Confirm the source, rights, and integrity of model artifacts independently; see [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
