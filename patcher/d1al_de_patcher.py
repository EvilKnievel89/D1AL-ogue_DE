#!/usr/bin/env python3
"""D1AL-ogue – Deutsche Fan-Übersetzung: Patcher.

Ersetzt die englischen Texte des Spiels durch die deutsche Übersetzung. Dazu wird das englische
String-Table-Bundle (Unity Localization / Addressables) neu geschrieben und im Addressables-Katalog
die CRC-Prüfung für dieses eine Bundle abgeschaltet. Die Originaldateien werden vorher gesichert.

Aufruf:
  D1AL-ogue_DE_Patcher.exe                     interaktives Menü
  D1AL-ogue_DE_Patcher.exe install   [--game PFAD] [--translation DATEI]
  D1AL-ogue_DE_Patcher.exe uninstall [--game PFAD]
  D1AL-ogue_DE_Patcher.exe status    [--game PFAD]
"""
import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import struct
import subprocess
import sys

VERSION = "1.0.2"
GAME_DIR_NAME = "D1AL-ogue"
GAME_EXE = "D1AL-ogue.exe"
AA_REL = os.path.join("D1AL-ogue_Data", "StreamingAssets", "aa")
BUNDLE_NAME = "localization-string-tables-english(unitedstates)(en-us)_assets_all.bundle"
SHARED_NAME = "localization-assets-shared_assets_all.bundle"
BACKUP_DIR_NAME = "_D1AL-ogue_DE_backup"
TRANSLATION_NAME = "D1AL-ogue_DE.json"
BREAK = re.compile(r"\s*\\[Nn]\s*")


class PatchError(Exception):
    pass


# --------------------------------------------------------------------------- Pfade
class Game:
    def __init__(self, root):
        self.root = root
        self.aa = os.path.join(root, AA_REL)
        self.bundle = os.path.join(self.aa, "StandaloneWindows64", BUNDLE_NAME)
        self.shared = os.path.join(self.aa, "StandaloneWindows64", SHARED_NAME)
        self.catalog = os.path.join(self.aa, "catalog.bin")
        self.backup_dir = os.path.join(self.aa, BACKUP_DIR_NAME)
        self.backup_bundle = os.path.join(self.backup_dir, BUNDLE_NAME)
        self.backup_catalog = os.path.join(self.backup_dir, "catalog.bin")
        self.manifest_path = os.path.join(self.backup_dir, "manifest.json")

    def valid(self):
        return all(os.path.isfile(p) for p in (self.bundle, self.shared, self.catalog))

    def manifest(self):
        if os.path.isfile(self.manifest_path):
            with open(self.manifest_path, encoding="utf-8") as fh:
                return json.load(fh)
        return None

    def save_manifest(self, data):
        with open(self.manifest_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)


def steam_libraries():
    """Alle Steam-Bibliotheksordner (Windows-Registry + libraryfolders.vdf)."""
    roots = []
    try:
        import winreg
        for hive, key, val in ((winreg.HKEY_CURRENT_USER, r"Software\Valve\Steam", "SteamPath"),
                               (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath")):
            try:
                with winreg.OpenKey(hive, key) as k:
                    roots.append(os.path.normpath(winreg.QueryValueEx(k, val)[0]))
            except OSError:
                pass
    except ImportError:
        pass
    libs = []
    for r in roots:
        libs.append(r)
        vdf = os.path.join(r, "steamapps", "libraryfolders.vdf")
        if os.path.isfile(vdf):
            with open(vdf, encoding="utf-8", errors="replace") as fh:
                for m in re.finditer(r'"path"\s+"([^"]+)"', fh.read()):
                    libs.append(os.path.normpath(m.group(1).replace("\\\\", "\\")))
    seen, out = set(), []
    for l in libs:
        if l.lower() not in seen:
            seen.add(l.lower())
            out.append(l)
    return out


def find_game(explicit=None):
    candidates = []
    if explicit:
        candidates.append(explicit)
    here = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
    d = here
    for _ in range(4):  # Patcher liegt evtl. im Spielordner oder darunter
        candidates.append(d)
        d = os.path.dirname(d)
    candidates.append(os.getcwd())
    for lib in steam_libraries():
        candidates.append(os.path.join(lib, "steamapps", "common", GAME_DIR_NAME))
    for c in candidates:
        g = Game(os.path.normpath(c))
        if g.valid():
            return g
    if explicit:
        raise PatchError(f"Im angegebenen Ordner wurde D1AL-ogue nicht gefunden:\n  {explicit}")
    return None


# ------------------------------------------------------------------------ Hilfen
def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def game_running():
    if os.name != "nt":
        return False
    try:
        # Ausgabe als Bytes prüfen: tasklist schreibt in der OEM-Codepage (z. B. cp850), nicht UTF-8.
        out = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {GAME_EXE}"], capture_output=True,
                             creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0)).stdout or b""
        return GAME_EXE.lower().encode("ascii") in out.lower()
    except OSError:
        return False


def resource_path(name):
    """Datei neben der .exe hat Vorrang (eigene/neuere Übersetzung), sonst die eingebettete."""
    exe_dir = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
    for d in (exe_dir, os.path.join(exe_dir, "..", "translation"), getattr(sys, "_MEIPASS", "")):
        p = os.path.join(d, name)
        if d and os.path.isfile(p):
            return os.path.normpath(p)
    raise PatchError(f"Übersetzungsdatei {name} nicht gefunden.")


def load_translation(path):
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    if data.get("format") != 1 or "entries" not in data:
        raise PatchError(f"Unbekanntes Format der Übersetzungsdatei: {path}")
    return data


def fix_breaks(original, text):
    """Hat das Original einen Umbruch (Zeichenfolge \\n, von TextMeshPro gerendert), bleiben Umbrüche
    der Übersetzung als \\n erhalten; sonst werden \\N/\\n zu Leerzeichen (das Spiel bricht selbst um).
    {NL}/{CRLF} sind kodierte echte Zeilenumbrüche (News-Texte)."""
    if "\\n" in original:
        text = re.sub(r"\\N", lambda m: "\\n", text)
    else:
        text = BREAK.sub(" ", text).strip()
    return text.replace("\\h", "\u00a0").replace("{CRLF}", "\r\n").replace("{NL}", "\n")


def shared_ids(shared_path):
    import UnityPy
    out = {}
    for obj in UnityPy.load(shared_path).objects:
        if obj.type.name != "MonoBehaviour":
            continue
        t = obj.read_typetree()
        if "m_TableCollectionName" in t and "m_Entries" in t:
            out[t["m_TableCollectionName"]] = {e["m_Key"]: e["m_Id"] for e in t["m_Entries"]}
    return out


def by_table(entries):
    out = {}
    for k, v in entries.items():
        table, key = k.split("|", 1)
        out.setdefault(table, {})[key] = v
    return out


def looks_patched(bundle_path, ids, trans):
    """Erkennt ein bereits übersetztes Bundle (z. B. von einer älteren Patcher-Version ohne Backup)."""
    import UnityPy
    sample = list(trans.get("DialogueTable", {}).items())[:200]
    if not sample:
        return False
    for obj in UnityPy.load(bundle_path).objects:
        if obj.type.name != "MonoBehaviour":
            continue
        t = obj.read_typetree()
        if t.get("m_Name") != "DialogueTable_en-US":
            continue
        cur = {e["m_Id"]: e["m_Localized"] for e in t["m_TableData"]}
        hits = sum(1 for key, de in sample
                   if ids["DialogueTable"].get(key) in cur
                   and cur[ids["DialogueTable"][key]] == fix_breaks(cur[ids["DialogueTable"][key]], de)
                   and de.strip() not in ("...", "…"))
        return hits > len(sample) * 0.3
    return False


# ---------------------------------------------------------------------- Befehle
def install(game, translation_path):
    if game_running():
        raise PatchError("D1AL-ogue läuft gerade. Bitte das Spiel beenden und erneut versuchen.")
    import UnityPy
    data = load_translation(translation_path)
    trans = by_table(data["entries"])
    shown = "eingebaut" if getattr(sys, "_MEIPASS", None) and translation_path.startswith(sys._MEIPASS) else translation_path
    print(f"Übersetzung: {shown} – Version {data.get('version', '?')}, {len(data['entries'])} Einträge")
    ids = shared_ids(game.shared)

    cur_b, cur_c = sha256(game.bundle), sha256(game.catalog)
    man = game.manifest()
    known_b = man and cur_b in (man["orig_bundle_sha256"], man.get("patched_bundle_sha256"))
    known_c = man and cur_c in (man["orig_catalog_sha256"], man.get("patched_catalog_sha256"))
    if man and known_b and known_c and os.path.isfile(game.backup_bundle) and os.path.isfile(game.backup_catalog):
        print("Sicherung der Originaldateien vorhanden.")
    else:
        if man:
            print("Die Spieldateien haben sich seit der letzten Installation geändert (Spiel-Update oder\n"
                  "„Dateien überprüfen“). Die Sicherung wird mit den aktuellen Originalen erneuert.")
        if looks_patched(game.bundle, ids, trans):
            raise PatchError("Die Spieldateien sind bereits übersetzt, es gibt aber keine passende Sicherung.\n"
                             "Bitte in Steam: Rechtsklick auf D1AL-ogue > Eigenschaften > Installierte Dateien >\n"
                             "„Dateien auf Fehler überprüfen“ und den Patcher danach erneut starten.")
        os.makedirs(game.backup_dir, exist_ok=True)
        shutil.copy2(game.bundle, game.backup_bundle)
        shutil.copy2(game.catalog, game.backup_catalog)
        man = {"orig_bundle_sha256": cur_b, "orig_catalog_sha256": cur_c}
        print(f"Originaldateien gesichert: {game.backup_dir}")

    env = UnityPy.load(game.backup_bundle)
    applied, missing = 0, []
    for obj in env.objects:
        if obj.type.name != "MonoBehaviour":
            continue
        t = obj.read_typetree()
        table = t.get("m_Name", "").rsplit("_", 1)[0]
        if table not in trans:
            continue
        rows = {e["m_Id"]: e for e in t["m_TableData"]}
        for key, de in trans[table].items():
            kid = ids.get(table, {}).get(key)
            if kid is None or kid not in rows:
                missing.append(f"{table}|{key}")
                continue
            rows[kid]["m_Localized"] = fix_breaks(rows[kid]["m_Localized"], de)
            applied += 1
        obj.save_typetree(t)
    new_bundle = env.file.save(packer="lz4")

    cat = bytearray(open(game.backup_catalog, "rb").read())
    orig_size = os.path.getsize(game.backup_bundle)
    pat = struct.pack("<I", orig_size)
    hits = [i for i in range(4, len(cat) - 3) if cat[i:i + 4] == pat]
    if len(hits) != 1:
        raise PatchError("Der Addressables-Katalog hat ein unerwartetes Format (Bundle-Eintrag nicht eindeutig).\n"
                         "Vermutlich wurde das Spiel stark verändert – bitte nach einer neuen Patcher-Version schauen.\n"
                         "Es wurde nichts verändert.")
    p = hits[0]
    cat[p - 4:p] = struct.pack("<I", 0)               # CRC 0 = keine Prüfung
    cat[p:p + 4] = struct.pack("<I", len(new_bundle))  # neue Größe

    with open(game.bundle, "wb") as fh:
        fh.write(new_bundle)
    with open(game.catalog, "wb") as fh:
        fh.write(cat)
    man.update({"patcher_version": VERSION, "translation_version": data.get("version"),
                "installed": datetime.datetime.now().isoformat(timespec="seconds"),
                "patched_bundle_sha256": sha256(game.bundle), "patched_catalog_sha256": sha256(game.catalog)})
    game.save_manifest(man)
    print(f"\n{applied} Texte übersetzt.")
    if missing:
        print(f"Hinweis: {len(missing)} Einträge passen nicht zu dieser Spielversion und wurden übersprungen\n"
              f"  (z. B. {', '.join(missing[:5])}). Die betroffenen Texte bleiben englisch.")
    print("Fertig! Im Spiel unter Optionen die Sprache „English“ wählen – die Texte erscheinen auf Deutsch.")


def uninstall(game):
    if game_running():
        raise PatchError("D1AL-ogue läuft gerade. Bitte das Spiel beenden und erneut versuchen.")
    man = game.manifest()
    if not man:
        print("Die deutsche Übersetzung ist nicht installiert (keine Sicherung gefunden).")
        return
    cur_b, cur_c = sha256(game.bundle), sha256(game.catalog)
    if cur_b == man.get("patched_bundle_sha256") and cur_c == man.get("patched_catalog_sha256"):
        shutil.copy2(game.backup_bundle, game.bundle)
        shutil.copy2(game.backup_catalog, game.catalog)
        print("Originaldateien wiederhergestellt.")
    else:
        print("Die Spieldateien sind nicht (mehr) vom Patcher verändert – vermutlich durch ein Steam-Update\n"
              "oder „Dateien überprüfen“. Es wird nichts zurückkopiert.")
    shutil.rmtree(game.backup_dir, ignore_errors=True)
    print("Sicherung entfernt. Das Spiel ist wieder im Originalzustand (Englisch).")


def status(game):
    man = game.manifest()
    print(f"Spielordner: {game.root}")
    if not man:
        print("Status: nicht installiert (Original).")
        return
    cur_b = sha256(game.bundle)
    if cur_b == man.get("patched_bundle_sha256"):
        print(f"Status: Deutsch installiert (Übersetzung {man.get('translation_version')}, "
              f"Patcher {man.get('patcher_version')}, {man.get('installed')}).")
    elif cur_b == man.get("orig_bundle_sha256"):
        print("Status: Original (Sicherung vorhanden, Übersetzung nicht aktiv).")
    else:
        print("Status: Spieldateien wurden geändert (Update?). Bitte „Installieren“ erneut ausführen.")


# ------------------------------------------------------------------------ Start
def resolve_game(arg):
    game = find_game(arg)
    if game:
        return game
    print("D1AL-ogue wurde nicht automatisch gefunden.")
    if sys.stdin and sys.stdin.isatty():
        path = input("Bitte den Spielordner eingeben (z. B. C:\\Steam\\steamapps\\common\\D1AL-ogue):\n> ").strip('" ')
        return find_game(path)
    raise PatchError("Spielordner mit --game angeben.")


def menu(args):
    print(f"D1AL-ogue – Deutsche Fan-Übersetzung (Patcher {VERSION})\n")
    game = resolve_game(args.game)
    status(game)
    choice = input("\n[1] Installieren / aktualisieren\n[2] Deinstallieren (Original wiederherstellen)\n"
                   "[Q] Beenden\n> ").strip().lower()
    if choice == "1":
        install(game, args.translation or resource_path(TRANSLATION_NAME))
    elif choice == "2":
        uninstall(game)


def main():
    if not sys.stdout.isatty():  # umgeleitete Ausgabe (Log-Datei, Pipe) als UTF-8
        sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="D1AL-ogue – Deutsche Fan-Übersetzung (Patcher)")
    ap.add_argument("command", nargs="?", choices=["install", "uninstall", "status"])
    ap.add_argument("--game", help="Spielordner (Standard: automatisch über Steam suchen)")
    ap.add_argument("--translation", help=f"Übersetzungsdatei (Standard: {TRANSLATION_NAME})")
    ap.add_argument("--version", action="version", version=VERSION)
    args = ap.parse_args()
    interactive = args.command is None
    try:
        if interactive:
            menu(args)
        else:
            game = resolve_game(args.game)
            if args.command == "install":
                install(game, args.translation or resource_path(TRANSLATION_NAME))
            elif args.command == "uninstall":
                uninstall(game)
            else:
                status(game)
        code = 0
    except PatchError as e:
        print(f"\nFEHLER: {e}")
        code = 1
    except KeyboardInterrupt:
        code = 130
    if interactive:
        try:
            input("\nEnter drücken zum Schließen …")
        except EOFError:
            pass
    sys.exit(code)


if __name__ == "__main__":
    main()
