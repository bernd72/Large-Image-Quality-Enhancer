# Tests und Kompatibilität / Testing and compatibility

## Deutsch

### Bisheriger Teststand

- **Kameras und Dateiformat:** Insta360 X5 und ein Smartphone; bislang JPEG.
- **Bildgrößen:** Insta360 X5 mit 11.904 × 5.952 Pixeln (ca. 70,86 MP) und Smartphone-Foto mit 3.246 × 2.448 Pixeln (ca. 4:3) getestet.
- **Windows 11:** Die portable EXE wurde laut Entwickler auch auf einem zweiten und dritten PC erfolgreich verwendet. Einzelbild- und Stapelverarbeitung funktionieren laut Rückmeldung vom 07.11.2026 auch mit einem Smartphone-Foto.
- **Offlinebetrieb:** Die bereits lauffähige Windows-EXE funktioniert laut Rückmeldung ohne Internet. Genaue Testbedingungen und EXE-Buildnummer sind nicht dokumentiert.
- **Noch offen:** Weitere Kameras und Dateiformate, Bilder über 71 MP mit vollständiger KI-Verarbeitung sowie andere Windows-Versionen sind nicht ausreichend geprüft.
- **Verzeichnispfade:** Bei tief verschachtelten Windows-Ordnern wurden Probleme berichtet. Kurze Pfade empfohlen; Ursache noch unklar. Siehe [KNOWN_ISSUES.md](KNOWN_ISSUES.md).
- **Gleichzeitige Instanzen:** Zwei auf einem Intel Core i5-14400; auf einem leistungsfähigeren PC laut Erfahrungsbericht bis zu fünf oder sechs. Keine Benchmarkmessung.
- **Laufzeit:** Ein vollständiges Insta360-X5-JPEG mit rund 71 MP benötigte laut Entwickler auf einem Intel Core i5-14400 ungefähr **45–50 Minuten**. Kein standardisierter Benchmark.

Diese Angaben beruhen auf berichteten Praxistests, nicht auf reproduzierbaren Messungen innerhalb des Repositories. Eine garantierte maximale Bildauflösung oder Speicherobergrenze ist nicht ermittelt.

### Seitenverhältnisse und Sprachumschaltung

- **Seitenverhältnisse:** Die feste 2:1-Beschränkung wurde am 07.11.2026 im Quellcode beider Versionen entfernt. Die Bildgeometrie und die Randbehandlung bei normalen Fotos wurden angepasst. Regressionstests mit simulierter KI-Verarbeitung decken 3:2, 4:3, quadratische und Hochformat-JPEGs ab; weitere vollständige Praxistests mit echten Modellen stehen aus.
- **Windows v4.1.1:** Im Quellcode ist eine offline nutzbare Deutsch-Englisch-Umschaltung ohne Neustart enthalten. Die Bildverarbeitung mit einem 4:3-Smartphone-Foto wurde unter Windows 11 positiv berichtet; die Sprachumschaltung wurde noch nicht ausdrücklich bestätigt. Für Quellcodeänderungen muss eine bestehende EXE neu gebaut werden.
- **Python v3.3:** Sprachumschaltung in der Tkinter-Oberfläche einschließlich Modell-Downloads und Stapeldialog umgesetzt. Übersetzungszuordnungen statisch geprüft; Tests unter [`python/v3.3/tests/test_i18n.py`](python/v3.3/tests/test_i18n.py). Praktische Tests der Windows-GUI, des Starts mit lokalen Modellen und der vollständigen Bildverarbeitung stehen noch aus.

### Hinweise für weitere Tests

**Parallele Verarbeitung:** Die gemeldete Anzahl gleichzeitig laufender Instanzen ist keine garantierte Kapazität. Grenzen hängen von CPU, RAM, Datenträger, Bildgröße und Modellen ab. Bei Tests mit einer, zwei oder mehr Instanzen CPU-Last, Spitzen-RAM, Laufzeit und Fehler erfassen.

**Sicherheit großer Bilddateien:** Die Einstiegspunkte von Python v3.3 und Windows v4.1.1 setzen `Image.MAX_IMAGE_PIXELS = None`. Damit entfällt die standardmäßige Schutzprüfung von Pillow gegen extrem große Bilder. Das ist kein nachgewiesener Fehler in bisherigen Tests. Bis zur Einführung einer eigenen Größen- und Speicherprüfung nur vertrauenswürdige Eingabedateien verwenden; siehe [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

**Geplanter Belastungstest:** 100 MP, 200 MP und 500 MP. Für nachvollziehbare Ergebnisse bitte Bildmaße und Dateityp, Programm- und Modellversionen (mit Hashes), CPU/RAM/Windows/Python, Laufzeit und Speicherspitzen, Ergebnisqualität einschließlich Kachelgrenzen sowie Fehlerprotokolle dokumentieren. Mit Kopien arbeiten, Originale schützen und ausreichend freien Speicher vorsehen. Die Pillow-Schutzprüfung sollte nicht ohne angemessene alternative Eingabe- und Speicherbegrenzung deaktiviert werden. Schätzungen nicht als durchgeführte Tests ausgeben.

---

## English

### Reported test status

- **Cameras and input format:** Insta360 X5 and one smartphone; JPEG so far.
- **Image sizes:** Insta360 X5 at 11,904 × 5,952 pixels (approx. 70.86 MP) and a smartphone photo at 3,246 × 2,448 pixels (approx. 4:3).
- **Windows 11:** According to the developer, the portable EXE also worked on a second and third PC. Single-image and batch processing reportedly worked with a smartphone photo on November 7, 2026.
- **Offline use:** An existing working Windows EXE reportedly runs without an internet connection. Exact test conditions and EXE build number were not recorded.
- **Still open:** Other cameras and file formats, images above 71 MP using the complete AI pipeline, and other Windows versions have not been sufficiently verified.
- **Directory paths:** Problems were reported with deeply nested Windows folders. Short paths are recommended; the cause remains unknown. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).
- **Concurrent instances:** Two on an Intel Core i5-14400; reportedly up to five or six on a stronger PC. Not a benchmark.
- **Processing time:** A complete Insta360 X5 JPEG of about 71 MP reportedly took **45–50 minutes** on an Intel Core i5-14400. Not a standardized benchmark.

These are developer-reported practical observations, not reproducible measurements carried out in this repository. No guaranteed maximum resolution or memory ceiling has been established.

### Aspect ratios and language selection

- **Aspect ratios:** The hard-coded 2:1 restriction was removed from both source editions on November 7, 2026. Image geometry and edge handling for ordinary photos were updated. Mock-inference regression tests cover 3:2, 4:3, square and portrait JPEGs; broader end-to-end testing with real models is still pending.
- **Windows v4.1.1:** The source includes an offline German/English selector that updates the UI without restarting. Processing a 4:3 smartphone photo on Windows 11 was reported successful; language switching has not been explicitly confirmed. Existing EXEs must be rebuilt to incorporate source changes.
- **Python v3.3:** Language selection was added to the Tkinter UI, including model downloads and the batch dialog. Translation mappings were statically checked; see [`python/v3.3/tests/test_i18n.py`](python/v3.3/tests/test_i18n.py). Native Windows GUI tests, startup with local models, and complete image processing remain unverified for this update.

### Guidance for further tests

**Parallel processing:** Reported instance counts do not establish guaranteed capacity. Limits depend on CPU, RAM, storage I/O, image dimensions and model runtimes. For one, two and more instances, record CPU usage, peak RAM, elapsed time and failures.

**Large-image safety:** Python v3.3 and Windows v4.1.1 entry points set `Image.MAX_IMAGE_PIXELS = None`, disabling Pillow's standard oversized-image safeguard. This is not a confirmed failure in previous tests. Until explicit image-size and memory validation is implemented, use trusted inputs only; see [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

**Planned stress tests:** 100 MP, 200 MP and 500 MP. For reproducible results, record image dimensions and format, software and model versions (including hashes), CPU/RAM/Windows/Python environment, runtime and peak resource usage, output quality including tile seams, and failure logs. Work from copies, protect originals and ensure sufficient disk space. Do not disable Pillow's safeguard without an appropriate alternative input-validation and memory policy. Do not present estimates as completed tests.
