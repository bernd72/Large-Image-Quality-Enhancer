# Large Image Quality Enhancer

**Open-Source-Software zur KI-gestützten Qualitätsverbesserung großer, hochauflösender Fotos.**

[English](README.md) · [Mitarbeit / Contributing](CONTRIBUTING.md) · [Fremdlizenzen](THIRD_PARTY_NOTICES.md) · [Teststand](TESTING.md) · [Bekannte Einschränkungen](KNOWN_ISSUES.md)

> **Quellcode vorhanden – noch keine fertige EXE zum Herunterladen.** Die Python-Version 3.3 und die Windows-Bauskripte für v4.1.1 sind veröffentlicht. **KI-Modellgewichte und eine fertige EXE sind nicht enthalten.** Für die Modelle sind die Nutzungs- und Weitergaberechte gesondert zu beachten. Eine bestehende Windows-EXE wurde laut Entwickler auf zwei weiteren Windows-11-PCs getestet; ein unabhängig überprüfter Build aus diesem Repository liegt noch nicht vor.

## Schnellstart unter Windows 11 (64 Bit)

1. Auf GitHub **Code → Download ZIP** auswählen und das Repository in einen kurzen Pfad entpacken, beispielsweise `C:\\LIQE\\`.
2. Den Ordner `windows/offline-v4.1.1/` öffnen und **[AUTO_BUILD_WINDOWS_EXE.bat](windows/offline-v4.1.1/AUTO_BUILD_WINDOWS_EXE.bat)** starten. Das Skript kann Python 3.12 für den aktuellen Benutzer installieren, nach Zustimmung benötigte KI-Modelle herunterladen, Python-Bibliotheken einrichten und die portable Windows-Version bauen. **Für den ersten Bau ist normalerweise Internet erforderlich.**
3. Alternativ **Python 3.12 (64 Bit)** selbst installieren, die drei benötigten Modelldateien rechtmäßig im lokalen Ordner `models` bereitstellen und `BAUE_WINDOWS_EXE.bat` ausführen.
4. Nach erfolgreichem Bau den **gesamten** Ordner `dist/Insta360_X5_KI_Offline/` auf den Ziel-PC kopieren. Zum Ausführen der EXE sind dort weder Python noch eine Internetverbindung nötig.

**Wichtiger Teststand:** Der automatische Bau wurde auf einem frisch eingerichteten Windows-PC noch **nicht** praktisch verifiziert. Eine funktionierende EXE lässt sich daher noch nicht garantieren. Die Modellgewichte und die fertige EXE liegen **nicht** im Repository. Das automatische Skript lädt die Modelle nach Zustimmung von **externen Drittanbietern** herunter: DPRNet aus dem Repository von Raspberry Pi und die konvertierte SCUNet-ONNX-Version von Heliosoph auf Hugging Face, nicht vom ursprünglichen SCUNet-Projekt. Siehe [Lizenzhinweise](THIRD_PARTY_NOTICES.md) und [Windows-Bauanleitung](windows/offline-v4.1.1/README_OFFLINE.txt).

## Sprachauswahl in der Python-Version 3.3

Auch die [Python-Version 3.3](python/v3.3/) enthält jetzt eine Auswahl **„Sprache / Language“** mit **Deutsch** und **English**. Die Oberfläche, Modell-Downloads und die Stapelverarbeitung können ohne Neustart umgeschaltet werden. Die neue Datei [`python/v3.3/x5_i18n.py`](python/v3.3/x5_i18n.py) muss neben `x5_dprnet.py` liegen; `STARTEN.bat` bleibt unverändert. **Die Sprachumschaltung selbst ist offline**, für das Herunterladen fehlender KI-Modelle kann jedoch Internet erforderlich sein. Ein vollständiger Windows-GUI-Test steht aus.

## Sprache der Windows-Oberfläche

Im aktuellen Windows-Quellcode lässt sich die grafische Oberfläche über das Auswahlfeld **„Sprache / Language“** zwischen **Deutsch** und **English** umschalten. Die Auswahl wirkt sofort, auch in der Stapelverarbeitung; ein Neustart ist nicht nötig. Die Übersetzungen sind lokal eingebaut und benötigen keine Internetverbindung. **Bereits erstellte EXE-Dateien enthalten diese neue Funktion nicht automatisch:** Dazu muss mit dem aktualisierten Quellcode eine neue EXE gebaut werden. Der neue Sprachwechsel wurde noch nicht auf einem Windows-PC praktisch geprüft.

## Ziel

Die Bildqualität soll verbessert werden, **nicht die Bildauflösung vergrößert**. Die bisherige Entwicklung konzentriert sich auf Aufhellung dunkler Bereiche, Rauschreduzierung und Stapelverarbeitung hochauflösender Fotos. Zwei Quellcode-Ausgaben sind bereits vorhanden: Python v3.3 und das Windows-Offline-Baupaket v4.1.1. Eine fertige Windows-Version zum direkten Herunterladen gibt es derzeit nicht.

## Kompatibilität und Teststand

**Bisher wurde die Software ausschließlich mit JPEG-Aufnahmen einer Insta360 X5 bis etwa 71 Megapixel (11.904 × 5.952 Pixel) getestet.** Sie soll grundsätzlich herstellerunabhängig einsetzbar sein; **andere Kameras, andere Bildformate und Bilder über 71 MP sind bisher nicht verifiziert**. Eine garantierte maximale Bildgröße wird ausdrücklich nicht angegeben.

Eine Windows-EXE wurde nach Angabe des Entwicklers auf einem zweiten und dritten PC erfolgreich unter Windows 11 getestet. Die genaue EXE-Version und die Einzelheiten der Offline-Testumgebung müssen noch dokumentiert werden; laut Entwickler funktioniert die vorhandene Windows-EXE auch ohne Internetverbindung. Daraus ergibt sich **keine** bestätigte Kompatibilität mit anderen Windows-Versionen oder Bildformaten. Belastungstests mit ungefähr 100, 200 und 500 Megapixeln sind geplant, aber noch nicht abgeschlossen. Näheres unter [TESTING.md](TESTING.md).

## Bekannte Einschränkung: nur Bilder im Seitenverhältnis 2:1

Nach aktuellen Entwicklertests verarbeitet die Windows-Version **nur Bilder mit dem Breiten-Höhen-Verhältnis 2:1** (zum Beispiel 11.904 × 5.952 Pixel). **Bei anderen Seitenverhältnissen tritt während der Verarbeitung eine Fehlermeldung auf, sowohl bei Einzelbildern als auch bei der Stapelverarbeitung.** Die Ursache ist noch ungeklärt. Bis zur Behebung sind nur 2:1-Bilder als funktionierend gemeldet. Siehe [bekannte Fehler](KNOWN_ISSUES.md).

## Bekannte Einschränkung: lange Verzeichnispfade unter Windows

Die Windows-EXE funktioniert laut Entwickler unter Windows 11 **vollständig ohne Internetverbindung**. Beim Entpacken oder Ausführen aus sehr tief verschachtelten Ordnern traten jedoch Probleme auf. **Vorläufige Lösung:** Das Programm unter einem möglichst kurzen Pfad wie `C:\LIQE\` entpacken und von dort aus starten. Die genaue Ursache und eine mögliche Pfadlängengrenze sind noch nicht geklärt. Weitere Hinweise: [KNOWN_ISSUES.md](KNOWN_ISSUES.md).

## Sicherheit und Einschränkungen beim Bau

Beide Quellcode-Versionen deaktivieren derzeit die automatische Bildgrößen-Schutzprüfung von Pillow (`Image.MAX_IMAGE_PIXELS = None`), damit sehr große Fotos geöffnet werden können. **Bis zur Einführung eigener Größen- und Speicherprüfungen sollten nur vertrauenswürdige Bilddateien geöffnet werden.** Das automatische Downloadskript prüft bei allen drei Modelldateien die Mindestgröße, vergleicht aber nur für **eine** SCUNet-Datei einen festen SHA-256-Prüfwert. Die übrigen Modelldateien sind somit nicht vollständig per Prüfsumme abgesichert. Siehe [bekannte Einschränkungen](KNOWN_ISSUES.md). Die erzeugte Windows-EXE ist nicht digital signiert.

## Mehrere Instanzen parallel verwenden

Die Windows-EXE kann mehrfach gestartet werden, sodass mehrere Bildverarbeitungen gleichzeitig laufen können, sofern ausreichend Rechnerressourcen vorhanden sind. Nach Angaben des Entwicklers laufen **zwei Instanzen parallel auf einem Rechner mit Intel Core i5-14400**; auf einem **leistungsstärkeren Rechner sind fünf bis sechs Instanzen möglich**. Diese Werte sind Erfahrungsbeispiele, **keine garantierte Leistung und keine feststehende Softwaregrenze**. Wie viele Instanzen sinnvoll sind, hängt unter anderem von CPU-Auslastung, verfügbarem Arbeitsspeicher, Datenträgergeschwindigkeit, Bildgröße und Einstellungen ab. Die Systemauslastung sollte beobachtet werden; zusätzliche Instanzen können die Verarbeitung auch verlangsamen oder zu Speichermangel führen.

## Berichtete Bearbeitungszeit

Nach Erfahrung des Entwicklers dauert die **vollständige Verarbeitung eines JPEG-Bildes der Insta360 X5 mit rund 71 Megapixeln auf einem Intel Core i5-14400 etwa 45–50 Minuten**. Dies ist ein **berichteter Praxiswert, kein standardisierter Benchmark und keine garantierte Laufzeit**. Der Einfluss gleichzeitig gestarteter Instanzen, der RAM-Ausstattung, der Modelle/Einstellungen und der EXE-Version wurde für diese Zeitangabe noch nicht systematisch dokumentiert.

## Sprache des Windows-Bauprogramms

Die Startdatei [`AUTO_BUILD_WINDOWS_EXE.bat`](windows/offline-v4.1.1/AUTO_BUILD_WINDOWS_EXE.bat) und die nachgelagerten PowerShell-Bauschritte geben Rückfragen, Fortschrittsmeldungen und Fehler jetzt **auf Englisch** aus. Das betrifft auch die Python-Installation und den Modelldownload. Die Sprachauswahl in der späteren Programmoberfläche ist davon unabhängig. Die englischen Texte wurden im Quellcode überprüft; ein kompletter Praxistest auf einem englischsprachigen Windows-System steht noch aus.

## Automatischer Windows-Bau ohne vorherige Python-Installation

Das Baupaket enthält **`AUTO_BUILD_WINDOWS_EXE.bat`**. Es erkennt vorhandenes Python 3.12 oder installiert es nach Zustimmung für den aktuellen Benutzer. Anschließend können die externen KI-Modelle mit Zustimmung heruntergeladen und die benötigten Pakete für den EXE-Bau eingerichtet werden. **Python wird für den Bau weiterhin benötigt**, muss aber nicht vorher installiert sein. Der automatische Ablauf ist noch nicht auf einem frischen Windows-System verifiziert; Netzwerksperren oder Unternehmensrichtlinien können ihn verhindern.

Die **manuelle Alternative** bleibt `BAUE_WINDOWS_EXE.bat` mit bereits vorhandenem Python 3.12 und den lokal bereitgestellten Modelldateien. Siehe [Windows-Bauanleitung](windows/offline-v4.1.1/README_OFFLINE.txt).

## Programmquellen und EXE-Bau

- **[Python-Version 3.3](python/v3.3/):** Quellcode, `requirements.txt` und `STARTEN.bat`. Benötigt eine geeignete 64-Bit-Python-Version, die Python-Bibliotheken sowie lokal bereitgestellte DPRNet-/SCUNet-Modelldateien im Unterordner `models`. Einzelheiten: [`README_START_HIER.txt`](python/v3.3/README_START_HIER.txt).
- **[Windows-Baupaket 4.1.1](windows/offline-v4.1.1/):** Python-Quellen und `BAUE_WINDOWS_EXE.bat` / `.ps1`. Auf einem Windows-64-Bit-Rechner Python 3.12 (64 Bit) bereitstellen, die erforderlichen Modellgewichte unter `windows/offline-v4.1.1/models/` ablegen und `BAUE_WINDOWS_EXE.bat` starten. PyInstaller erstellt daraus die portable EXE. Siehe [`README_OFFLINE.txt`](windows/offline-v4.1.1/README_OFFLINE.txt) und [`Hinweise zu den Modellen`](windows/offline-v4.1.1/MODELLE_HIER_EINFUEGEN.txt). Nur der Bau kann einen Internetzugang für Pakete benötigen, die fertige Anwendung ist für den Offlinebetrieb vorgesehen.

**Nicht enthalten:** fertige EXE, KI-Modellgewichte, Python-Umgebungen oder Build-Ausgaben. Ein erfolgreicher Windows-Bau der v4.1.1 wurde hier **nicht** unabhängig bestätigt; die Version der zuvor getesteten EXE ist nicht dokumentiert. Die beiden Quellcode-Ausgaben bleiben getrennt.

Der Offlinebetrieb einer vorhandenen Windows-EXE wurde vom Entwickler berichtet; die Bildverarbeitung erfolgt lokal ohne Cloud-Upload der Fotos. Für die Installation von Abhängigkeiten oder das Erstellen der Software kann dennoch Internet erforderlich sein. Bitte keine ungeprüften Modellgewichte öffentlich hochladen.

## Open Source und Mitarbeit

Fehlermeldungen, Verbesserungen, Übersetzungen und reproduzierbare Tests sind willkommen. Siehe [CONTRIBUTING.md](CONTRIBUTING.md).

Die hier neu eingeführten eigenen Projektbestandteile stehen unter der [MIT-Lizenz](LICENSE). **Fremdcode, KI-Modelle und Bibliotheken behalten ihre eigenen Lizenzen**. Für noch ungeklärte Modellgewichte oder Konvertierungen wird keine Weitergabeerlaubnis behauptet. Siehe [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Unabhängiges Projekt

Dies ist ein unabhängiges Community-Projekt und **steht in keiner offiziellen Verbindung zu Insta360**. Die Herstellerbezeichnung dient ausschließlich zur Benennung der bisher verwendeten Testkamera.
