# Werkzeuge

Alle Skripte brauchen Python ≥ 3.10 und [UnityPy](https://github.com/K0lb3/UnityPy) (`pip install UnityPy`).
Pfade im Beispiel: `GAME` = Spielordner, `WORK` = lokaler Arbeitsordner (nicht im Repo).

## Ablauf

1. **Originaltexte extrahieren** (unverändertes Spiel, ggf. vorher Patcher → Deinstallieren):
   ```
   python tools/extract_tables.py GAME WORK
   ```
   Schreibt `WORK/quelle/*.csv`: alle String-Tables (alle Sprachen) und die Entwickler-CSVs aus
   `resources.assets` (`Dialogue` mit Sprecher/Szenentyp, `Guest`, `News`).

2. **ASS-Dateien erzeugen** (eine pro Kundenbesuch bzw. Tabelle):
   ```
   python tools/make_ass.py WORK
   ```
   Jede Zeile: `Style` = Szenentyp, `Name` = Sprecher, `Effect` = `Tabelle|Key` im Bundle, `Text` = englischer Text.
   Echte Zeilenumbrüche (News) werden als `{NL}` kodiert. Vorhandene Dateien werden nie überschrieben.
   Prüft, dass jede der 3.874 Dialogzeilen genau einer Datei zugeordnet ist.

3. **Übersetzen** – die ASS-Dateien wurden mit einem Untertitel-Übersetzungs-Workflow (Claude-Agent,
   Skript zur Struktur/Text-Trennung) bearbeitet: erst Analyse aller Folgen, dann gemeinsames Glossar
   (`translation/glossar.md`), dann parallele Übersetzung mit automatischer Vollständigkeits- und Tag-Prüfung.
   Ergebnis: `*.de.ass` → nach `translation/ass/` kopieren.

4. **Übersetzungsdatei bauen:**
   ```
   python tools/build_translation.py [--version X.Y.Z]
   ```

5. **Prüfen:**
   | Skript | Zweck |
   |---|---|
   | `qa.py WORK [S01E02:5-30]` | Länge DE/EN, eingefügte Umbrüche, gleiche Quelle mit verschiedener Übersetzung, Stichprobe |
   | `glyphs.py WORK GAME` | Alle verwendeten Zeichen im Spielfont (Silver_EN) vorhanden? |
   | `termcheck.py WORK "Regex" …` | Wie wurde ein Begriff in welcher Datei übersetzt? |
   | `show.py WORK S01E03:82-84` | Segmente EN/DE anzeigen |
   | `context.py WORK "DialogueTable\|60016_56" [n]` | Zeile mit n Zeilen Kontext in EN, KO (Originalsprache), JA und DE – für Fehlermeldungen |
   | `verify_bundle.py WORK GAME` | Gepatchtes Bundle gegen Original: gleiche Struktur (Umbrüche, Tags, Platzhalter) je Eintrag |

Hinweis: `qa.py`, `glyphs.py`, `termcheck.py` erwarten `*.de.ass` (und für Vergleiche `*.en.ass`) im
Arbeitsordner; `verify_bundle.py` erwartet die Original-Sicherung unter `WORK/backup/`.
