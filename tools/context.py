"""Zeigt eine Zeile mit Kontext in allen Sprachen: EN, KR (Originalsprache), JP und DE.
Aufruf: python tools/context.py WORK Tabelle|Key [Kontextzeilen=4]
Erwartet WORK/quelle/*.csv (extract_tables.py) und WORK/*.de.ass."""
import csv, glob, os, re, sys

W, target = sys.argv[1], sys.argv[2]
n = int(sys.argv[3]) if len(sys.argv) > 3 else 4
table, key = target.split("|", 1)
rows = list(csv.DictReader(open(os.path.join(W, "quelle", table + ".csv"), encoding="utf-8-sig")))
de = {}
for f in glob.glob(os.path.join(W, "*.de.ass")):
    for line in open(f, encoding="utf-8-sig"):
        if line.startswith("Dialogue:"):
            p = line.rstrip("\r\n").split(",", 9)
            de[p[8]] = (p[4], p[9])
idx = next(i for i, r in enumerate(rows) if r["key"] == key)
for r in rows[max(0, idx - n): idx + n + 1]:
    k = f"{table}|{r['key']}"
    spk, txt = de.get(k, ("?", ""))
    mark = ">>" if r["key"] == key else "  "
    print(f"{mark} {r['key']} [{spk}]")
    for lang in ("en-US", "ko-KR", "ja-JP"):
        print(f"     {lang[:2].upper()}: {r.get(lang, '')}")
    print(f"     DE: {txt}")
