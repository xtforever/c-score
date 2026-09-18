# score.py

Ein winziges, dependency-freies Werkzeug, das jede C-Funktion mit einer
einzigen Zahl bewertet. Hoher Score heißt: **Diese Funktion lohnt einen
prüfenden Blick** — als Review-Kandidat und als Refactoring-Hinweis.

    score(f) = Verschachtelung × Zeiger-Tiefe × Deref-Kette

Auf zwei sehr unterschiedlichen Codebasen (libXt, libtiff) ranket der Score
die Funktionen mit dem höchsten Wartungs-Churn besser als Zeilenzahl oder
zyklomatische Komplexität. Es ist ein Triage-Werkzeug, kein Bug-Detektor.

Bei KI-gestützter C-Entwicklung ist c-code-score ein nützliches Hilfsmittel:
Das Modell bekommt mit dem Score direktes Feedback zu jeder Funktion und kann
so verschachtelten, zeigerlastigen Code vermeiden — es erzeugt von sich aus
besser wartbaren Code.

## Dateien

- [quickstart.md](quickstart.md) — in 30 Sekunden loslegen
- [anleitung.md](anleitung.md) — Metrik, Interpretation, Grenzen
- [artikel.md](artikel.md) — der kurze Artikel zur Veröffentlichung
- `score.py` — das Werkzeug selbst (eine Datei, kein Dependency)

## Kurz

```sh
python3 score.py --selftest      # Selbsttest
python3 score.py pfad/zu/datei.c # Funktionen + Score
```
