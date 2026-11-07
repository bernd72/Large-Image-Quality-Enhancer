# Contributing / Mitmachen

Thank you for helping build **Large Image Quality Enhancer**. / Danke für deine Mitarbeit!

**Current status:** Python v3.3 source and Windows v4.1.1 build scripts are available under [`python/v3.3`](python/v3.3/) and [`windows/offline-v4.1.1`](windows/offline-v4.1.1/). Compiled binaries and model weights are not distributed, and the Windows build has not been independently verified here. / Quellcode und Bauskripte vorhanden; fertige EXE und Modellgewichte sind nicht veröffentlicht.

## How to contribute / So kannst du helfen

- Open an **Issue** for a bug, feature idea, documentation correction or camera compatibility report. / Melde Fehler, Ideen oder Kameratests als Issue.
- For code changes, use a separate branch and submit a **Pull Request** with a clear description and, when possible, test instructions. / Für Codeänderungen bitte einen eigenen Branch und Pull Request verwenden.
- Include image resolution, file format, camera, software version, operating system, and any relevant error message in reports. / Bitte Bildgröße, Dateiformat, Kamera, Programmversion, Betriebssystem und Fehlermeldungen nennen.
- Do not upload private photographs, secrets, private certificates, proxy credentials, or third-party model files without confirmed redistribution rights. / Keine privaten Fotos, Zugangsdaten, Zertifikate oder ungeprüfte Modellgewichte hochladen.
- Only submit contributions you are entitled to license under **MIT**, and preserve all upstream notices for third-party work. / Nur Beiträge einreichen, die du unter MIT freigeben darfst; Fremdlizenzen erhalten.
- Be respectful, focus on technical issues, and provide reproducible evidence. / Bitte sachlich und respektvoll zusammenarbeiten.

## Priority work / Nächste Aufgaben

1. Review and improve the published Python v3.3 code while preserving a working version.
2. Independently verify the **automated EXE build process** on a fresh Windows installation; the developer has already tested the **portable Windows application** on a clean Windows 11 PC.
3. Verify model provenance, licenses, and exact binaries before any model release.
4. Add reproducible JPEG tests and stress tests at 100/200/500 MP.
5. Extend portable EXE compatibility testing beyond Windows 11 and record reproducible test details; clean-machine use under Windows 11 has already been reported.
6. Extend real-world testing to more cameras and image formats; document only verified results.
