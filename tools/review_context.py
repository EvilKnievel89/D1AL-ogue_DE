"""Zeigt zu Korrekturvorschlägen die Nachbarzeilen (DE) und ob der alte Text noch an anderer Stelle vorkommt.
Aufruf: python tools/review_context.py WORK FUNDE.jsonl [...] [--keys K1,K2]"""
import glob, json, os, sys

W = sys.argv[1]
args = [x for x in sys.argv[2:] if not x.startswith("--keys")]
only = set()
for x in sys.argv[2:]:
    if x.startswith("--keys="):
        only = set(x[7:].split(","))
order, text = [], {}
for f in sorted(glob.glob(os.path.join(W, "*.de.ass"))):
    for line in open(f, encoding="utf-8-sig"):
        if line.startswith("Dialogue:"):
            p = line.rstrip("\r\n").split(",", 9)
            order.append(p[8]); text[p[8]] = (p[4], p[9])
pos = {k: i for i, k in enumerate(order)}
for path in args:
    for l in open(path, encoding="utf-8"):
        if not l.strip():
            continue
        f = json.loads(l)
        k = f["key"]
        if only and k not in only:
            continue
        i = pos[k]
        same = [o for o in order if o != k and text[o][1] == text[k][1]]
        print(f"== {k}  (gleicher DE-Text an {len(same)} weiteren Stellen{': ' + ', '.join(same[:4]) if same else ''})")
        for j in range(max(0, i - 1), min(len(order), i + 2)):
            m = "NEU" if j == i else "   "
            spk, de = text[order[j]]
            print(f"  {m} [{spk}] {f['neu'] if j == i else de}")
