# Niners Faithful Europe

Deutsch-englische Collab-Plattform für deutschsprachige Autoren über die San Francisco 49ers und die NFL. Deutsche Beiträge erscheinen als Teaser mit Link zum Original beim Autor, englische Fassungen im Volltext (KI-übersetzt, vom Autor freigegeben).

Unabhängiges Fanprojekt, keine Verbindung zur NFL oder zu den San Francisco 49ers.

## Redaktion
Alles wird unter **`/admin/`** gepflegt (https://niners-faithful-europe.github.io/admin/):

- **Beiträge:** Neue Beiträge kommen täglich um 6:17 Uhr automatisch als „Entwurf“ dazu (Filter „Entwürfe“). Öffnen, Autor wählen, Format und Rubrik prüfen, Status auf „Live“ setzen, speichern. Ablehnen: Status „Abgelehnt“ (wird nicht erneut importiert). Eigene Beiträge über „Neu“ anlegen.
- **Autoren:** Profile im Line-up, alle mit denselben Angaben: Herkunft, Schreibt für, Schwerpunkt, Faithful seit, Kurzprofil, Website.
- Nach dem Speichern ist die Seite in ein bis zwei Minuten aktuell.

**Anmelden:** „Sign In with Token“ und einen GitHub-Token eingeben (Fine-grained token mit Resource owner `niners-faithful-europe`, nur dieses Repo, Berechtigung *Contents: Read and write*; anlegen unter GitHub > Settings > Developer settings > Personal access tokens > Fine-grained tokens). Der Browser merkt sich die Anmeldung.

## Englische Volltexte über Claude
Beiträge einpflegen und übersetzen geht am einfachsten mit Claude (Claude Code mit Zugriff auf dieses Repo): Link oder Text schicken und sagen „pflege das ein und übersetze es“. Die Arbeitsweise steht in `CLAUDE.md` und im Skill `.claude/skills/beitrag-einpflegen/`. Die Übersetzung landet mit Status „Übersetzt, wartet auf Prüfung“ beim Beitrag; nach Freigabe durch den Autor auf „Vom Autor freigegeben“ setzen (Redaktion oder Claude). Der Volltext erscheint nur, wenn beim Autor „Übersetzung erlaubt“ angehakt ist.

## Aufbau
- `data/articles/*.json`: ein Beitrag je Datei. `status`: `live`, `entwurf` oder `abgelehnt`.
- `data/authors/*.json`: ein Autor je Datei.
- `data/sources.json`: Quellen für den Import (RSS-Feeds, cp7-Projekte).
- `admin/`: Redaktionsoberfläche (Sveltia CMS) und ihre Konfiguration.
- `src/import_feeds.py`: holt neue Beiträge und legt sie als Entwurf an, mit Vorschlag für Rubrik und Format.
- `src/build.py`: baut alle Seiten (DE/EN) nach `site/`.
- `src/figs.py`: Bildkatalog je Rubrik. `src/poster.js`: Plakatgrafik (erzeugt `poster_*.svg.txt` und `watermark.svg`).

## Hinweis Niner Empire Germany
Der NEG-Feed nennt keinen Autor. Neue NEG-Beiträge kommen deshalb ohne Autor als Entwurf; den Autor in der Redaktion wählen. Podcast-Folgen („Ep. 395 …“) werden übersprungen.

## Lokal bauen
```

python3 src/build.py site   # wie auf GitHub Pages (Seite liegt im Wurzelverzeichnis)
```
Die Seite liegt im Wurzelverzeichnis; für einen Unterpfad die Actions-Variable `NFE_BASE` setzen.
