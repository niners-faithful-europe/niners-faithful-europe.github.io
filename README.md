# Niners Faithful Europe

Deutsch-englische Collab-Plattform für deutschsprachige Autoren über die San Francisco 49ers und die NFL. Deutsche Beiträge erscheinen als Teaser mit Link zum Original beim Autor, englische Fassungen im Volltext (KI-übersetzt, vom Autor freigegeben).

Unabhängiges Fanprojekt, keine Verbindung zur NFL oder zu den San Francisco 49ers.

## Aufbau
- `data/articles.json`: alle Beiträge. `status`: `live` (auf der Seite), `entwurf` (wartet in der Inbox), `abgelehnt` (wird ignoriert und nicht erneut importiert).
- `data/sources.json`: Quellen für den Import (RSS-Feeds, cp7-Projekte).
- `src/inbox.py`: legt Freigabe-Issues an und wertet geschlossene Issues aus.
- `src/import_feeds.py`: holt neue Beiträge und legt sie als Entwurf an, mit Vorschlag für Rubrik und Format.
- `src/build.py`: baut alle Seiten (DE/EN) nach `site/`, inklusive der internen Inbox unter `/de/inbox/`.
- `src/figs.py`: Bildkatalog je Rubrik. `src/poster.js`: Plakatgrafik (erzeugt `poster_*.svg.txt` und `watermark.svg`).

## Ablauf
1. Täglich um 6:17 Uhr holt `.github/workflows/site.yml` neue Beiträge und legt zu jedem Entwurf ein **Issue** an („Freigabe: …“). GitHub schickt dazu eine Benachrichtigung (Mail/App).
2. Im Issue Format, Rubrik und Autor per Häkchen prüfen, optional englischen Titel und Teaser eintragen.
3. **Close as completed** = freigeben, **Close as not planned** = ablehnen. Der Workflow trägt das in `data/articles.json` ein und veröffentlicht die Seite neu.
4. Überblick über offene Entwürfe: Inbox unter `/de/inbox/` oder die Issue-Liste.

## Hinweis Niner Empire Germany
Der NEG-Feed und die Artikelseiten nennen keinen Autor. Neue NEG-Beiträge kommen deshalb als „Niner Empire Germany“ (Kürzel `NEG`) in die Inbox; bei der Freigabe `aut` und `author` auf den echten Autor setzen (z. B. `CP` / `Chris Pracher`). Podcast-Folgen („Ep. 395 …“) werden übersprungen.

## Lokal bauen
```
python3 src/build.py site            # Seite unter / (eigene Domain)
NFE_BASE=/niners-faithful-europe python3 src/build.py site   # wie auf GitHub Pages
```
Für eine eigene Domain unter Settings > Secrets and variables > Actions die Variable `NFE_BASE` auf `/` setzen.
