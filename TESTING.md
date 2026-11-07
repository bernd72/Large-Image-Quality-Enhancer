# Testing and compatibility / Tests und Kompatibilität

## Reported status / Bisheriger Stand

- **Camera / Kamera:** Insta360 X5 and a smartphone JPEG / Insta360 X5 und ein Smartphone-JPEG.
- **Input format / Eingabeformat:** JPEG only / ausschließlich JPEG.
- **Aspect-ratio fix in source / Korrektur der Seitenverhältnisse im Quellcode (2026-11-07):** Hard-coded 2:1 restrictions removed from both editions; geometry-preserving model input and non-wrapping photo denoising added. New regression tests cover 3:2, 4:3, square and portrait JPEGs with mock inference; **broader real-model verification pending** / Explizite 2:1-Sperren in beiden Quellcode-Ausgaben entfernt; geometrieerhaltende KI-Eingabe und passende Randbehandlung ergänzt. Regressionstests mit simulierten Modellen für 3:2, 4:3, quadratische und Hochformat-JPEGs ergänzt; **weitere Praxistests mit echten Modellen stehen noch aus**.
- **Reported tested image dimensions / Berichtete getestete Bildgröße:** 11,904 × 5,952 pixels, approx. 70.86 MP / 11.904 × 5.952 Pixel, ca. 70,86 MP.
- **Larger than 71 MP / Über 71 MP:** Not yet tested with the complete AI pipeline / Noch nicht mit der vollständigen KI-Verarbeitung getestet.
- **Other camera models / Andere Kameras:** One smartphone photo tested; others not verified / Ein Smartphone-Foto getestet; weitere Kameras nicht geprüft.
- **Other formats / Andere Formate:** Not yet verified / Noch nicht verifiziert.
- **Windows EXE on additional PCs / Windows-EXE auf weiteren PCs:** Reported working on a second and third PC, both running Windows 11 / Nach Angabe des Entwicklers auf einem zweiten und dritten PC unter Windows 11 erfolgreich getestet.
- **Exact tested EXE build / Genau getestete EXE-Version:** Not yet recorded / Noch nicht dokumentiert.
- **Disconnected operation / Betrieb ohne Netzwerk:** Existing Windows EXE reportedly runs without an internet connection; precise test conditions and build version not recorded / Vorhandene Windows-EXE läuft laut Entwickler ohne Internetverbindung; genaue Testbedingungen und Build-Version nicht dokumentiert.
- **Other Windows versions / Andere Windows-Versionen:** Not verified / Nicht verifiziert.
- **Long Windows directory paths / Lange Windows-Verzeichnispfade:** Problems reported during extraction or use from deeply nested folders; a short folder path is recommended; root cause unconfirmed / Probleme beim Entpacken oder Betrieb in tief verschachtelten Ordnern berichtet; kurzer Pfad empfohlen; genaue Ursache ungeklärt. See / Siehe [KNOWN_ISSUES.md](KNOWN_ISSUES.md).
- **Parallel runs / Gleichzeitige Instanzen:** Two on a computer with an Intel Core i5-14400; reportedly up to five or six on a stronger computer (developer experience, not a benchmark) / Zwei auf einem Rechner mit Intel Core i5-14400; nach Erfahrungswerten bis zu fünf oder sechs auf leistungsfähigerem Rechner (keine Benchmarkmessung).

- **Reported time per complete image / Berichtete Zeit pro vollständig verarbeitetem Bild:** Approx. **45–50 minutes** for an Insta360 X5 JPEG image (~71 MP) on an **Intel Core i5-14400**, per developer experience / Ca. **45–50 Minuten** für ein Insta360-X5-JPEG (~71 MP) auf einem **Intel Core i5-14400**, laut Entwicklererfahrung.

These entries reflect the **previously reported development tests**, including Windows 11 tests on two additional PCs, not reproducible tests executed in this GitHub repository. The processing time above is an approximate user-reported observation, not a standardized benchmark. No verified memory ceiling or supported maximum resolution is claimed.

Diese Angaben beruhen auf **bisher berichteten Entwicklungstests**, darunter Windows-11-Tests auf zwei weiteren PCs, nicht auf in diesem Repository reproduzierten Messungen. Die oben genannte Bearbeitungszeit ist ein ungefährer Praxiswert, kein standardisierter Benchmark. Es gibt derzeit keine belegte maximale Auflösung oder garantierte Speicheranforderung.

## Latest developer feedback / Aktueller Praxistest

- **2026-11-07, Windows 11:** Single-image and batch processing reportedly work; tested with a smartphone JPEG (3246 × 2448 px, approximately 4:3) / Einzelbild- und Stapelverarbeitung funktionieren laut Rückmeldung; getestet mit einem Smartphone-JPEG (3246 × 2448 Pixel, ungefähr 4:3).
- **Open / Offen:** Language switch and Python edition not yet practically confirmed / Sprachumschaltung und Python-Version noch nicht praktisch bestätigt.

## Python v3.3 GUI language selector / Python-v3.3-Sprachumschaltung

- **Implemented / Eingebaut:** A live Deutsch/English selector was added to the Python v3.3 Tkinter GUI, including its model-download buttons and batch dialog / Deutsch-Englisch-Umschaltung in der Python-v3.3-Oberfläche einschließlich Modell-Downloads und Stapeldialog.
- **Translation tests / Übersetzungstests:** Dedicated dependency-free test cases are provided in [`python/v3.3/tests/test_i18n.py`](python/v3.3/tests/test_i18n.py). Translation mappings were checked statically / Eigenständige Tests für die Übersetzungstexte sind vorhanden; die Zuordnungen wurden statisch abgeglichen.
- **Still pending / Noch offen:** Native Windows GUI test, Python startup with local models, and end-to-end image processing have **not** been verified for this change / Windows-GUI, Start mit lokalen Modellen und vollständiger Bildverarbeitungslauf wurden für diese Änderung **noch nicht** praktisch getestet.

## GUI language selector / Sprachauswahl der Oberfläche

- **Implementation / Umsetzung:** The Windows v4.1.1 source now includes an offline German/English selector that updates interface labels and dialog text without restarting / Der Windows-v4.1.1-Quellcode enthält jetzt eine Offline-Umschaltung Deutsch/Englisch, die Oberfläche und Dialogtexte ohne Neustart aktualisiert.
- **Verification / Teststand:** Code and translation entries reviewed statically; on 2026-11-07 the developer reported an ongoing, apparently successful Windows 11 application test, but the language switch, exact build and full processing have **not yet been separately confirmed** / Code und Übersetzungseinträge statisch geprüft; am 07.11.2026 meldete der Entwickler einen laufenden, vorläufig positiv verlaufenden Anwendungstest unter Windows 11. Sprachwechsel, genaue Build-Version und vollständige Verarbeitung sind **noch nicht gesondert bestätigt**.
- **Existing EXEs / Bestehende EXE-Dateien:** Rebuild required / Neubau erforderlich.

## Parallel-instance test guidance / Hinweise zu Tests mit mehreren Instanzen

Reported concurrent use is **not** a guaranteed capacity or a measured throughput improvement. Practical limits depend on CPU, RAM, storage I/O, image sizes and model runtime. Record peak RAM, CPU utilization, elapsed time, and any failures for one, two and higher instance counts.

Die gemeldete parallele Nutzung ist **keine** garantierte Kapazität oder gemessene Beschleunigung. Die Anzahl sinnvoller Instanzen hängt von CPU, RAM, Massenspeicher und Bild- bzw. Modelllast ab. Bei künftigen Tests bitte CPU-Auslastung, maximalen Arbeitsspeicher, Gesamtlaufzeit und Fehler bei einer, zwei und mehr Instanzen erfassen.

## Source review: image validation / Quellcode-Prüfung: Eingabevalidierung

The current Python v3.3 and Windows v4.1.1 entry points set `Image.MAX_IMAGE_PIXELS = None`. This allows very large images, but disables Pillow's default decompression-bomb size safeguard. It is **not** a measured failure in existing tests. Until appropriate explicit pixel/memory validation is implemented, test with trusted inputs only. See [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

Die aktuellen Python-Einstiegspunkte in v3.3 und Windows v4.1.1 setzen `Image.MAX_IMAGE_PIXELS = None`. Damit lassen sich große Bilder öffnen, aber Pillow prüft die Bildgröße nicht mehr standardmäßig auf ungewöhnlich hohe Speicheranforderungen. Das ist **kein** nachgewiesener Fehler bei den bisherigen Bildern. Bis zu einer eigenen Eingabeprüfung nur vertrauenswürdige Bilder verwenden.

## Planned large-image stress test / Geplanter Belastungstest

Target sizes / Zielgrößen: **100 MP, 200 MP and 500 MP**. For future reproducible tests with the published source, record:

1. exact image dimensions and file type / Auflösung und Dateiformat;
2. software version, model versions and hashes / Programm- und Modellversionen;
3. CPU, RAM, Windows/Python details / Hardware und Umgebung;
4. runtime, peak RAM and storage usage / Laufzeit und maximalen Speicherbedarf;
5. output correctness and visible tile seams / Ergebnisqualität und Kachelgrenzen;
6. crash logs and reproducible steps / Fehlerprotokolle und Wiederholungsschritte.

**Safety / Sicherheit:** Start from copies of test images, protect originals, and check enough free disk space. Pillow's decompression-bomb safeguards must not be disabled globally without a considered input-validation and memory policy.

Testing results should be added here with dates and reproducible parameters; do not substitute estimates for completed measurements.
