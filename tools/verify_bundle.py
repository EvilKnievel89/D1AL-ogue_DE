"""Vergleicht gepatchtes Bundle mit dem Backup: Struktur je Eintrag (echte Umbrüche, \\n, Tags, {0}) muss gleich sein.
Aufruf: python verify_bundle.py <arbeitsordner> <spielordner>"""
import os, re, sys
from collections import Counter
import UnityPy

work, game = sys.argv[1:3]
NAME = "localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle"
orig_p = os.path.join(work, "backup", NAME)
new_p = os.path.join(game, "D1AL-ogue_Data", "StreamingAssets", "aa", "StandaloneWindows64", NAME)


def tables(path):
    out = {}
    for o in UnityPy.load(path).objects:
        if o.type.name == "MonoBehaviour":
            t = o.read_typetree()
            out[t["m_Name"]] = {e["m_Id"]: e["m_Localized"] for e in t["m_TableData"]}
    return out


def shape(s):
    return (s.count("\n"), s.count("\\n"), tuple(sorted(Counter(re.findall(r"<[^>]+>|\{\d\}", s)).items())))


o, n = tables(orig_p), tables(new_p)
bad, same, total = [], Counter(), 0
for name, entries in o.items():
    for k, v in entries.items():
        total += 1
        w = n[name][k]
        if v == w and v.strip():
            same[name] += 1
        if shape(v) != shape(w):
            bad.append((name, k, shape(v), shape(w), w[:80]))
print(f"Einträge: {total} | Struktur abweichend: {len(bad)}")
print("unverändert (identisch mit Englisch) je Tabelle:", dict(same))
for b in bad[:15]:
    print("  ", b[0], b[1], "orig", b[2][:2], "neu", b[3][:2], ascii(b[4]))
