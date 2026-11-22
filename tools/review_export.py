"""Exportiert die Übersetzung zur Korrektur-Prüfung: je Zeile Key, Sprecher, EN, KO (Originalsprache), DE.

Aufruf: python tools/review_export.py WORK OUTDIR PAKET=DATEIPRÄFIX,... [PAKET=...]
  z. B. p1=S00E01,S00E02 p2=S01E05,S01E06
Liest WORK/*.en.ass (Effect = Tabelle|Key), WORK/.sub_work/<datei>/seg.jsonl + trans_*.jsonl und
WORK/quelle/<Tabelle>.csv. DE und EN enthalten die geschützten Platzhalter ⟦Tn⟧ (Tags), wie sie
im Übersetzungs-Workflow verwendet werden – Korrekturen müssen sie unverändert übernehmen.
"""
import csv, glob, json, os, sys

W, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
ko_cache = {}


def ko(table, key):
    if table not in ko_cache:
        p = os.path.join(W, "quelle", table + ".csv")
        ko_cache[table] = {r["key"]: r.get("ko-KR", "") for r in csv.DictReader(open(p, encoding="utf-8-sig"))}
    return ko_cache[table].get(key, "")


for spec in sys.argv[3:]:
    name, prefixes = spec.split("=", 1)
    lines = []
    for pre in prefixes.split(","):
        en_ass = glob.glob(os.path.join(W, pre + "*.en.ass"))[0]
        base = os.path.basename(en_ass)[:-4]
        work = os.path.join(W, ".sub_work", base)
        eff = {}
        for i, line in enumerate(open(en_ass, encoding="utf-8-sig"), 1):
            if line.startswith("Dialogue:"):
                eff[i] = line.split(",", 9)[8]
        trans = {}
        for f in glob.glob(os.path.join(work, "trans_*.jsonl")):
            for l in open(f, encoding="utf-8"):
                if l.strip():
                    o = json.loads(l); trans[o["id"]] = o["de"]
        lines.append(f"\n## {base[:-3]}\n")
        last_style = None
        for l in open(os.path.join(work, "seg.jsonl"), encoding="utf-8"):
            s = json.loads(l)
            key = eff[s["id"]]
            table, k = key.split("|", 1)
            if s["style"] != last_style:
                lines.append(f"\n### Szene: {s['style']}\n")
                last_style = s["style"]
            lines.append(f"[{key}] {s['name']}\n  EN: {s['src']}\n  KO: {ko(table, k)}\n  DE: {trans[s['id']]}\n")
    path = os.path.join(out, f"review_{name}.md")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("".join(lines))
    print(f"{path}: {sum(1 for x in lines if x.startswith('['))} Zeilen")
