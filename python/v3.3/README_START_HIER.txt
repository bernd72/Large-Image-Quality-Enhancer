Insta360 X5 · DPRNet + SCUNet KI-Optimierer v3.3
================================================

SPRACHAUSWAHL / LANGUAGE SELECTION (AKTUALISIERTER QUELLCODE)
- Oben in der grafischen Oberfläche „Sprache / Language“ auswählen.
- Die Oberfläche kann ohne Neustart zwischen Deutsch und English wechseln.
- Auch Modell-Downloads, Rückfragen und die Stapelverarbeitung werden übersetzt.
- Die Sprachdatei x5_i18n.py muss zusammen mit x5_dprnet.py im Programmordner liegen.
- Für die Sprachumschaltung ist kein Internet nötig; Modell-Downloads können weiterhin
  eine Internetverbindung erfordern.
- Änderungen am KI-Verarbeitungsablauf sind hierfür nicht erforderlich.
- Teststand: Übersetzungstexte statisch geprüft; ein vollständiger GUI-Test auf
  einem Windows-Rechner steht noch aus.

NEU IN VERSION 3.3
- STAPELVERARBEITUNG: mehrere JPGs auf einmal auswählen und bearbeiten.
- Restzeitanzeige bei Einzel- und Stapelverarbeitung in Stunden/Minuten.
- Drei Speichermodi für den Stapel:
  1) Neue KI-Bilder erzeugen; bei Namensgleichheit automatisch durchnummerieren (Standard).
  2) Bereits vorhandene KI-Ergebnisbilder ersetzen (Originale bleiben unverändert).
  3) Original-JPGs ersetzen (nach ausdrücklicher Bestätigung; Sicherungen empfohlen).
- Einzel-Export: optionale Checkbox zum Ersetzen des Original-JPGs mit automatischer Sicherung.
- Kleinere Fenster: Hauptansicht kann vertikal gescrollt werden.
- Bei fehlgeschlagenem oder abgebrochenem Export wird keine unvollständige Datei
  als Ergebnis gespeichert. Ein Original wird erst nach vollständiger Bearbeitung ersetzt.

UPDATE EINER FUNKTIONIERENDEN VERSION 3.2
1. Programm schließen.
2. Die drei Update-Dateien x5_dprnet.py, x5_batch.py und x5_i18n.py in den
   bisherigen Programmordner kopieren; vorhandene gleichnamige Dateien ersetzen.
3. Ordner .venv und models UNVERÄNDERT LASSEN.
4. STARTEN.bat wie gewohnt starten.

ALLE BILDER IM STAPEL VERARBEITEN
1. Bisheriges KI-Setup wie gewohnt einstellen (DPRNet, SCUNet, Schatten usw.).
2. STAPELVERARBEITUNG ... anklicken.
3. JPGs hinzufügen ... wählen; bei Bedarf mehrere Dateigruppen ergänzen.
4. Speichermodus und gegebenenfalls Ausgabeordner festlegen.
5. STAPELVERARBEITUNG STARTEN anklicken.

SPEICHERN UND ORIGINALSCHUTZ
- Standardmäßig werden zusätzliche JPG-Dateien mit dem Zusatz
  _DPRNet_SCUNet_KI erzeugt. Bereits vorhandene Ergebnisse werden dann nicht überschrieben.
- Der Modus 'Vorhandene KI-Ergebnisdateien ersetzen' überschreibt nur die
  vom Programm erzeugten Ergebnisnamen im gewählten Ausgabeordner.
- Der Modus 'Original-JPGs direkt überschreiben' ersetzt die eingesetzten JPGs
  erst nach vollständigem und erfolgreichem Export. Er benötigt eine ausdrückliche
  Bestätigung. Die unveränderte Sicherung heißt z.B.
  IMG_123_ORIGINAL_Sicherung_20261105_102000.jpg
- Sicherungen benötigen freien Speicher. Bitte besonders wichtige Originaldateien
  zusätzlich auf einem zweiten Datenträger sichern.
- Auch beim einzelnen Export kann das Original über eine eigene Checkbox
  (mit automatischer Sicherung) ersetzt werden.

FORTSCHRITT UND RESTZEIT
- Balken und Text zeigen Gesamtfortschritt beim Stapel und das aktuelle Bild (i/n).
- Die Restzeit wird anhand der bisherigen Geschwindigkeit geschätzt; sie ist
  gerade während des ersten Bildes nur eine Näherung.
- Die Schätzung kann bei Bildern unterschiedlicher Auflösung und unterschiedlichem
  Motiv etwas abweichen. Die Anzeige nutzt Stunden und Minuten.
- ABBRECHEN stoppt nach dem nächsten überprüften Verarbeitungsschritt. Ein schon
  vollständig gespeichertes Ergebnis bleibt bestehen.

MODELLE / BIBLIOTHEKEN
- DPRNet_1024.tflite oder DPRNet_512.tflite im Unterordner models.
- SCUNet: scunet_color_real_psnr.onnx + scunet_color_real_psnr.onnx.data
  ebenfalls in models (beide benötigt).
- Die bestehende Python-3.12-Umgebung .venv bleibt unverändert.
- Die KI läuft lokal; kein Abo und kein Upload deiner Fotos nötig.

BEKANNTE EINSCHRÄNKUNGEN
- Die fruehere 2:1-Beschraenkung ist im Quellcode behoben. Weitere Fotoformate
  sind bei dieser Python-Version noch nicht praktisch getestet.
- Die vollständige Bearbeitung eines 71-MP-Panoramas mit SCUNet kann auf CPU
  sehr lange dauern. Bei der Vorschau zuerst die Wirkung testen.
- Teststand: GUI, Stapel, sichere Speicherung und Abbruch wurden mit
  Testbildern und simulierten Modellkorrekturen geprüft. Ein echter Windows-KI-Lauf
  mit DPRNet+SCUNet wurde hier nicht erneut ausgeführt.
