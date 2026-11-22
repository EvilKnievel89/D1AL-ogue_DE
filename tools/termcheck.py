"""Zählt, wie Begriffe in den *.de.ass übersetzt wurden (pro Datei), um Inkonsistenzen zwischen Paketen zu finden.
Aufruf: python termcheck.py <arbeitsordner> "Regex1" "Regex2" ..."""
import glob, os, re, sys
from collections import Counter

W = sys.argv[1]
pats = [re.compile(p) for p in sys.argv[2:]]
for f in sorted(glob.glob(os.path.join(W, "*.de.ass"))):
    c = Counter()
    for line in open(f, encoding="utf-8-sig"):
        if line.startswith("Dialogue:"):
            text = line.split(",", 9)[9]
            for p in pats:
                for m in p.finditer(text):
                    c[m.group(0)] += 1
    if c:
        print(os.path.basename(f)[:28].ljust(28), dict(c))
