"""Erzeugt aus den Spieltabellen ASS-Dateien für den Untertitel-Agenten.

Aufruf: python make_ass.py <arbeitsordner>
- Effect-Feld = "Tabelle|Key" im Bundle (wird von patch_bundle.py beim Zurückschreiben benutzt).
- Name-Feld = Sprecher, Style = Szenentyp.
- Bereits vorhandene *.en.ass werden NICHT überschrieben (an ihnen hängen Segmente/Übersetzungen).
- Prüft, dass jede Dialogzeile genau einer Datei zugeordnet ist.
"""
import csv, os, re, sys
from collections import defaultdict, OrderedDict

W = sys.argv[1]
Q = os.path.join(W, "quelle")
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
read = lambda name, enc="utf-8-sig": list(csv.DictReader(open(os.path.join(Q, name), encoding=enc, newline="")))

# --- Dialogzeilen (Sprecher/Typ aus der Original-CSV, Text + Key aus dem Bundle) -------------
rows = read("Dialogue_TextAsset.csv", "utf-8")
pool = defaultdict(list)
for t in ("DialogueTable", "CommentDialogueTable", "CutScene"):
    for r in read(t + ".csv"):
        pool[r["key"].split("_")[0]].append([t, r["key"], r["en-US"], False])
for r in rows:
    c = [e for e in pool[r["Key"]] if not e[3] and norm(e[2]) == norm(r["Dialogue_ENG"])]
    c[0][3] = True
    r["_table"], r["_key"], r["_en"] = c[0][0], c[0][1], c[0][2]
assert not [e for v in pool.values() for e in v if not e[3]], "Bundle-Einträge ohne Zuordnung"

NAMES = {"CHAR_CHRIS": "Chris", "CHAR_MICHELLE": "Michelle", "CHAR_PRAY": "Pray", "CHAR_ORCA": "Orca",
         "CHAR_LIANNE": "Lianne", "CHAR_BLADE": "Blade", "CHAR_UNKNOWN": "???",
         "CHAR_NONE": "Erzaehler (Chris)", "CHAR_REQUEST": "Auftragstitel", "": "Chris (Monolog)"}
CREDIT_SPK = re.compile(r"^<color=[^>]*>([^<]+)</color>\s*:")

HDR = ("[Script Info]\nTitle: {t}\nScriptType: v4.00+\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize\n"
       "Style: Default,Arial,20\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")


def write(fn, title, items):
    path = os.path.join(W, fn)
    if os.path.exists(path):
        print(f"{fn}: existiert – übersprungen")
        return
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(HDR.format(t=title))
        for i, (style, name, eff, text) in enumerate(items):
            # Echte Zeilenumbrüche (nur in News-Texten) als geschützte Marke; patch_bundle.py stellt sie wieder her.
            text = text.replace("\r\n", "{CRLF}").replace("\n", "{NL}")
            assert "\r" not in text, (eff, text)
            s, e = f"0:{i // 60:02d}:{i % 60:02d}.00", f"0:{i // 60:02d}:{i % 60:02d}.90"
            f.write(f"Dialogue: 0,{s},{e},{style},{name},0,0,0,{eff},{text}\n")
    print(f"{fn}: {len(items)} Zeilen")


def style_of(r):
    k = r["Key"]
    if k.startswith("8"):
        return "Ending_Figur"
    if k.startswith("9"):
        return "Abspann"
    return r["Type"] or "CutScene"


def speaker_of(r):
    if r["Key"].startswith("9"):
        m = CREDIT_SPK.match(r["_en"])
        return m.group(1).strip() if m else "Abspann"
    return NAMES[r["Name"]]


# --- Folgen: Intro + je Kundenbesuch (GuestKey), dann Enden ------------------------------------
guests = OrderedDict((g["Key"], g) for g in read("Guest.csv", "utf-8"))
short = {"CHAR_MICHELLE": "Michelle", "CHAR_PRAY": "Pray", "CHAR_ORCA": "Orca", "CHAR_LIANNE": "Lianne",
         "CHAR_BLADE": "Blade"}
episodes = OrderedDict()
n = 0
for gk, g in guests.items():
    if g["Name"] == "Ending":
        continue
    n += 1
    label = f"S01E{n:02d}_{'Intro_' if n == 1 else ''}Tag{g['Day']}_{short[g['Name']]}"
    episodes[label] = lambda r, gk=gk, first=(n == 1): r["GuestKey"] == gk or (first and r["Key"] == "30001")
episodes[f"S01E{n + 1:02d}_Ende_Polarnacht"] = lambda r: r["GuestKey"] == "51015"
episodes[f"S01E{n + 2:02d}_Ende_Figuren"] = lambda r: r["Key"].startswith("8")
episodes[f"S01E{n + 3:02d}_Abspann"] = lambda r: r["Key"].startswith("9")

assigned = defaultdict(list)
for label, pred in episodes.items():
    for i, r in enumerate(rows):
        if pred(r):
            assigned[i].append(label)
lost = [rows[i]["Key"] for i in range(len(rows)) if len(assigned[i]) != 1]
assert not lost, f"Zeilen nicht genau einer Folge zugeordnet: {sorted(set(lost))[:20]}"

for label, pred in episodes.items():
    write(label + ".en.ass", label,
          [(style_of(r), speaker_of(r), f'{r["_table"]}|{r["_key"]}', r["_en"]) for r in rows if pred(r)])

# --- Weitere Tabellen ---------------------------------------------------------------------------
write("S00E01_Menue.en.ass", "Menue",
      [("Sign_UI", "UI", f'TitleTables|{r["key"]}', r["en-US"]) for r in read("TitleTables.csv")])
write("S00E02_Tutorial.en.ass", "Tutorial",
      [("Tutorial", "Chris", f'TutorialDialogueTable|{r["key"]}', r["en-US"]) for r in read("TutorialDialogueTable.csv")])
grade = {"C3": "Kommentar_Gut", "C2": "Kommentar_Normal", "C1": "Kommentar_Schlecht"}
write("S00E03_Kommentare.en.ass", "Kundenkommentare",
      [(grade.get(r["key"].split("_")[-1], "Kommentar"), NAMES[guests[r["key"].split("_")[0]]["Name"]],
        f'CommentTable|{r["key"]}', r["en-US"]) for r in read("CommentTable.csv")])
write("S00E04_News.en.ass", "News",
      [("News_Titel" if "SUBJECT" in r["key"] else "News_Text", "News", f'NewsTable|{r["key"]}', r["en-US"])
       for r in read("NewsTable.csv")])
