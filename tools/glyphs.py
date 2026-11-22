"""Prüft, ob alle Zeichen der *.de.ass-Übersetzungen im englischen Spielfont (Silver_EN) vorhanden sind."""
import glob, os, re, sys
from collections import Counter
import UnityPy

work, game = sys.argv[1], sys.argv[2]
aa = os.path.join(game, "D1AL-ogue_Data", "StreamingAssets", "aa", "StandaloneWindows64")
chars = set()
for f in glob.glob(os.path.join(aa, "localization-assets-english*.bundle")):
    for obj in UnityPy.load(f).objects:
        if obj.type.name == "MonoBehaviour":
            t = obj.read_typetree()
            if "m_CharacterTable" in t:
                chars |= {c["m_Unicode"] for c in t["m_CharacterTable"]}
used = Counter()
for f in glob.glob(os.path.join(work, "*.de.ass")):
    for line in open(f, encoding="utf-8-sig"):
        if line.startswith("Dialogue:"):
            text = re.sub(r"<[^>]+>|\\[Nnh]", "", line.split(",", 9)[9].rstrip("\r\n"))
            used.update(text)
missing = {c: n for c, n in used.items() if ord(c) not in chars and c not in " "}
print(f"Font-Zeichen: {len(chars)}, verwendete Zeichen: {len(used)}")
print("FEHLEND:", {f"U+{ord(c):04X} {ascii(c)}": n for c, n in missing.items()} or "keine")
