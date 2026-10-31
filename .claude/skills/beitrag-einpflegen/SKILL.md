---
name: beitrag-einpflegen
description: Einen deutschen Football-Beitrag (NEG-Seite, cp7, Substack, X oder eingefügter Text) in Niners Faithful Europe aufnehmen und/oder ins Englische übersetzen. Verwenden, wenn der Nutzer einen Link oder Text schickt und ihn "einpflegen", "aufnehmen", "übersetzen" oder "auf Englisch veröffentlichen" möchte, oder fragt, welche Beiträge noch übersetzt werden müssen.
---

# Beitrag einpflegen und übersetzen

## 1. Beitrag anlegen (falls noch nicht vorhanden)
Erst prüfen, ob es `data/articles/*.json` mit gleichem `link_de` schon gibt (`grep -l "<link>" data/articles/*.json`).

Neue Datei `data/articles/<id>.json`, `id` kurz und sprechend (Kleinbuchstaben, Ziffern, Bindestriche, z. B. `aiyuk-quo-vadis`):

```json
{
  "id": "aiyuk-quo-vadis",
  "status": "live",
  "date": "2026-06-10",
  "title_de": "…", "teaser_de": "…",
  "title_en": "…", "teaser_en": "…",
  "link_de": "https://…",
  "aut": "CP",
  "src": "Niner Empire Germany",
  "fmt": "analyse",
  "rub": "draft"
}
```

- `status`: `live` (auf der Seite), `entwurf` (wartet in der Redaktion), `abgelehnt`.
- `fmt`: `analyse` | `fantext` | `grafik`.
- `rub`: `vorschau` | `nachbericht` | `team` | `spieler` | `draft` | `scheme`.
- `aut`: Kürzel aus `data/authors/`. Unbekannter Autor: Nutzer fragen; neuer Autor: `data/authors/<KÜRZEL>.json` mit `name`, `origin`, `writes_for`, `focus_de`, `focus_en`, `faithful_since`, `bio_de`, `bio_en`, `url`, `consent` (false, bis Zustimmung vorliegt), `aut`.
- `src`: wo das Original erschienen ist (`Niner Empire Germany`, `cp7`, `X`, `Substack` …).
- `teaser_de`: zwei, drei Sätze, die neugierig machen; nichts erfinden, was nicht im Original steht.

## 2. Volltext beschaffen
Reihenfolge:
1. Vom Nutzer eingefügter Text.
2. Original direkt abrufen (WebFetch). NEG-Seite (WordPress): `https://theninerempiregermany.de/wp-json/wp/v2/posts?slug=<slug>&_fields=title,content,date`.
3. Ist die Seite aus der Sitzung nicht erreichbar: Workflow „NEG-Archiv einlesen (mit Volltexten)“ starten (`gh api -X POST repos/niners-faithful-europe/niners-faithful-europe.github.io/actions/workflows/archive-scan.yml/dispatches -f ref=main -f "inputs[after]=JJJJ-MM-TT"`), danach `git fetch origin scan && git show origin/scan:scan/neg-archive.json` lesen (Feld `content_html`).
4. Sonst den Nutzer bitten, den Text einzufügen. X-Artikel und -Posts immer so.

## 3. Übersetzen
In `body_en` als Markdown: Absätze, `##`/`###` Zwischenüberschriften, Listen, Tabellen (`| a | b |`), Zitate (`>`), Links.

Stil:
- Amerikanisches Englisch für ein internationales Faithful-Publikum, sachlich, nah am Original; nichts hinzufügen, nichts weglassen, keine eigene Meinung.
- Football-Fachbegriffe in der üblichen englischen Form (Outside Zone, Play-Action, Cap Hit, Dead Money, RAS, EPA/Play, Success Rate, 53-man roster, Training Camp). Deutsche Anglizismen zurück ins Original-Englisch.
- Zahlen ins englische Format (1,500; 8.00; October 20, 2026). Statistiken, Namen, Tabellenwerte nie verändern.
- Zitate englischer Originalquellen (Spieler, Coaches, Journalisten) nicht rückübersetzen, sondern im Wortlaut übernehmen, wenn bekannt; sonst übersetzen und das kenntlich lassen.
- Kein Geviertstrich (—); stattdessen Komma, Doppelpunkt oder Klammern.
- Bilder/Grafiken: nur übernehmen, wenn der Autor zugestimmt hat; sonst an der Stelle einen Link zum Original setzen („See the chart in the original article“).

Zusätzlich, wenn sinnvoll: `key_de`/`key_en` (Kernaussage, ein Satz) und `method_de`/`method_en` (Datenbasis und Stand).

Dann `"en_status": "zu prüfen"` setzen. Erst wenn der Nutzer sagt, dass der Autor die Übersetzung freigegeben hat: `"en_status": "freigegeben"`. Der englische Volltext erscheint nur, wenn beim Autor `"consent": true` steht; fehlt das, darauf hinweisen.

## 4. Prüfen und veröffentlichen
- `pip install markdown` falls nötig, dann `NFE_BASE= python3 src/build.py /tmp/nfe-check` und kontrollieren, dass `/tmp/nfe-check/en/playbook/<id>/index.html` entsteht (nur bei `freigegeben` + `consent`).
- Committen und auf `main` pushen; der Workflow veröffentlicht in ein bis zwei Minuten.
- Dem Nutzer den Link nennen: `https://niners-faithful-europe.github.io/en/playbook/<id>/`. Bei `zu prüfen`: sagen, dass die Übersetzung in der Redaktion (`/admin/`, Feld „Volltext (Englisch)“) gegengelesen und dort freigegeben werden kann.

## Offene Übersetzungen finden
`grep -L '"body_en"' data/articles/*.json` (noch keine Übersetzung) und `grep -l '"zu prüfen"' data/articles/*.json` (wartet auf Freigabe).
