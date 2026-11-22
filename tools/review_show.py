"""Zeigt Korrekturvorschläge kompakt zur Prüfung: Key, Art, EN, alt, neu, Grund.
Aufruf: python tools/review_show.py WORK FUNDE.jsonl [...]"""
import csv, json, os, sys

W = sys.argv[1]
en_cache = {}
def en(key):
    table, k = key.split("|", 1)
    if table not in en_cache:
        p = os.path.join(W, "quelle", table + ".csv")
        en_cache[table] = {r["key"]: r.get("en-US", "") for r in csv.DictReader(open(p, encoding="utf-8-sig"))}
    return en_cache[table].get(k, "")

for path in sys.argv[2:]:
    for n, l in enumerate(open(path, encoding="utf-8"), 1):
        if l.strip():
            f = json.loads(l)
            print(f"#{os.path.basename(path)[6:8]}-{n} {f['key']} [{f.get('art')}]")
            print(f"   EN : {en(f['key'])}")
            print(f"   alt: {f['alt']}")
            print(f"   neu: {f['neu']}")
            print(f"   ⇒ {f.get('grund')}")
