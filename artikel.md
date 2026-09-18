# score.py — eine Zahl, die sagt, wo ein Blick lohnt

score.py ist ein winziges Werkzeug, das jede C-Funktion mit einer einzigen
Zahl bewertet. Hoher Score heißt: **Diese Funktion lohnt einen prüfenden
Blick** — ohne Parser, ohne Dependencies, ohne Setup.

## Die Metrik

    score(f) = Verschachtelung × Zeiger-Tiefe × Deref-Kette

- **Verschachtelung** misst die Arbeitsgedächtnis-Last tiefer `if`/`for`/`while`-Ebenen.
- **Zeiger-Tiefe** zählt `int *`, `int **`, `int ***` in Parametern und Locals — je tiefer, desto näher am Memory-Bug.
- **Deref-Kette** zählt `a->b->c`-Ketten, also Null-Derefs, wo der Zwischen-Zeiger von woanders kommt.

Jeder Faktor ist in einem Satz erklärbar. Genau das ist der Punkt: eine
Metrik, die man erklären kann, wird benutzt.

## Der Beleg

Auf zwei sehr unterschiedlichen Codebasen — einem 40 Jahre alten
X11-Framework (libXt) und einem Dateiformat-Parser (libtiff) — korreliert
der Score mit dem Wartungs-Churn (wie oft eine Funktion angefasst wurde)
besser als Zeilenzahl oder zyklomatische Komplexität:

    Spearman(Score, Churn): 0.52 (libXt), 0.38 (libtiff)

Und die Top-15 haben rund das Drei- bis Fünffache des Churn der Bottom-15.

## Wofür — und wofür nicht

score.py ist ein **Triage-Werkzeug**: „Schau dir die Top-15 an“ statt die
ganze Datei zu lesen. Es ist kein Bug-Detektor, kein Qualitäts-Gate und
sieht semantische Fehler nicht. Aber ein kleiner, erklärbarer Hinweis ist
besser als keiner.

## Ausprobieren

    python3 score.py datei.c        # Funktionen + Score
    python3 score.py --selftest     # Selbsttest

Eine Datei, keine Dependencies.
