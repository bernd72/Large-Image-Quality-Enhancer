# Contributing / Mitmachen

## Deutsch

Danke für deine Mitarbeit an **Large Image Quality Enhancer**!

**Projektstand:** Der Quellcode der Python-Version 3.3 liegt unter [`python/v3.3`](python/v3.3/), die Bauskripte der Windows-Version 4.1.1 unter [`windows/offline-v4.1.1`](windows/offline-v4.1.1/). Fertige EXE-Dateien und KI-Modellgewichte werden nicht bereitgestellt. Die portable Windows-Anwendung wurde laut Entwickler auf einem sauberen Windows-11-PC getestet; der automatische EXE-Bau ist noch nicht unabhängig auf einer frischen Windows-Installation überprüft.

### So kannst du helfen

- Melde Fehler, Ideen, Dokumentationsfehler oder Kameratests als GitHub-Issue.
- Reiche Codeänderungen über einen eigenen Branch und Pull Request ein, möglichst mit Testhinweisen.
- Gib bei Fehlermeldungen Bildgröße, Dateiformat, Kamera, Programmversion, Betriebssystem und Fehlertext an.
- Lade keine privaten Fotos, Zugangsdaten, Zertifikate oder Modellgewichte ohne geklärte Weitergaberechte hoch.
- Reiche nur Beiträge ein, die du unter der MIT-Lizenz freigeben darfst, und erhalte Hinweise zu Fremdlizenzen.
- Bleibe sachlich und belege technische Probleme möglichst nachvollziehbar.

### Nächste Aufgaben

1. Python-Version 3.3 prüfen und verbessern, ohne eine funktionierende Version zu beeinträchtigen.
2. Den **automatischen EXE-Bau** auf einer frisch installierten Windows-Umgebung unabhängig testen; die **portable Anwendung** wurde bereits unter Windows 11 getestet.
3. Herkunft, Lizenzen und genaue Dateien der KI-Modelle vor einer Veröffentlichung prüfen.
4. Reproduzierbare JPEG-Tests und Belastungstests mit 100, 200 und 500 MP ergänzen.
5. Die portable Anwendung auf weiteren Windows-Versionen testen und Ergebnisse dokumentieren.
6. Weitere Kameras und Bildformate praktisch testen und nur bestätigte Ergebnisse dokumentieren.

## English

Thank you for contributing to **Large Image Quality Enhancer**!

**Current status:** Python v3.3 source is available in [`python/v3.3`](python/v3.3/), and Windows v4.1.1 build scripts are in [`windows/offline-v4.1.1`](windows/offline-v4.1.1/). Compiled EXEs and AI model weights are not distributed. The developer reports successful testing of the portable application on a clean Windows 11 PC; the automated EXE build has not yet been independently verified on a fresh Windows installation.

### How to contribute

- Open a GitHub Issue for bugs, feature ideas, documentation corrections, or camera compatibility reports.
- Use a separate branch and a Pull Request for code changes, with test instructions where possible.
- Include image resolution, file format, camera, software version, operating system, and error messages in bug reports.
- Do not upload private photos, credentials, certificates, or model weights without confirmed redistribution rights.
- Submit only contributions you may license under MIT, and preserve third-party notices.
- Be respectful, focus on technical issues, and provide reproducible evidence where possible.

### Priority work

1. Review and improve Python v3.3 without disrupting a working version.
2. Independently test the **automated EXE build** on a fresh Windows installation; the **portable application** has already been tested on Windows 11.
3. Verify model provenance, licenses, and exact artifacts before any model release.
4. Add reproducible JPEG tests and stress tests at 100, 200, and 500 MP.
5. Test the portable application on additional Windows versions and document results.
6. Test more cameras and image formats in practice; document only verified results.
