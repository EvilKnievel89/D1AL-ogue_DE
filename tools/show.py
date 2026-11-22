"""Zeigt Segmente (EN und, falls vorhanden, DE) nach Datei-Präfix und Segment-id.
Aufruf: python show.py <arbeitsordner> S01E03:83 S01E08:218-221 ..."""
import glob, json, os, re, sys

W = sys.argv[1]
for spec in sys.argv[2:]:
    pre, rng = spec.split(":")
    a, _, b = rng.partition("-")
    a, b = int(a), int(b or a)
    work = glob.glob(os.path.join(W, ".sub_work", pre + "*"))[0]
    trans = {}
    for f in glob.glob(os.path.join(work, "trans_*.jsonl")):
        for line in open(f, encoding="utf-8"):
            if line.strip():
                o = json.loads(line); trans[o["id"]] = o["de"]
    for line in open(os.path.join(work, "seg.jsonl"), encoding="utf-8"):
        s = json.loads(line)
        if a <= s["id"] <= b:
            print(f'{pre}:{s["id"]} [{s["name"]}] {s["src"]}')
            if s["id"] in trans:
                print(f'{" " * (len(pre) + 1)}DE: {trans[s["id"]]}')
