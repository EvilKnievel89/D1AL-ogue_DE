# Glossar – D1AL-ogue

Verbindlich für alle Folgen der Serie. Vom Nutzer korrigierte Einträge haben Vorrang vor allem anderen.

## Kontext (wichtig – kein Anime, sondern ein Videospiel)
- D1AL-ogue ist ein koreanisches Indie-Spiel (Cyberpunk, Puzzle + Visual Novel). Quelle ist die **offizielle englische Fassung**. Chris betreibt die Reparaturklinik „D1AL-ogue“ in Chroma City und wartet E.V.Es (Androiden/Cyborg-Kundinnen). Ton: locker, trocken-humorvoll, teils derb und anzüglich.
- Jede „Folge“ ist **ein Kundenbesuch**, die Dateien sind künstlich aus den Spieltabellen erzeugt. Timing ist bedeutungslos.
- Das Feld **Effect** (`Tabelle|Key`) ist die Zuordnung zur Spieldatei und wird vom Skript unverändert übernommen – nicht beachten.
- **Styles** sind Szenentypen des Spiels, keine Untertitel-Styles: alle `übersetzen`, außer `Sign_UI` (siehe unten).

## Konventionen
- **Ein Segment = ein Textfenster im Spiel.** Sätze laufen oft über mehrere aufeinanderfolgende Segmente („…where Ohara“ / „completely smashed…“). Inhalt darf **nicht** zwischen Segmenten verschoben werden. Deutschen Satzbau so wählen, dass jedes Segment für sich lesbar ist und die Teile hintereinander einen natürlichen Satz ergeben (notfalls umstellen, z. B. Verb früher bringen).
- **Kein `\N` einfügen.** Das Spiel bricht selbst um; eingefügte `\N` werden beim Zurückschreiben zu Leerzeichen.
- **Länge:** Deutsch darf länger sein, aber nicht ausufern – möglichst ≤ 130 % der englischen Länge.
- **Tags** wie `<color=#…>…</color>`, `<shake …>`, `<bounce …>` erscheinen als Platzhalter ⟦Tn⟧ – an der sinngemäß passenden Stelle behalten (gefärbtes/wackelndes Wort bleibt eingefasst). `{0}`, `{1}` in Menütexten ebenso.
- **Honorifika:** kommen nicht vor – keine erfinden.
- Anrede: du als Default; Sie nur bei klarer Höflichkeits-/Hierarchiesituation. Einmal festgelegt → für dieses Figurenpaar konstant (Wechsel nur, wenn die Beziehung sich erkennbar ändert – mit Folgenangabe).
- Anführungszeichen: „…“; englische einfache Anführungszeichen für Titel ('Buff Girl Ohara') → „…“.
- Eigennamen (Figuren, Orte, Firmen, Produkte) unverändert, sofern das Glossar nichts anderes sagt.
- **Sprecher-Feld:** `Erzaehler (Chris)` = Erzähltext/innere Gedanken aus Chris' Sicht (Präteritum, Ich-Perspektive bzw. Beschreibung). `Chris (Monolog)` = Chris' Brief/Monolog an Michelle im Intro. `Auftragstitel` = Überschrift eines Kundenauftrags im Format „[Prays Auftrag] …“ – knapp halten. `???` = noch unbekannte Figur.
- Zeilen in `( … )` sind Chris' Gedanken – Klammern behalten.
- Stöhn-/Schmerzlaute (Szenentyp `Sub`, „Nngh“, „Ahn“): deutsch lautmalerisch („Mmh“, „Ngh“, „Ah…“), nicht wörtlich erklären.
- **Menütexte (`Sign_UI`):** kurze Schaltflächen/Titel, so knapp wie möglich, übliche deutsche Spiel-UI-Begriffe (Start, Laden, Optionen, Fortsetzen …).

## Styles
Behandlung: `übersetzen` | `Sign` (feste Box, knapp halten) | `auslassen`

| Style | Behandlung | Bemerkung |
|---|---|---|
| CutScene | übersetzen | Zwischensequenz/Intro |
| StartMain | übersetzen | Gespräch vor der Reparatur |
| ClearMain | übersetzen | Gespräch nach der Reparatur |
| Comment_Good / Comment_Normal / Comment_Bad | übersetzen | alternative Reaktionen je nach Reparaturergebnis (gut/mittel/schlecht) |
| Sub | übersetzen | Laute während der Reparatur |
| Repair1 / Repair2 | übersetzen | Smalltalk während der Reparatur |
| WorkBefore | übersetzen | Chris' Gedanken am Morgen |
| Sign_UI | Sign | Menü-/Oberflächentexte |
| Ending | übersetzen | Polarnacht-Tag, gemeinsames Ende (inkl. Auswahl, wen Chris besucht) |
| Ending_Figur | übersetzen | Ende mit der gewählten Figur (Pray/Lianne/Orca/Michelle) |
| Abspann | übersetzen | Kurzszenen im Abspann, Sprecher steht im Text (siehe unten) |
| Tutorial | übersetzen | Puzzle-Anleitung, Chris erklärt (sich selbst/dem Spieler) |
| Kommentar_Gut / Kommentar_Normal / Kommentar_Schlecht | übersetzen | Kundenkommentar nach der Reparatur je nach Ergebnis; Sprecher = Kundin |
| News_Titel | übersetzen | Schlagzeile, knapp, Zeitungsstil |
| News_Text | übersetzen | Zeitungsartikel, lang – keine Längenbegrenzung |

## Konventionen für Abspann, News, Tutorial, Kommentare
- **Abspann:** Jede Zeile beginnt mit `⟦T0⟧Name⟦T1⟧ : ` – Name und „ : “ **unverändert** lassen, nur den Text danach übersetzen.
- **News:** `⟦Tn⟧`-Platzhalter stehen hier auch für echte Absätze (`{NL}`) und Ausrichtungs-Tags – alle an derselben Stelle behalten (Absatzstruktur 1:1). Vorhandene `\n` beibehalten, keine neuen einfügen. Deutscher Nachrichtenstil (sachlich, Präteritum/Präsens wie in der Quelle, indirekte Rede mit Konjunktiv). Byline „By Waifu Matin Press (WMP)“ → „Von Waifu Matin Press (WMP)“. Schlagzeilen im typischen Zeitungsstil („Hype um …“, „[Exklusiv]“, „[Bekanntmachung]“). Eigennamen/Organisationen laut Glossar.
- **Tutorial:** Chris spricht den Spieler bzw. sich selbst mit **du** an, locker-erklärend („Zieh ein Modul …“, „Lass uns …“). Vorhandene `\n` beibehalten. Puzzle-Begriffe konsistent mit dem Menü (Fusionen, Zielzüge …); Bauteile englisch (Power/Neural/Logic Unit).
- **Kommentare:** kurze Zitate der Kundin in ihrer Sprechweise; die Anführungszeichen der Quelle als „…“ wiedergeben.

## Weitere Festlegungen (aus der Analyse)
- **Comment_Normal und Comment_Bad sind im Original oft wortgleich** → dann auch wortgleich übersetzen (gleicher Text = gleiche Übersetzung, Zeichen für Zeichen).
- **Wiederholte identische Zeilen** (auch Menü-Duplikate) immer identisch übersetzen.
- **Offensichtliche Fehler der englischen Quelle** („we gets“, fehlender Punkt, „Oblivious“ groß, „E.V.Es..“, verwaiste Anführungszeichen, „a some“) stillschweigend korrigieren. Schreibvarianten vereinheitlichen: „D1al-ogue“/„D1alogue“ → „D1AL-ogue“, „E.V.E.s“ → „E.V.Es“, „O'Hara“ → „Ohara“, „Sunshine Corp.“ → „Sunshine Corp“.
- **Rückbezüge innerhalb einer Folge** (gleiches Wort wird später zitiert, z. B. „attached“, „it wasn't my business“, „as far as I can remember“, „dazed and refreshed“) immer mit demselben deutschen Wortlaut.
- `*Wort*` (Sternchen-Betonung in der Quelle) beibehalten.
- **Wortspiele mit Doppeldeutigkeit** (z. B. „wet themselves“/Kühlmittel, „chips“, „main event“, „service“, „creaky“/Dial, „Neon Sign“→„Neon Shine“, Re:tro-jan/Trojaner): Pointe auf Deutsch erhalten, Rückbezüge in Folgezeilen müssen dasselbe Wort aufgreifen (z. B. „Was meinst du mit ‚Hauptakt‘?“).
- **Sprecher `???`** = Figur, deren Name erst später fällt (S01E04 49–54: Lianne; S01E05 11–52: Blade). Anrede wie für die jeweilige Figur.
- **Sprechweisen:** Chris trocken, selbstironisch, Understatement; Michelle derb-sarkastisch, kratzbürstig-fürsorglich; Pray frech, spöttisch, theatralisch bei Serienzitaten; Orca höflich, beflissen, naiv-mitteilsam, technikbegeistert; Lianne verspielt, flirtend, anzüglich, emotional schwankend; Blade vulgär, herablassend, großspurig.
- **Erzähltext** (`Erzaehler (Chris)`): Präteritum, Ich-Perspektive.
- **Auftragstitel:** „[Prays Auftrag] …“, „[Orcas Auftrag] …“, „[Liannes Auftrag] …“, „[Blades Auftrag] …“ – Imperativ/Nominalstil, knapp.
- **Dialogauswahl-Titel** wie „[Practice Repair] …“ → „[Übungsreparatur] …“.

## Figuren
| Figur (Schreibweise) | Beschreibung | erste Folge |
|---|---|---|
| Chris | Ich-Erzähler, Betreiber der Reparaturklinik D1AL-ogue | S01E01 |
| Michelle | Chris' jüngere Schwester, chattet/telefoniert mit ihm; Eltern „Mom and Dad“ → „Mama und Papa“. **Spoiler:** die echte Michelle ist tot, die Michelle im Chat ist eine von Chris geschaffene KI (E13, E15, E16: „Michelle is dead“ / „But I am Michelle“). Anrede bleibt du. Chris weiß lange nicht, wo sie „wohnt“ – Plotpunkt erhalten. Nennt Pray spöttisch „Fly“ → „Fliege“ | S01E01 |
| Nina | Prays Chefin im Café; „Boss“ → „Chefin“ (auch rückwirkend: Prays Boss ist immer Nina) | S01E18 |
| Cinderella | Selbstjustiz-Phantom mit Glasschuhen (Glasschuh, Stiletto-Absatz); Geschlecht/Anzahl offen – Quelle „they“ → „sie“ (bewusst mehrdeutig), Name unverändert; Forum „Cinderella, Help!“ unverändert | S01E06 |
| Mayor Lucas | Bürgermeister Lucas | S00E04 |
| Pray (Pray Emery) | E.V.E, Stammkundin, arbeitet im Café gegenüber, Katze Remy | S01E02 |
| Orca (Orca O. Ohara) | E.V.E, TN-DLS-Rettungsmodell mit Schwanz, Scarlet Response Unit | S01E03 |
| Lianne | E.V.E mit Emotionsmodul, Forscherin in einer Pharmafirma | S01E04 |
| Blade (Blade Hamilton) | männlicher Kunde mit optischer Tarnung, vulgär, gefährlich | S01E05 |
| Remy | Prays Katze | S01E02 |
| Ohara, Mrs. Blind | Figuren der Serie „Buff Girl Ohara“ | S01E02 |
| Dokim | Streamer | S01E04 |

## Anrede
| Sprecher | spricht mit | du/Sie | Honorifikum | Bemerkung |
|---|---|---|---|---|
| Chris | Michelle | du | – | Geschwister |
| Michelle | Chris | du | – | |
| Chris | Pray | du | – | S01E02 215 „valued customer Pray Emery“ = ironisch übertriebene Wortwahl, trotzdem du |
| Pray | Chris | du | – | |
| Chris | Orca | du | – | |
| Orca | Chris | du | „Manager“ → „Chef“ | höflich-beflissen im Ton, aber du; später nur noch „Chris“ |
| Chris | Lianne | du | – | |
| Lianne | Chris | du | – | |
| Chris | Blade | **Sie** | „Sir“ → keine Entsprechung (nur Sie-Form), „Mr. Blade“ → „Herr Blade“ | bewusste Distanz |
| Blade | Chris | du | „kid“ → „Kleiner“ | herablassend, Asymmetrie beibehalten; Spitznamen „pale kid“ → „Bleichgesicht“, „hothouse flower“ → „Treibhauspflänzchen“, „rich boy“ → „Bonzensöhnchen“, „sickly mug“ → „kränkliche Visage“ |
| Chris | Blade (ab S01E09) | Sie | – | bleibt Sie, auch wenn Chris frecher wird |
| Nina | Pray | du | – | Chefin, resolut |
| Pray | Nina | du | „Boss“ → „Chefin“ | |
| Behörden/Bekanntmachungen | Bürger | Sie/euch | – | amtliche Durchsagen (USA, Neon-Net) siezen; The Noise duzt kollektiv („ihr“) |
| Alle Paare | (bis zum Ende) | unverändert | – | Beziehungen werden in E17 romantisch/vertrauter – Anrede bleibt du |
| Chris | Kundschaft allgemein / Unbekannte | du | – | außer klar förmlicher Rahmen |

## Begriffe
Art: Ort, Organisation, Attacke/Technik, Gegenstand, Running Gag, Anspielung, Sonstiges

| Original | Deutsch | Art | Bemerkung |
|---|---|---|---|
| Repair Clinic D1AL-ogue | Reparaturklinik D1AL-ogue | Ort | Name der Klinik bleibt; „repair clinic“ allgemein → „Reparaturklinik“ |
| Chroma City | Chroma City | Ort | |
| Luminance City | Luminance City | Ort | |
| E.V.E / E.V.Es | E.V.E / E.V.Es | Sonstiges | Plural unverändert lassen; grammatisch feminin („die E.V.E“) |
| Polarnight Day | Polarnacht-Tag | Sonstiges | Feiertag der Stadt (vom Nutzer bestätigt) |
| Chromatic Zenith | Chromatic Zenith | Sonstiges | Holo-Panorama, unverändert |
| Gray Night | „Graue Nacht“ | Sonstiges | |
| Sunshine Corp | Sunshine Corp | Organisation | |
| Neon Shine | Neon Shine | Sonstiges | Licht-Abo; „subscription fee“ → „Abogebühr“ |
| Stability Officers | Stability Officers | Organisation | Ordnungskräfte, unverändert |
| Chroma City Urban Recovery Agency | unverändert | Organisation | |
| Scarlet Response Unit | unverändert | Organisation | |
| Sunshine Corp manager („bigshot“) | Bonze / hohes Tier von Sunshine Corp | Sonstiges | |
| district manager | Bezirksleiter | Sonstiges | |
| TN-DLS, D1AL, D5AL, DXAL | unverändert | Gegenstand | Modell-/Gerätebezeichnungen |
| Dial (Gerät), 1st gen / 5th gen | Dial, 1. Generation / 5. Generation | Gegenstand | |
| Power Unit / Neural Unit / Logic Unit / Synaptic Unit | Power Unit / Neural Unit / Logic Unit / Synaptic Unit | Gegenstand | Spielbauteile, englisch lassen (auch im Menü); „Tier 2 Power Unit“ → „Tier-2-Power-Unit“ |
| unit synthesis / synthesize | Unit-Synthese / synthetisieren | Technik | |
| Practice Repair / Mock Repair | Übungsreparatur | Sonstiges | |
| Request (Auftrag eines Kunden) | Auftrag | Sonstiges | „Accept Request“ → „Auftrag annehmen“ |
| LDS / Light Deficiency Syndrome | LDS / Lichtmangel-Syndrom | Sonstiges | Abkürzung bleibt |
| Blackouts / Blackout phenomenon | Blackouts / Blackout-Phänomen | Sonstiges | Krankheitsstufe |
| Flicker (patients) | Flicker-Patienten | Sonstiges | Drogenkranke |
| zombies | Zombies | Sonstiges | Slang |
| optical camouflage / optical camo | optische Tarnung | Gegenstand | |
| corp executioner | Konzernhenker | Sonstiges | |
| nepo hire | Vetternwirtschafts-Neuling / „Protegé“ | Sonstiges | abwertend |
| Buff Girl Ohara | „Buff Girl Ohara“ | Anspielung | Serie in der Spielwelt, Titel unverändert |
| Magical Piledriver / Magical Lariat / Brief Seed | unverändert | Attacke | Serienattacken |
| Re:tro-jan | Re:tro-jan | Ort | Café; Wortspiel Retro + Trojaner (Virus) – über „Trojaner“/„Trojanisches Pferd“ lösen |
| Lunatic (Auftragstitel) | Irrer | Sonstiges | |
| Mock Repair test / mock maintenance | Übungsreparatur-Test / Übungswartung | Sonstiges | S01E01 95: „Standard-Level-1-DXAL-Übungsreparatur-Test“ |
| lame / shady / creepy (Michelle über den Klinik-Namen) | lahm / zwielichtig / gruselig | Running Gag | konsistent halten |
| same difference | Ist doch dasselbe in Grün | Sonstiges | |
| wet themselves / discharging overheated coolant | sich einnässen / Ablassen von überhitztem Kühlmittel | Wortspiel | S01E01 59–62 |
| Oasis (ironisch) | „Oase“ | Anspielung | |
| crappy shop | Bruchbude | Sonstiges | |
| Neon Sign (Wortspiel zu Neon Shine) | „Neon Sign“ unverändert | Wortspiel | |
| neural stimulation unit | Neurostimulationseinheit | Gegenstand | |
| processing unit / emotion unit | Prozessoreinheit / Emotionseinheit | Gegenstand | (anders als die Spielbauteile eingedeutscht) |
| photonic neural network | photonisches neuronales Netz | Sonstiges | |
| electronic drugs | Elektro-Drogen | Sonstiges | |
| moths | Motten | Sonstiges | Lichtmotiv |
| main event | Hauptakt | Wortspiel | Rückbezüge mit gleichem Wort |
| nepo hire | Protegé | Sonstiges | |
| memory-suppressing drugs / amnesia drug | gedächtnisunterdrückende Medikamente / „Amnesie-Medikament“ | Sonstiges | |
| management (Firma) | Geschäftsführung | Sonstiges | |
| Dial (Gerät) | das Dial | Gegenstand | Neutrum |
| creaky / creak | knarzig / Knarzen | Wortspiel | |
| colleagues (Orcas Einheit) | Kolleginnen | Sonstiges | |
| dispatch calls | Einsatzrufe | Sonstiges | |
| the joint (Blade) | Schuppen | Sonstiges | |
| service (Doppeldeutigkeit) | Service | Wortspiel | |
| Open for Business (Menü, Key OPEN_BUSINESS) | Laden öffnen | Sonstiges | Schaltfläche zum Öffnen des Ladens am Tagesbeginn (Aktion, kein Status) |
| Standard-UI (Continue/Settings/Back/Next/Confirm/Cancel/Close/Complete/Submit) | Fortsetzen/Einstellungen/Zurück/Weiter/Bestätigen/Abbrechen/Schließen/Fertig/Absenden | Sonstiges | Exit/Quit → Beenden |
| Credits (Menü) | Mitwirkende | Sonstiges | |
| **Tag 3–7, Ende, News, Tutorial** | | | |
| Polarnight (allein) / Total Polar Night | Polarnacht / Totale Polarnacht | Sonstiges | Quelle schreibt auch „Polanight“, „Polar Night Day“ → einheitlich |
| Happy Polarnight Day | Frohen Polarnacht-Tag! | Running Gag | im Satz: „Heute ist ein froher Polarnacht-Tag.“ / „Immerhin ist heute ein froher Polarnacht-Tag.“ |
| Way too late | Viel zu spät | Running Gag | E16/E17 gleich |
| The moon is beautiful tonight | Der Mond ist heute Nacht wunderschön | Anspielung | verdeckte Liebeserklärung |
| Night air is pretty nice | Die Nachtluft ist ziemlich angenehm | Running Gag | E17 gleich |
| Ash Gray Night | aschgraue Nacht | Sonstiges | |
| Dimming / Flicker / Blackout | Dimming / Flicker / Blackout | Sonstiges | LDS-Stufen 1/2/3, unverändert („Stufe 1 ‚Dimming‘“) |
| A.D.A.M. (Autonomous Data Anomaly Manifestation) | A.D.A.M. | Sonstiges | Abkürzung bleibt, Langform englisch |
| Electric Entity (E.E.) / Electric Vital Entity (E.V.E.) | unverändert | Sonstiges | |
| Shadow Proxy / Shadow Proxying | Shadow Proxy / Shadow-Proxying | Organisation | Sunshine-Dienst (E.V.Es spielen Verstorbene) |
| Secret Tuning | „Secret Tuning“ | Sonstiges | |
| Nano Catalyst | Nano-Katalysator | Gegenstand | |
| Sigmund Pact | Sigmund-Pakt | Sonstiges | |
| Summary Executioners | Summary Executioners | Organisation | unverändert (wie Stability Officers) |
| Morning Glory | Morning Glory | Organisation | Terrorgruppe; Name bleibt. Wortspiel mit „morning wood“ (S01E09 73–82, 112; S01E10 20) → Blade erklärt es als „Morgenlatte“ |
| The Noise | The Noise | Organisation | Untergrund; Wortspiel „one massive noise“ → „ein einziger gewaltiger Noise/Lärm“ sinngemäß |
| Urban Stability Agency (USA) | Urban Stability Agency (USA) | Organisation | |
| Stability Officer Academy / training center | Stability-Officer-Akademie | Ort | beide Quellbegriffe gleich |
| Independent Government | Unabhängige Regierung | Organisation | |
| Gray Unit | Gray Unit | Organisation | |
| Waifu Matin Press (WMP), Sunshine Dispatch, The Chroma City Standard (CCS), Achromatic Press (AP), Neon-Net | unverändert | Organisation | Bylines: „Von …“ |
| Dark Brown Street, Deep Red Street, Sunshine Tower | unverändert | Ort | |
| Chroma City Central Plaza | Zentralplatz von Chroma City | Ort | |
| Chroma (Kurzform der Stadt) | Chroma | Ort | |
| Chromatic Zenith Terror Incident | Terroranschlag beim Chromatic Zenith | Sonstiges | |
| O'rhasm Buff | O'rhasm Buff | Gegenstand | Wortspiel bleibt |
| D6AL | D6AL | Gegenstand | |
| Magical German Suplex / Magical Backbreaker | unverändert | Attacke | |
| Buff Girl (Kurzform) | Buff Girl | Anspielung | |
| O'Hara (Quellvariante) | Ohara | Figur | immer „Ohara“ |
| Story Mode | Erzählmodus | Sonstiges | |
| free tip | Gratis-Tipp | Sonstiges | |
| (Send Cancelled) / (Input Cancelled) | (Senden abgebrochen) / (Eingabe abgebrochen) | Sonstiges | Chat-UI |
| [Pray's Reward] | [Prays Belohnung] | Sonstiges | Auftragstitel-Variante |
| neon signs (klein, allgemein) | Neonreklamen | Sonstiges | nicht das Wortspiel „Neon Sign“ |
| heat control unit | Wärmeregelungseinheit | Gegenstand | |
| observatory / scenic promenade / bike | Observatorium / Aussichtspromenade / Motorrad | Sonstiges | |
| Sprecher `???` als Geräusch (S01E12 106–111, S01E17 157–158) | Lautmalerei | Sonstiges | keine Figur |
| **Tutorial/Puzzle** | | | |
| module / damaged part / damage spot | Modul / beschädigtes Teil / Schadensstelle | Spielbegriff | |
| layers / indices | Ebenen / Indizes | Spielbegriff | |
| battery (D1AL) | Akku | Spielbegriff | |
| chain synthesis | Kettensynthese | Spielbegriff | |
| Info Panel / Replace button / Restart button / Encyclopedia | Infopanel / Ersetzen-Button / Neustart-Button / Enzyklopädie | UI | |
| special function / gauge | Spezialfunktion / Anzeige | Spielbegriff | |
| Overloaded Unit / Cyber Drug Unit | Overloaded Unit / Cyber Drug Unit | Spielbegriff | Bauteile englisch |
| **Aus dem Hauptlauf (Phase 4)** | | | |
| supplements (Chris' Pillen) | Nahrungsergänzungsmittel | Gegenstand | festgelegt (S01E12 hatte „Supplements“) |
| core (E.V.E) | Kern | Gegenstand | festgelegt (S01E08 hatte „Core“) |
| memory suppressant / neuromodulator / Amnestics | Gedächtnisunterdrücker / Neuromodulator / „Amnestika“ | Sonstiges | |
| med-subs / medical sub | Medizin-Abo(s) | Sonstiges | |
| the Outside / Command / Warlords | die Außenwelt / Einsatzleitung / Kriegsherren | Sonstiges | |
| made, not born | hergestellt, nicht geboren | Rückbezug | E12 ↔ E13 |
| second / real Michelle, fake, failed project, Case 17 | „zweite“ / „echte“ Michelle, Fälschung, gescheitertes Projekt, Fall 17 | Sonstiges | |
| Mr. Hotshot Mechanic | Herr Superschrauber | Sonstiges | ironisch |
| Michelle is dead. / But I am Michelle. | Michelle ist tot. / Aber ich bin Michelle. | Rückbezug | E15/E16 |
| expert opinion („that word“) | Expertenmeinung / Expertin | Running Gag | Chris ↔ Lianne |
| attached (Lianne) | an jemandem hängen | Wortspiel | |
| it wasn't his/my business | weil es ihn/mich nichts anging | Rückbezug | |
| dazed and refreshed | benommen und … erfrischt | Rückbezug | |
| Morning Glory (Chris' Lesart) | „Pracht des Morgens“ | Wortspiel | Blade: „Morgenlatte“ |
| Friendly Clerk Patch | „Freundliche-Verkäuferin-Patch“ | Gegenstand | |
| Intensive Crackdown Period | verschärfte Kontrollphase | Sonstiges | |
| Urban Happiness Index | Stadt-Glücksindex | Sonstiges | |
| High-Level Sunshine Corp. Executive | Hochrangiger Sunshine-Corp-Manager | Sonstiges | News 17 / E06 58 |
| Chromatic Zenith (Genus) | das Chromatic Zenith | Sonstiges | |
| rebar | Armierungseisen | Gegenstand | |
| Ship of Theseus / essence | Schiff des Theseus / Essenz | Anspielung | |
| Klick-Hinweise (Tutorial) | „(Klicke auf …, um fortzufahren)“ | UI | |
| **Festgelegte Zitate (wörtlich übernehmen)** | | | |
| S01E08 220 zitiert S01E03 83 | „Nimm Budget und Entschädigungen raus, und in Chroma bleiben nur die Patienten übrig.“ | Zitat | bereits übersetzt – Orca zitiert Chris wörtlich |
| S01E06 58 zitiert News-Titel S00E04 17 | identisch übersetzen (gleiches Paket) | Zitat | |
| Prays Kundenkommentare S00E03 26–28 = S01E06 145–147/153–154 | identisch übersetzen (gleiches Paket) | Zitat | |
| S01E17 183 greift S01E14 234 auf („rambling about my own interests“) | „… über meine eigenen Interessen drauflosgeplappert“ | Rückbezug | beide Folgen mit „drauflosplappern“ |
| Sprachnamen im Menü (English, 한국어 …) | unverändert in Eigenschreibweise | Sonstiges | |

## Zu prüfen
- (vom Nutzer bestätigt: Polarnacht-Tag, Bauteile englisch, Orca → „Chef“)
