# Promotion

Ready-to-post material for `c-code-score`. English, idea-first, honest about
limitations and AI involvement.

## Reddit — r/C_Programming

**Title:** After 40 years of C, I wrote a tiny triage tool that scores every C
function with a single number

> score(f) = nesting × pointer depth × deref chain
>
> Each factor is one sentence:
> - **nesting** — depth of `if`/`for`/`while` levels
> - **pointer depth** — `int *`, `int **`, `int ***` in params/locals (deeper = closer to a memory bug)
> - **deref chain** — `a->b->c` runs, i.e. null-derefs where the middle pointer came from somewhere else
>
> No parser, no dependencies, one file.
>
> I tested it on two very different codebases — a 40-year-old X11 toolkit (libXt) and a format parser (libtiff) — and correlated the score against maintenance churn (how often a function gets touched):
>
> - Spearman(Score, Churn): 0.52 (libXt), 0.38 (libtiff)
> - vs. NLOC: 0.50 / 0.33, vs. cyclomatic complexity: 0.41 / 0.32
> - the top-15 functions see ~3–5× the churn of the bottom-15
>
> It's a triage tool, not a bug detector — it won't find semantic bugs, and it's not a quality gate. But "read the top 15, skip the rest" beats reading the whole file.
>
> `pip install c-code-score` · `c-score file.c`
> Repo: https://github.com/xtforever/c-score — feedback welcome.
>
> Disclaimer: my idea; I used DeepSeek V4 Pro to help write the Python and this post.

## X/Twitter — thread

1. A C function is worth a second look when it's deeply nested, juggles pointers-of-pointers, and chases `a->b->c`. I turned that intuition into one number.
2. `score(f) = nesting × pointer depth × deref chain` — each factor is one sentence: nesting = if/for/while depth; pointer depth = `int *` vs `int **` vs `int ***`; deref chain = `a->b->c` runs.
3. Does it predict pain? On libXt/libtiff it correlates with maintenance churn at Spearman 0.52/0.38 — better than LOC or cyclomatic complexity.
4. It's a triage tool, not a bug detector: "review the top 15, skip the rest." One file, zero dependencies.
5. Try it: `pip install c-code-score` · https://github.com/xtforever/c-score #CProgramming #StaticAnalysis

## Reddit — AI angle (r/LocalLLaMA / r/ClaudeAI)

**Title:** Cheap feedback loop for LLM-written C: a one-number score that flags over-nested, pointer-heavy output

> LLM-generated C has a tell: it's deeply nested and leans on pointers-of-pointers.
> I wrote a tiny scorer that turns that into one number per function:
> `score(f) = nesting × pointer depth × deref chain`.
> The loop: generate → `c-score file.c` → "rewrite the top 3" → re-score.
> One round visibly flattens the code. `pip install c-code-score`
> https://github.com/xtforever/c-score
