# Quickstart

## Voraussetzung

Python 3. Sonst nichts.

## 30 Sekunden

```sh
python3 score.py --selftest      # muss "selftest ok" ausgeben
python3 score.py pfad/zu/datei.c # pro Funktion: Faktoren + Score
```

Nach Score absteigend ansehen — die Funktionen oben sind die Kandidaten.

## Beispiel-Ausgabe

```
parse_list (line 147)
  c(i): {1: 7, 2: 6}
  p(k): {1: 2}
  d(j): {}
  nesting term: 7*2^0 + 6*2^1 = 19
  pointer term: 2^2 = 4
  deref term:   1 = 1
  score: 76
```

## Top-N über mehrere Dateien

```sh
for f in lib/*.c; do python3 score.py "$f"; done | grep 'score:' | sort -t: -k2 -rn | head
```

(Die Funktionsnamen stehen im Block direkt über der `score:`-Zeile.)
