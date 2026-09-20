#!/usr/bin/env python3
"""Track median/max score of a C library over git history.

Usage:
  score_history.py --repo PATH --src SUBDIR [--samples N] [--plot out.png]

Prints CSV (index, date, median, max, functions) to stdout; optionally plots
median and max over time (log y-axis) to out.png. matplotlib is only needed
for --plot; the CSV works without it.
"""
import argparse
import datetime
import glob
import io
import os
import statistics
import subprocess
import sys
import tarfile
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import score as scoremod


def extract(repo, src, commit, dest):
    p = subprocess.run(
        ["git", "archive", "--format=tar", commit, "--", src],
        cwd=repo, capture_output=True)
    if p.returncode != 0 or not p.stdout:
        return False
    with tarfile.open(fileobj=io.BytesIO(p.stdout)) as tf:
        tf.extractall(dest)
    return True


def scores_in_dir(root):
    vals = []
    for path in sorted(glob.glob(os.path.join(root, "**", "*.c"),
                                 recursive=True)):
        with open(path, "rb") as fh:
            src = fh.read().decode("utf-8", "replace")
        for name, ln, ptoks, btoks in scoremod.find_functions(
                scoremod.tokenize(src)):
            vals.append(scoremod.metric(name, ln, ptoks, btoks)[6])
    return vals


def sample_indices(n, samples):
    if n <= samples:
        return list(range(n))
    step = (n - 1) / (samples - 1)
    return sorted({round(i * step) for i in range(samples)})


def plot(rows, out):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    dates = [datetime.datetime.fromisoformat(r[1]) for r in rows]
    fig, ax = plt.subplots()
    ax.plot(dates, [r[3] for r in rows], label="max", color="tab:red")
    ax.plot(dates, [r[2] for r in rows], label="median", color="tab:blue")
    ax.set_yscale("log")
    ax.set_ylabel("score (log)")
    ax.set_xlabel("revision date")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(out, dpi=130)
    print(f"wrote {out}", file=sys.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--src", required=True)
    ap.add_argument("--samples", type=int, default=100)
    ap.add_argument("--plot", default=None)
    args = ap.parse_args()

    commits = subprocess.run(
        ["git", "rev-list", "--reverse", "HEAD"], cwd=args.repo,
        capture_output=True, text=True).stdout.split()
    indices = sample_indices(len(commits), args.samples)

    tmp = tempfile.mkdtemp(prefix="scorehist")
    rows = []
    print("index,date,median,max,functions")
    for i in indices:
        c = commits[i]
        date = subprocess.run(
            ["git", "show", "-s", "--format=%cI", c], cwd=args.repo,
            capture_output=True, text=True).stdout.strip()
        dest = os.path.join(tmp, str(i))
        os.makedirs(dest, exist_ok=True)
        if not extract(args.repo, args.src, c, dest):
            continue
        vals = scores_in_dir(dest)
        if not vals:
            continue
        row = (i, date, statistics.median(vals), max(vals), len(vals))
        rows.append(row)
        print(f"{row[0]},{row[1]},{row[2]:g},{row[3]},{row[4]}")
        print(f"  commit {i}/{len(commits)}: median={row[2]:g} max={row[3]}",
              file=sys.stderr)

    if args.plot and rows:
        plot(rows, args.plot)


if __name__ == "__main__":
    main()
