"""Wendet geprüfte Korrekturvorschläge (funde_*.jsonl) auf die Übersetzung an.

Aufruf: python tools/review_apply.py WORK FUNDE.jsonl [...] [--skip KEY,KEY] [--dry-run]
Fund-Format: {"key": "Tabelle|Key", "alt": "...", "neu": "...", "art": "...", "grund": "..."}

Sicherheitsprüfungen je Fund: Key bekannt, "alt" entspricht exakt der aktuellen Übersetzung,
Platzhalter ⟦Tn⟧ in "neu" identisch zu "alt", keine echten Zeilenumbrüche, keine { }.
Geändert werden nur die trans_*.jsonl unter WORK/.sub_work/; danach sub_tool check/inject ausführen.
Gibt die betroffenen Dateien (ohne Endung) aus.
"""
import argparse, glob, json, os, re
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("work")
ap.add_argument("funde", nargs="+")
ap.add_argument("--skip", default="")
ap.add_argument("--dry-run", action="store_true")
a = ap.parse_args()
skip = {s.strip() for s in a.skip.split(",") if s.strip()}
PH = re.compile(r"⟦T\d+⟧")

# Key -> (Arbeitsverzeichnis, Segment-id)
where = {}
for en in glob.glob(os.path.join(a.work, "*.en.ass")):
    work = os.path.join(a.work, ".sub_work", os.path.basename(en)[:-4])
    for i, line in enumerate(open(en, encoding="utf-8-sig"), 1):
        if line.startswith("Dialogue:"):
            where[line.split(",", 9)[8]] = (work, i)

# trans laden: work -> {id: (datei, de)}
trans = {}
def load(work):
    if work not in trans:
        d = {}
        for f in sorted(glob.glob(os.path.join(work, "trans_*.jsonl"))):
            for l in open(f, encoding="utf-8"):
                if l.strip():
                    o = json.loads(l); d[o["id"]] = [f, o["de"]]
        trans[work] = d
    return trans[work]

applied, problems, touched = [], [], set()
for path in a.funde:
    for n, l in enumerate(open(path, encoding="utf-8"), 1):
        if not l.strip():
            continue
        f = json.loads(l)
        key, alt, neu = f["key"], f["alt"], f["neu"]
        tag = f"{os.path.basename(path)}:{n} {key}"
        if key in skip:
            continue
        if key not in where:
            problems.append(f"{tag}: Key unbekannt"); continue
        work, sid = where[key]
        d = load(work)
        if sid not in d:
            problems.append(f"{tag}: keine Übersetzung für id {sid}"); continue
        if d[sid][1] != alt:
            problems.append(f"{tag}: 'alt' passt nicht zur aktuellen Übersetzung"); continue
        if Counter(PH.findall(alt)) != Counter(PH.findall(neu)):
            problems.append(f"{tag}: Platzhalter verändert"); continue
        if "\n" in neu or "{" in neu or "}" in neu or neu == alt or not neu.strip():
            problems.append(f"{tag}: ungültiges 'neu'"); continue
        d[sid][1] = neu
        applied.append(key); touched.add(work)

if not a.dry_run:
    for work in touched:
        by_file = {}
        for sid, (f, de) in trans[work].items():
            by_file.setdefault(f, []).append((sid, de))
        for f in sorted(glob.glob(os.path.join(work, "trans_*.jsonl"))):
            order = [json.loads(l)["id"] for l in open(f, encoding="utf-8") if l.strip()]
            vals = dict(by_file.get(f, []))
            with open(f, "w", encoding="utf-8", newline="\n") as fh:
                for sid in order:
                    fh.write(json.dumps({"id": sid, "de": vals[sid]}, ensure_ascii=False) + "\n")

print(f"angewendet: {len(applied)}{' (Probelauf)' if a.dry_run else ''} | Probleme: {len(problems)}")
for p in problems:
    print("  PROBLEM", p)
for w in sorted(touched):
    print("DATEI", os.path.basename(w)[:-3])
