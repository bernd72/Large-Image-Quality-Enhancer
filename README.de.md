# Large Image Quality Enhancer

**Open-Source-Software zur KI-gestützten Qualitätsverbesserung großer, hochauflösender Fotos.**

[English](README.md) · [Mitarbeit / Contributing](CONTRIBUTING.md) · [Fremdlizenzen](THIRD_PARTY_NOTICES.md) · [Teststand](TESTING.md)

> **Projektaufbau / noch keine Veröffentlichung der Software.** Dieses Repository enthält derzeit nur Dokumentation. Die vorhandenen Python- und Windows-Programmdateien, KI-Modelle und die Windows-EXE wurden noch nicht hochgeladen oder vollständig für eine öffentliche Weitergabe geprüft.

## Ziel

Die Bildqualität soll verbessert werden, **nicht die Bildauflösung vergrößert**. Die bisherige Entwicklung konzentriert sich auf Aufhellung dunkler Bereiche, Rauschreduzierung und Stapelverarbeitung hochauflösender Fotos. Eine Python-Ausgabe und eine offline verwendbare Windows-Ausgabe sind vorgesehen.

## Kompatibilität und Teststand

**Bisher wurde die Software ausschließlich mit JPEG-Aufnahmen einer Insta360 X5 bis etwa 71 Megapixel (11.904 × 5.952 Pixel) getestet.** Sie soll grundsätzlich herstellerunabhängig einsetzbar sein; **andere Kameras, andere Bildformate und Bilder über 71 MP sind bisher nicht verifiziert**. Eine garantierte maximale Bildgröße wird ausdrücklich nicht angegeben.

Belastungstests mit ungefähr 100, 200 und 500 Megapixeln sind geplant, aber noch nicht abgeschlossen. Näheres unter [TESTING.md](TESTING.md).

## Vorgesehene Ausgaben (noch nicht hochgeladen)

- **Python-Version v3.3:** bestehende Version, deren Quellen nach Prüfung übernommen werden sollen.
- **Windows-Offline-Version v4.1.1:** als portable Windows-Ausgabe vorgesehen; ein vollständiger, erfolgreicher EXE-Test auf einem zweiten Rechner ist noch nicht bestätigt.
- Bestehende ältere Versionen sollen bei der Übernahme unverändert bleiben.

Die vorgesehene lokale Bildverarbeitung benötigt keinen Cloud-Upload der Fotos. Für Installation und Erstellung der Software kann dennoch Internet erforderlich sein.

## Open Source und Mitarbeit

Fehlermeldungen, Verbesserungen, Übersetzungen und reproduzierbare Tests sind willkommen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md).

Die hier neu eingeführten eigenen Projektbestandteile stehen unter der [MIT-Lizenz](LICENSE). **Fremdcode, KI-Modelle und Bibliotheken behalten ihre eigenen Lizenzen**. Für noch ungeklärte Modellgewichte oder Konvertierungen wird keine Weitergabeerlaubnis behauptet. Siehe [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Unabhängiges Projekt

Dies ist ein unabhängiges Community-Projekt und **steht in keiner offiziellen Verbindung zu Insta360**. Die Herstellerbezeichnung dient ausschließlich zur Benennung der bisher verwendeten Testkamera.
