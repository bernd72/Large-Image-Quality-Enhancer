# Testing and compatibility / Tests und Kompatibilität

## Reported status / Bisheriger Stand

- **Camera / Kamera:** Insta360 X5 only / ausschließlich Insta360 X5.
- **Input format / Eingabeformat:** JPEG only / ausschließlich JPEG.
- **Reported tested image dimensions / Berichtete getestete Bildgröße:** 11,904 × 5,952 pixels, approx. 70.86 MP / 11.904 × 5.952 Pixel, ca. 70,86 MP.
- **Larger than 71 MP / Über 71 MP:** Not yet tested with the complete AI pipeline / Noch nicht mit der vollständigen KI-Verarbeitung getestet.
- **Other camera models / Andere Kameras:** Not yet verified / Noch nicht verifiziert.
- **Other formats / Andere Formate:** Not yet verified / Noch nicht verifiziert.
- **Offline Windows EXE on a second PC / Offline-EXE auf zweitem PC:** Not yet verified / Noch nicht verifiziert.

These entries reflect the **previously reported development tests**, not reproducible tests executed in this GitHub repository. No benchmark results, processing time, memory ceiling, or supported maximum resolution are currently claimed.

Diese Angaben beruhen auf **bisher berichteten Entwicklungstests**, nicht auf in diesem Repository reproduzierten Messungen. Es gibt derzeit keine belegte maximale Auflösung oder garantierte Speicheranforderung.

## Planned large-image stress test / Geplanter Belastungstest

Target sizes / Zielgrößen: **100 MP, 200 MP and 500 MP**. When working code becomes available, record:

1. exact image dimensions and file type / Auflösung und Dateiformat;
2. software version, model versions and hashes / Programm- und Modellversionen;
3. CPU, RAM, Windows/Python details / Hardware und Umgebung;
4. runtime, peak RAM and storage usage / Laufzeit und maximalen Speicherbedarf;
5. output correctness and visible tile seams / Ergebnisqualität und Kachelgrenzen;
6. crash logs and reproducible steps / Fehlerprotokolle und Wiederholungsschritte.

**Safety / Sicherheit:** Start from copies of test images, protect originals, and check enough free disk space. Pillow's decompression-bomb safeguards must not be disabled globally without a considered input-validation and memory policy.

Testing results should be added here with dates and reproducible parameters; do not substitute estimates for completed measurements.
