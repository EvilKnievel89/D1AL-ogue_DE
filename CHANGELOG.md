# Changelog

## 1.0.2 – 2026-11-23

- Die Übersetzung wurde einmal vollständig im Spiel durchgespielt; die dabei gefundenen Stellen sind korrigiert.
  Hinweis in README und LIESMICH entsprechend aktualisiert.

- Tag 7 (Orca): „Anders als bei deinen Standard-E.V.Es“ → „Anders als gewöhnliche E.V.Es“ – das englische
  „your standard“ war generisch gemeint, keine Anrede (`DialogueTable|60026_15`).
- Tag 7 (Pray): „Bist du komplett kastriert oder was?“ → „Bist du impotent oder was?“ – wie im Original
  (KO 고자, JA インポ) derb, aber idiomatisch (`DialogueTable|60028_35`).
- Tag 7 (Pray): „zu der man zurückkann“ → „zu der man zurückkehren kann“ (`DialogueTable|60028_94`).
- Tag 7 (Pray): „verdächtig glattzüngigen Mechaniker“ → „verdächtig redegewandten Mechaniker“
  (`DialogueTable|60028_163`).
- Tag 7 (Pray): „nehme ich dich mit an einen Hammer-Laden“ → „nehme ich dich mit in ein mega leckeres
  Restaurant“ (`DialogueTable|40282_6`).

## 1.0.1 – 2026-11-23

- Menü: Schaltfläche zum Öffnen des Ladens am Tagesbeginn heißt jetzt „Laden öffnen“ statt „Geöffnet“
  (`OPEN_BUSINESS` ist eine Aktion, kein Status).
- Tag 4 (Blade): grammatisch falschen Satz korrigiert – „Außerdem ist es auch für Sie angenehmer,
  wenn nichts protokolliert wird, Blade.“ (`DialogueTable|60016_56`).
- Korrekturdurchgang über alle 4.091 Texte (Abgleich mit Englisch und koreanischem Original):
  28 Zeilen korrigiert – Grammatik (z. B. Kasus, Verbstellung, ungültiges Passiv), wörtlich übernommene
  englische Wendungen („handlicher Mechaniker“, „Leider für sie“, „Das Gefühl ist gegenseitig“),
  Sinnfehler („Nur weil du die zweite Michelle akzeptierst, leugnest du nicht …“), kaputte
  Satzübergänge zwischen zwei Textfenstern, ein Glossar-Verstoß und ein Tippfehler.
- Tag 5 (Pray): Erklärung von „Shadow Proxying“ präzisiert – „… wenn einer E.V.E die Daten einer
  anderen Person übergestülpt werden“ (`DialogueTable|60018_105`).
- Tag 5 (Pray): „Gezappel.“ → „Ein unruhiges Herumrutschen.“, Folgesatz „Pray drehte und wand sich,
  als fühlte sie sich unwohl.“ (`60018_136`, `60018_137`).
- „Don't tell me …“ einheitlich als „Sag bloß …“ statt „Sag nicht …“ (4 weitere Stellen).
- Tag 5 (Lianne): Liannes Satz über fünf Textfenster („Dass ausgerechnet ich, die ich meine Gefühle so
  schlecht im Griff habe, … liegt vielleicht nur daran, dass ich mir etwas wünsche, das ich nicht habe.“)
  grammatisch durchgehend neu gebaut, „fader, langweiliger Mechaniker“ → „schlichter, unaufgeregter“
  (`60020_30`–`60020_34`).
- Zweiter Korrekturdurchgang gezielt für Sätze über mehrere Textfenster (592 Satzketten als Ganzes
  gelesen): 26 Ketten mit 39 Fenstern korrigiert – Nebensätze ohne passenden Hauptsatz, falsche
  Verbstellung über die Fenstergrenze, wörtliche englische Gerundium-Konstruktionen, verdrehte
  Kausalität (u. a. Michelles „… muss ich dieses schreckliche Leben führen, das ich nie wollte“,
  Orcas Rückblick in Tag 7, mehrere Stellen in den Enden).
- Tag 6: Michelle verwechselt Prays Namen jetzt mit „Play“ statt „Fliege“ – im Original eine
  R/L-Verwechslung (프레이/플라이, engl. „Fly“), kein Spitzname (`DialogueTable|60022_58`).
- Tag 6: Chris' „Orca-Orca-Orca“-Satz flüssiger, der beabsichtigte Namens-Gag bleibt erhalten
  („… heißt das, es fällt schwer zu merken, dass etwas nicht stimmt, / solange Orca Orca für ... Orca hält?“).

## 1.0.0 – 2026-11-22

- Erste Veröffentlichung: vollständige deutsche Übersetzung (4.091 Texte) – Intro, Tag 1–7,
  gemeinsames Ende, vier Figuren-Enden, Abspann, Menü, Tutorial, Kundenkommentare, News.
- Patcher mit automatischer Steam-Erkennung, Sicherung/Wiederherstellung der Originale,
  Update-Erkennung und Schutz vor doppeltem Patchen.
- Getestet mit Spielversion 1.0.4 (Steam-Build 24985627).
