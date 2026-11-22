"""Exportiert die Texttabellen aus der eigenen Spielinstallation nach <arbeitsordner>/quelle/.

Aufruf: python tools/extract_tables.py <spielordner> <arbeitsordner>

Erzeugt:
- <Tabelle>.csv für alle Unity-Localization-String-Tables (Spalten: key + alle Sprachen),
  Keys über die SharedTableData aufgelöst.
- Dialogue_TextAsset.csv, Guest.csv, News.csv aus resources.assets (Entwickler-CSV mit Sprecher,
  Szenentyp und Kunden-Zuordnung – nötig für make_ass.py).

Die Dateien enthalten die Originaltexte des Spiels und gehören NICHT ins Repository (.gitignore).
Muss mit einer UNVERÄNDERTEN Spielinstallation laufen (vorher ggf. Patcher > Deinstallieren).
"""
import csv, glob, os, sys
import UnityPy

game, work = sys.argv[1], sys.argv[2]
aa = os.path.join(game, "D1AL-ogue_Data", "StreamingAssets", "aa", "StandaloneWindows64")
out = os.path.join(work, "quelle")
os.makedirs(out, exist_ok=True)

# Keys der String-Tables
shared = {}
for obj in UnityPy.load(os.path.join(aa, "localization-assets-shared_assets_all.bundle")).objects:
    if obj.type.name == "MonoBehaviour":
        t = obj.read_typetree()
        if "m_Entries" in t and "m_TableCollectionName" in t:
            shared[t["m_TableCollectionName"]] = {e["m_Id"]: e["m_Key"] for e in t["m_Entries"]}

tables, locales = {}, []
for f in sorted(glob.glob(os.path.join(aa, "localization-string-tables-*.bundle"))):
    for obj in UnityPy.load(f).objects:
        if obj.type.name != "MonoBehaviour":
            continue
        t = obj.read_typetree()
        coll, loc = t["m_Name"].rsplit("_", 1)
        if loc not in locales:
            locales.append(loc)
        keys = shared.get(coll, {})
        d = tables.setdefault(coll, {})
        for e in t["m_TableData"]:
            d.setdefault(keys.get(e["m_Id"], str(e["m_Id"])), {})[loc] = e["m_Localized"]
for coll, d in tables.items():
    with open(os.path.join(out, coll + ".csv"), "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.writer(fh)
        w.writerow(["key"] + locales)
        for k, v in d.items():
            w.writerow([k] + [v.get(l, "") for l in locales])
    print(f"{coll}.csv: {len(d)} Einträge")

# Entwickler-CSVs (TextAssets)
wanted = {"Dialogue": "Dialogue_TextAsset.csv", "Guest": "Guest.csv", "News": "News.csv"}
env = UnityPy.load(os.path.join(game, "D1AL-ogue_Data", "resources.assets"))
for obj in env.objects:
    if obj.type.name != "TextAsset":
        continue
    d = obj.read()
    if d.m_Name in wanted:
        data = d.m_Script
        raw = data.encode("utf-8", "surrogateescape") if isinstance(data, str) else bytes(data)
        with open(os.path.join(out, wanted[d.m_Name]), "wb") as fh:
            fh.write(raw)
        print(f"{wanted[d.m_Name]}: {len(raw)} Bytes")
