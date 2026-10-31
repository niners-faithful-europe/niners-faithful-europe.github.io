# Niners Faithful Europe

Deutsch-englische Collab-Plattform für deutschsprachige 49ers-Autoren. Deutsche Beiträge erscheinen als Teaser mit Link zum Original, englische Fassungen im Volltext (übersetzt, vom Autor freigegeben). Seite: https://niners-faithful-europe.github.io/ , Redaktion: `/admin/`.

## Regeln
- Inhalte liegen in `data/articles/<id>.json` (ein Beitrag je Datei) und `data/authors/<KÜRZEL>.json`. Seiten nie von Hand bauen oder `site/` committen: Jeder Push auf `main` baut und veröffentlicht automatisch (`.github/workflows/site.yml`).
- Beiträge einpflegen und übersetzen: Skill `beitrag-einpflegen` verwenden.
- Englischen Volltext nur mit `"en_status": "freigegeben"` setzen, wenn der Autor die Übersetzung wirklich freigegeben hat. Sonst `"zu prüfen"`.
- Volltext erscheint nur, wenn beim Autor `"consent": true` steht (Zustimmung zur Übersetzung). Nie eigenmächtig setzen.
- Fremde Beiträge oder Autorenprofile nur ändern, wenn der Nutzer es ausdrücklich will.
- Kürzel (`aut`) und Kennung (`id`) nach dem Anlegen nicht mehr ändern, sonst verlieren Beiträge ihre Zuordnung.
- Keine Team- oder NFL-Logos verwenden. Kein Geviertstrich (—) in Texten.
- Commit-Nachrichten auf Deutsch, kurz, z. B. `Beitrag „aiyuk-quo-vadis“: englischer Volltext`.
