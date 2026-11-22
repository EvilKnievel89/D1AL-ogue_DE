"""Zeigt Korrekturvorschläge gruppiert nach Satzketten: ganzer Satz ALT und NEU, mit Kontextzeile.
Aufruf: python tools/review_chainview.py WORK FUNDE.jsonl [...]"""
import csv, glob, json, os, sys

W = sys.argv[1]
order, text = [], {}
for f in sorted(glob.glob(os.path.join(W, "*.de.ass"))):
    for line in open(f, encoding="utf-8-sig"):
        if line.startswith("Dialogue:"):
            p = line.rstrip("\r\n").split(",", 9)
            order.append(p[8]); text[p[8]] = (p[4], p[9])
pos = {k: i for i, k in enumerate(order)}
en = {}
for t in ("DialogueTable", "CutScene", "CommentDialogueTable"):
    for r in csv.DictReader(open(os.path.join(W, "quelle", t + ".csv"), encoding="utf-8-sig")):
        en[f"{t}|{r['key']}"] = r["en-US"]

fixes = {}
for path in sys.argv[2:]:
    for n, l in enumerate(open(path, encoding="utf-8"), 1):
        if l.strip():
            f = json.loads(l); f["_id"] = f"{os.path.basename(path)[6:8]}-{n}"; fixes[f["key"]] = f
keys = sorted(fixes, key=lambda k: pos[k])
groups, cur = [], []
for k in keys:
    if cur and pos[k] - pos[cur[-1]] > 2:
        groups.append(cur); cur = []
    cur.append(k)
if cur:
    groups.append(cur)
for g in groups:
    a, b = pos[g[0]] - 1, pos[g[-1]] + 1
    span = order[max(0, a): b + 1]
    ids = ", ".join(fixes[k]["_id"] for k in g)
    print(f"=== {g[0]} … ({len(g)} Fenster geändert; {ids}) – {fixes[g[0]].get('grund', '')[:160]}")
    print("  EN : " + " / ".join(en.get(k, "?") for k in span[1:-1]))
    print("  ALT: " + " / ".join(text[k][1] for k in span[1:-1]))
    print("  NEU: " + " / ".join(fixes[k]["neu"] if k in fixes else text[k][1] for k in span[1:-1]))
