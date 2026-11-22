"""Qualitätscheck: vergleicht *.en.ass mit *.de.ass (Länge, eingefügte Umbrüche, Duplikat-Konsistenz)."""
import glob, os, re, sys
from collections import defaultdict

W = sys.argv[1]
sample = sys.argv[2] if len(sys.argv) > 2 else None   # z. B. "S01E02:11-30"
DLG = re.compile(r"^Dialogue:\s*(.*)$")


def load(path):
    out = {}
    for line in open(path, encoding="utf-8-sig"):
        m = DLG.match(line.rstrip("\r\n"))
        if m:
            p = m.group(1).split(",", 9)
            out[p[8]] = (p[4], p[9])
    return out


plain = lambda s: re.sub(r"<[^>]+>|\{[^}]*\}", "", s)
for en_path in sorted(glob.glob(os.path.join(W, "*.en.ass"))):
    de_path = en_path.replace(".en.ass", ".de.ass")
    if not os.path.exists(de_path):
        continue
    en, de = load(en_path), load(de_path)
    name = os.path.basename(en_path)[:6]
    breaks = [k for k in en if "\\N" in de[k][1] and "\\N" not in en[k][1] and "\\n" not in en[k][1]]
    long_ = [(k, len(plain(de[k][1])) / max(1, len(plain(en[k][1]))))
             for k in en if len(plain(en[k][1])) >= 20 and len(plain(de[k][1])) > 1.6 * len(plain(en[k][1]))]
    same_src = defaultdict(set)
    for k in en:
        same_src[en[k][1]].add(de[k][1])
    incons = [s for s, v in same_src.items() if len(v) > 1]
    tot_en = sum(len(plain(v[1])) for v in en.values()); tot_de = sum(len(plain(v[1])) for v in de.values())
    print(f"{name}: {len(en)} Zeilen | Länge DE/EN {tot_de / tot_en:.2f} | eingefügte \\N: {len(breaks)} "
          f"| >160 %: {len(long_)} | gleiche Quelle, versch. Übersetzung: {len(incons)}")
    for k, r in long_[:3]:
        print(f"    lang {r:.1f}x {k}: {plain(de[k][1])[:110]}")
    for s in incons[:3]:
        print(f"    inkonsistent: {s[:50]} -> {list(same_src[s])[:2]}")
    if sample and name == sample.split(":")[0]:
        a, b = map(int, sample.split(":")[1].split("-"))
        for i, k in enumerate(en):
            if a <= i + 1 <= b:
                print(f"  [{en[k][0]}] {en[k][1]}\n  {'':{len(en[k][0]) + 2}} {de[k][1]}")
