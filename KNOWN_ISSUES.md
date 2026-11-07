# Known issues and limitations / Bekannte Fehler und Einschränkungen

## Deutsch

### Windows-Version: Probleme bei langen Verzeichnispfaden

**Beobachtung:** Die Windows-EXE funktioniert nach Angaben des Entwicklers unter Windows 11 auch vollständig **ohne Internetverbindung**. Beim Entpacken oder Ausführen aus einem tief verschachtelten Verzeichnis kam es allerdings zu Problemen. Lange Pfade innerhalb des Installationsordners können die Nutzung beeinträchtigen.

**Vorläufige Lösung:** Das Programm in einen Ordner mit kurzem Pfad entpacken und von dort starten, zum Beispiel `C:\LIQE\` oder `C:\ImageEnhancer\`. Sehr tief verschachtelte Unterordner vermeiden.

**Status:** Bekannte, vom Entwickler berichtete Einschränkung. Die genaue Ursache, eine mögliche Pfadlängengrenze und die betroffenen Dateien wurden noch nicht systematisch untersucht. Ein Zusammenhang mit Windows-Pfadlängenbegrenzungen ist möglich, aber noch nicht bestätigt. Die korrekte Funktion bei beliebigen Verzeichnispfaden kann daher derzeit nicht zugesichert werden.

Der Offlinebetrieb bezieht sich auf die **Nutzung einer bereits lauffähigen Windows-EXE**. Das Einrichten der Entwicklungsumgebung oder Erstellen der EXE kann Internetzugang erfordern.

## English

### Windows edition: problems with long directory paths

**Observation:** According to developer testing, the Windows executable works on Windows 11 **without an internet connection**. However, problems were encountered when extracting or running the application from a deeply nested directory. Long paths within the application folder may interfere with its operation.

**Workaround:** Extract the application to a short folder path and run it from there, for example `C:\LIQE\` or `C:\ImageEnhancer\`. Avoid deeply nested directories.

**Status:** Known limitation reported by the developer. The root cause, any exact path-length threshold, and the affected files have not yet been systematically determined. Windows path-length restrictions are one possibility, but that has not been confirmed. Reliable operation from arbitrary directory depths is therefore not guaranteed.

Offline operation refers to **running an existing, working Windows executable**. Setting up the development environment or building the EXE may still require internet access.
