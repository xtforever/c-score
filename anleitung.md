# Anleitung

## Was der Score misst

Jede C-Funktion bekommt einen Score aus drei multiplikativ verknüpften
Faktoren:

    score(f) = ( sum_{i>=1} c(i) * 2^(i-1) )
             * ( prod_{k>=1} (k+1)^p(k) )
             * ( prod_{j>=2} (j+1)^d(j) )

| Faktor | Was es zählt | Intuition |
|---|---|---|
| `c(i)` | Statements auf Brace-Tiefe `i` | Tiefe Verschachtelung belastet das Arbeitsgedächtnis |
| `p(k)` | Zeiger mit Indirektion `k` (`int *` = 1, `int **` = 2) in Parametern + Locals | Tiefe Zeiger = Nähe zum Memory-Bug |
| `d(j)` | `->`-Kettenposition `j` ≥ 2 | `a->b->c` dereferenziert einen Zeiger, der von woanders kommt |

Alle drei sind bewusst trivial und in einem Satz erklärbar. Der Zeiger- und
der Deref-Faktor wachsen exponentiell mit der Tiefe — das ist Absicht: eine
Kette `a->b->c->d` ist riskanter als vier einzelne `a->b`.

## Wie die Ausgabe zu lesen ist

```sh
python3 score.py datei.c
```

Jede Funktion wird als Block ausgegeben: die Histogramme `c(i)`, `p(k)`,
`d(j)`, die drei Terme und der Gesamt-Score. Nur die Reihenfolge nach Score
zählt — die absoluten Zahlen sind nicht kalibriert und zwischen Codebasen
nicht vergleichbar.

## Wofür es taugt

- **Triage:** „Schau dir die Top-10/15 an“ statt die ganze Datei zu lesen.
- **Refactoring-Hinweis:** die Top-Scores sind die Wartungs-Hotspots.
- **Stil-Kontrolle:** ein Review der Top-15 vor dem Merge fängt die
  unübersichtlichsten Funktionen.

## Wofür es nicht taugt

- Kein Bug-Detektor. Der Score ranket *Kandidaten*, beweist keine Fehler.
- Sieht keine semantischen Fehler (unchecked return, falsche Logik).
- Sieht keine tiefen Call-Stacks mit Seiteneffekten (das ist eine
  Modul-Eigenschaft, keine Funktions-Eigenschaft).
- Ist durch Aufspalten einer Funktion in viele kleine spielbar — was
  allerdings genau der Zweck ist.

## Der Beleg

Auf zwei sehr unterschiedlichen Codebasen korreliert der Score mit dem
Wartungs-Churn (wie oft eine Funktion angefasst wurde) besser als Zeilenzahl
und zyklomatische Komplexität:

| | libXt | libtiff |
|---|---|---|
| Spearman(Score, Churn) | **0.52** | **0.38** |
| Spearman(NLOC, Churn) | 0.50 | 0.33 |
| Spearman(CCN, Churn) | 0.41 | 0.32 |

Die Top-15 haben rund das Drei- bis Fünffache des Churn der Bottom-15.
Churn ist der etablierte Proxy für „hier passiert Wartung“ — genau die
Stelle, an der Refactoring sich lohnt.

## Grenzen des Parsers

score.py ist ein Ein-Pass-Tokenizer, kein C-Parser. Bekannte Lücken:
K&R-Definitionen, exotische Makro-Konstrukte und typedef-basierte
Deklarationserkennung. Im Zweifel zählt er eine Funktion zu wenig oder zu
viel — für die Rangfolge ist das unkritisch.
