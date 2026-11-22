"""Findet Sätze, die über mehrere Textfenster laufen, und exportiert sie als Ganzes zur Prüfung.

Aufruf: python tools/review_chains.py WORK OUTDIR [--min 3] [--packages 4]
Verbindet Zeile i mit i+1 (gleiche Datei, gleiche Szene), wenn der englische Text von i offen endet
(Komma, Semikolon, Doppelpunkt, Gedankenstrich, Buchstabe) oder i+1 klein beginnt.
Ausgabe: OUTDIR/chains_pN.md – je Kette eine Kontextzeile davor/danach, dazu EN, KO, DE pro Zeile.
"""
import argparse, csv, glob, json, os, re

ap = argparse.ArgumentParser()
ap.add_argument("work"); ap.add_argument("out")
ap.add_argument("--min", type=int, default=3)
ap.add_argument("--packages", type=int, default=4)
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
PH = re.compile(r"⟦T\d+⟧")
ko_cache = {}


def ko(key):
    table, k = key.split("|", 1)
    if table not in ko_cache:
        p = os.path.join(a.work, "quelle", table + ".csv")
        ko_cache[table] = {r["key"]: r.get("ko-KR", "") for r in csv.DictReader(open(p, encoding="utf-8-sig"))}
    return ko_cache[table].get(k, "")


def open_end(t):
    t = PH.sub("", t).strip()
    return bool(t) and (t[-1] in ",;:—–-" or t[-1].isalnum())


def starts_lower(t):
    t = PH.sub("", t).lstrip(" .…'\"„“")
    return bool(t) and t[0].islower()


chains = []
for en_ass in sorted(glob.glob(os.path.join(a.work, "S01*.en.ass"))):
    base = os.path.basename(en_ass)[:-4]
    work = os.path.join(a.work, ".sub_work", base)
    eff = {i: l.split(",", 9)[8] for i, l in enumerate(open(en_ass, encoding="utf-8-sig"), 1) if l.startswith("Dialogue:")}
    trans = {}
    for f in glob.glob(os.path.join(work, "trans_*.jsonl")):
        for l in open(f, encoding="utf-8"):
            if l.strip():
                o = json.loads(l); trans[o["id"]] = o["de"]
    segs = [json.loads(l) for l in open(os.path.join(work, "seg.jsonl"), encoding="utf-8")]
    i = 0
    while i < len(segs):
        j = i
        while (j + 1 < len(segs) and segs[j + 1]["style"] == segs[j]["style"]
               and (open_end(segs[j]["src"]) or starts_lower(segs[j + 1]["src"]))):
            j += 1
        if j - i + 1 >= a.min:
            rows = []
            for k in range(max(0, i - 1), min(len(segs), j + 2)):
                s = segs[k]
                rows.append((k < i or k > j, eff[s["id"]], s["name"], s["src"], ko(eff[s["id"]]), trans[s["id"]]))
            chains.append((base[:-3], rows))
        i = j + 1

per = -(-len(chains) // a.packages)
total_lines = 0
for p in range(a.packages):
    part = chains[p * per:(p + 1) * per]
    out = []
    for n, (base, rows) in enumerate(part, 1):
        out.append(f"\n## Kette {p + 1}.{n} – {base}\n")
        for ctx, key, spk, en, k, de in rows:
            if ctx:
                out.append(f"(Kontext) [{key}] {spk}: {de}\n")
            else:
                total_lines += 1
                out.append(f"[{key}] {spk}\n  EN: {en}\n  KO: {k}\n  DE: {de}\n")
    with open(os.path.join(a.out, f"chains_p{p + 1}.md"), "w", encoding="utf-8") as fh:
        fh.write("".join(out))
print(f"{len(chains)} Ketten mit ≥{a.min} Fenstern, {total_lines} Zeilen, {a.packages} Pakete à ≤{per} Ketten")
