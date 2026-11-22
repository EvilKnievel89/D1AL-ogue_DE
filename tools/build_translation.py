"""Baut aus den übersetzten ASS-Dateien die Übersetzungsdatei für den Patcher.

Aufruf: python tools/build_translation.py [ass-ordner] [ziel.json] [--version X.Y.Z]
Standard: translation/ass  ->  translation/D1AL-ogue_DE.json

Jede Dialogue-Zeile trägt im Effect-Feld "Tabelle|Key" (von make_ass.py gesetzt); der Text wird
unverändert übernommen (\\N, {NL} usw. löst der Patcher passend zum Original auf).
"""
import argparse, glob, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DLG = re.compile(r"^Dialogue:\s*(.*)$")

ap = argparse.ArgumentParser()
ap.add_argument("ass_dir", nargs="?", default=os.path.join(ROOT, "translation", "ass"))
ap.add_argument("out", nargs="?", default=os.path.join(ROOT, "translation", "D1AL-ogue_DE.json"))
ap.add_argument("--version", default="1.0.0")
a = ap.parse_args()

entries, files = {}, sorted(glob.glob(os.path.join(a.ass_dir, "*.de.ass")))
for f in files:
    for line in open(f, encoding="utf-8-sig"):
        m = DLG.match(line.rstrip("\r\n"))
        if not m:
            continue
        parts = m.group(1).split(",", 9)
        if "|" not in parts[8]:
            continue
        if parts[8] in entries:
            raise SystemExit(f"Doppelter Key {parts[8]} in {f}")
        entries[parts[8]] = parts[9]

data = {"format": 1, "game": "D1AL-ogue", "steam_appid": 4270390, "language": "de",
        "version": a.version, "entries": dict(sorted(entries.items()))}
with open(a.out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=1)
    fh.write("\n")
print(f"{len(files)} Dateien, {len(entries)} Einträge -> {a.out}")
