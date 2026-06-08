#!/usr/bin/env python3
"""
Summarise the output of ``check_reviews.py``.

Reads the JSONL produced by ``check_reviews.py``, prints the flagged
reviews to stdout for triage, and writes a small set of bar/histogram
plots showing the verdict and signal distributions across the venue.

Usage:
    .venv/bin/python scripts/evaluate_reviews.py [options]

The default input is ``scripts/check_reviews_results.jsonl`` and plots
land in ``scripts/check_reviews_plots/``. Both paths are gitignored along
with the underlying review content.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable

import matplotlib

matplotlib.use("Agg")  # headless: no display required
import matplotlib.pyplot as plt
import seaborn as sns


# Verdict ordering for plots/tables — least-to-most-suspicious. Mirrors
# ``VERDICT_VALUES`` in ``check_reviews.py``; duplicated rather than
# imported because the two scripts are siblings without a shared module.
VERDICTS = ("human", "unclear", "likely_llm", "definitely_llm")
FLAGGED_VERDICTS = frozenset({"likely_llm", "definitely_llm"})

# Match the fixed signal vocabulary the judge is constrained to. Any
# stray signal in a row is shown but not in this canonical order.
SIGNAL_VOCAB = (
    "generic_praise",
    "templated_structure",
    "em_dash_pattern",
    "transition_overuse",
    "no_specific_references",
    "ai_disclosure",
    "refusal_pattern",
    "copy_paste_artifact",
    "balanced_to_a_fault",
    "citation_hallucination",
)


# ---------------------------------------------------------------------------
# I/O
# ---------------------------------------------------------------------------


def load_rows(path: Path, schema_version: int | None) -> list[dict]:
    """Read JSONL rows, optionally restricted to a single schema version."""
    if not path.exists():
        print(f"error: results file not found: {path}", file=sys.stderr)
        sys.exit(1)

    rows: list[dict] = []
    skipped_schema = 0
    skipped_bad = 0
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                print(f"warning: {path}:{lineno}: skipping malformed line ({exc})", file=sys.stderr)
                skipped_bad += 1
                continue
            if schema_version is not None and row.get("schema_version") != schema_version:
                skipped_schema += 1
                continue
            rows.append(row)

    if skipped_schema:
        print(
            f"note: skipped {skipped_schema} row(s) from a different schema_version",
            file=sys.stderr,
        )
    if skipped_bad:
        print(f"note: skipped {skipped_bad} malformed line(s)", file=sys.stderr)
    return rows


def split_rows(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Partition rows into successfully-judged vs. error rows."""
    judged = [r for r in rows if "verdict" in r and "error" not in r]
    errors = [r for r in rows if "error" in r]
    return judged, errors


# ---------------------------------------------------------------------------
# Reporting
# ---------------------------------------------------------------------------


def print_summary(judged: list[dict], errors: list[dict]) -> None:
    n = len(judged)
    print()
    print("=" * 72)
    print(f"  REVIEW AUDIT SUMMARY  ({n} judged, {len(errors)} errors)")
    print("=" * 72)

    if not n:
        print("  No successfully-judged rows. Nothing to report.")
        return

    counts = Counter(r["verdict"] for r in judged)
    print()
    print("  Verdict breakdown:")
    width = max(len(v) for v in VERDICTS)
    for v in VERDICTS:
        c = counts.get(v, 0)
        pct = (c / n) * 100
        print(f"    {v:<{width}}  {c:>4}  ({pct:5.1f}%)")
    extras = set(counts) - set(VERDICTS)
    for v in sorted(extras):
        print(f"    {v:<{width}}  {counts[v]:>4}  (UNEXPECTED VERDICT)")

    flagged = [r for r in judged if r["verdict"] in FLAGGED_VERDICTS]
    print(f"\n  Flagged: {len(flagged)} / {n}  ({len(flagged) / n * 100:.1f}%)")


def _print_review_row(r: dict) -> None:
    """Pretty-print a single review row in the standard triage format."""
    forum = r.get("forum_id", "?")
    rid = r.get("review_id", "?")
    score = r.get("score", 0.0)
    verdict = r.get("verdict", "?")
    signals = r.get("signals") or []
    signature = r.get("reviewer_signature") or ""
    short_sig = signature.rsplit("/", 1)[-1] if signature else ""
    rating = r.get("rating")
    confidence = r.get("confidence")
    rationale = (r.get("rationale") or "").strip()

    print()
    print(
        f"  [{verdict:<14} score={score:.2f}]  "
        f"https://openreview.net/forum?id={forum}&noteId={rid}"
    )
    meta_bits = [f"reviewer={short_sig}"]
    if rating is not None:
        meta_bits.append(f"rating={rating}")
    if confidence is not None:
        meta_bits.append(f"confidence={confidence}")
    print("    " + "  ".join(meta_bits))
    if signals:
        print(f"    signals: {', '.join(signals)}")
    if rationale:
        for line in _wrap(rationale, 64, indent="    "):
            print(line)


def print_top_n(judged: list[dict], n: int) -> None:
    """Print the top-N highest-scoring reviews regardless of threshold.

    Useful when no review crosses the flag threshold — you still want to
    eyeball the most-suspicious cases the judge produced.
    """
    if n <= 0 or not judged:
        return
    ranked = sorted(judged, key=lambda r: -r.get("score", 0.0))[:n]

    print()
    print("=" * 72)
    print(f"  TOP {len(ranked)} HIGHEST-SCORED REVIEWS")
    print("=" * 72)
    for r in ranked:
        _print_review_row(r)


def print_flagged(judged: list[dict], threshold: float) -> None:
    """Print every review whose score >= threshold, sorted desc."""
    flagged = [r for r in judged if r.get("score", 0.0) >= threshold]
    flagged.sort(key=lambda r: (-r.get("score", 0.0), r.get("forum_id", "")))

    print()
    print("=" * 72)
    print(f"  FLAGGED REVIEWS  (score >= {threshold:.2f}, n={len(flagged)})")
    print("=" * 72)
    if not flagged:
        print("  No reviews crossed the threshold.")
        return

    for r in flagged:
        _print_review_row(r)


def print_per_submission(judged: list[dict], threshold: float) -> None:
    """Group flagged reviews by submission and report concentrations."""
    by_forum: dict[str, list[dict]] = defaultdict(list)
    for r in judged:
        by_forum[r.get("forum_id", "?")].append(r)

    rows = []
    for forum, group in by_forum.items():
        n_total = len(group)
        n_flag = sum(1 for r in group if r.get("score", 0.0) >= threshold)
        if n_flag:
            rows.append((forum, n_flag, n_total))

    if not rows:
        return

    rows.sort(key=lambda x: (-x[1] / x[2], -x[1]))  # by flagged-fraction desc

    print()
    print("=" * 72)
    print("  CONCENTRATION BY SUBMISSION  (forums with >= 1 flagged review)")
    print("=" * 72)
    for forum, n_flag, n_total in rows:
        marker = " ⚠" if n_flag >= 2 else ""
        print(
            f"  {forum:<12}  {n_flag}/{n_total} flagged   "
            f"https://openreview.net/forum?id={forum}{marker}"
        )


def _wrap(text: str, width: int, indent: str) -> Iterable[str]:
    """Tiny word-wrapper. textwrap would also do but this is friendlier
    with the surrounding output style."""
    words = text.split()
    line = indent
    for w in words:
        if len(line) + 1 + len(w) > width + len(indent):
            yield line
            line = indent + w
        else:
            line = (line + " " + w) if line.strip() else (indent + w)
    if line.strip():
        yield line


# ---------------------------------------------------------------------------
# Plots
# ---------------------------------------------------------------------------


def make_plots(judged: list[dict], out_dir: Path) -> list[Path]:
    """Render the standard set of plots; return the list of written files."""
    out_dir.mkdir(parents=True, exist_ok=True)
    sns.set_theme(style="whitegrid", context="talk")

    written: list[Path] = []
    written.append(_plot_verdict_counts(judged, out_dir / "verdict_counts.png"))
    written.append(_plot_score_hist(judged, out_dir / "score_distribution.png"))
    written.append(_plot_signal_frequency(judged, out_dir / "signal_frequency.png"))
    rs = _plot_rating_vs_score(judged, out_dir / "rating_vs_score.png")
    if rs is not None:
        written.append(rs)
    return written


# Verdict-coloured palette: shifts from green (human) to red (definitely_llm).
# Same colours are reused wherever a chart's primary axis is the verdict, so
# the plots tell a consistent story.
_VERDICT_PALETTE = {
    "human": "#4c956c",
    "unclear": "#d9b341",
    "likely_llm": "#d97c2b",
    "definitely_llm": "#c1352e",
}


def _plot_verdict_counts(judged: list[dict], path: Path) -> Path:
    counts = Counter(r["verdict"] for r in judged)
    values = [counts.get(v, 0) for v in VERDICTS]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = sns.barplot(
        x=list(VERDICTS),
        y=values,
        hue=list(VERDICTS),
        palette=[_VERDICT_PALETTE[v] for v in VERDICTS],
        legend=False,
        ax=ax,
    )
    ax.set_xlabel("Verdict")
    ax.set_ylabel("Number of reviews")
    ax.set_title(f"Verdict distribution (n={len(judged)})")
    ax.tick_params(axis="x", rotation=15)
    for i, v in enumerate(values):
        if v:
            ax.text(i, v + max(values) * 0.01, str(v), ha="center", va="bottom", fontsize=12)
    sns.despine(fig)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def _plot_score_hist(judged: list[dict], path: Path) -> Path:
    scores = [r.get("score") for r in judged if isinstance(r.get("score"), (int, float))]
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(scores, bins=20, binrange=(0.0, 1.0), color="#4a6fa5", ax=ax)
    ax.set_xlabel("LLM-likelihood score")
    ax.set_ylabel("Number of reviews")
    ax.set_title(f"Score distribution (n={len(scores)})")
    ax.set_xlim(0.0, 1.0)
    # Light reference line at the default 0.5 flagging threshold.
    ax.axvline(0.5, color="#c1352e", linestyle="--", linewidth=1.5, alpha=0.6)
    ax.text(
        0.51, ax.get_ylim()[1] * 0.95, "default threshold",
        color="#c1352e", fontsize=11, va="top",
    )
    sns.despine(fig)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def _plot_signal_frequency(judged: list[dict], path: Path) -> Path:
    counts: Counter[str] = Counter()
    for r in judged:
        for s in r.get("signals") or []:
            counts[s] += 1

    # Keep canonical ordering for the vocab; append any unexpected tags
    # alphabetically at the bottom.
    ordered = [(s, counts.get(s, 0)) for s in SIGNAL_VOCAB]
    extras = sorted(s for s in counts if s not in SIGNAL_VOCAB)
    ordered += [(s, counts[s]) for s in extras]

    labels = [s.replace("_", " ") for s, _ in ordered]
    values = [c for _, c in ordered]

    fig, ax = plt.subplots(figsize=(9, max(4.5, 0.35 * len(labels) + 1.5)))
    sns.barplot(x=values, y=labels, color="#4a6fa5", ax=ax)
    ax.set_xlabel("Times flagged across all reviews")
    ax.set_ylabel("")
    ax.set_title("Signal frequency")
    for i, v in enumerate(values):
        if v:
            ax.text(v + max(values + [1]) * 0.01, i, str(v), va="center", fontsize=11)
    sns.despine(fig)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


def _plot_rating_vs_score(judged: list[dict], path: Path) -> Path | None:
    """Scatter rating vs. LLM-likelihood score. Returns None if no ratings."""
    pts = [
        (r["rating"], r["score"], r.get("verdict", "unclear"))
        for r in judged
        if isinstance(r.get("rating"), (int, float))
        and isinstance(r.get("score"), (int, float))
    ]
    if not pts:
        return None

    ratings = [p[0] for p in pts]
    scores = [p[1] for p in pts]
    verdicts = [p[2] for p in pts]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.scatterplot(
        x=ratings,
        y=scores,
        hue=verdicts,
        hue_order=list(VERDICTS),
        palette=_VERDICT_PALETTE,
        s=70,
        alpha=0.75,
        ax=ax,
    )
    ax.axhline(0.5, color="#c1352e", linestyle="--", linewidth=1.2, alpha=0.5)
    ax.set_xlabel("Reviewer rating")
    ax.set_ylabel("LLM-likelihood score")
    ax.set_title("Rating vs. LLM-likelihood")
    ax.set_ylim(-0.05, 1.05)
    ax.legend(title="verdict", loc="best", fontsize=10, title_fontsize=10)
    sns.despine(fig)
    fig.tight_layout()
    fig.savefig(path, dpi=140)
    plt.close(fig)
    return path


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--results",
        type=Path,
        default=Path("scripts/check_reviews_results.jsonl"),
        help="Path to the JSONL produced by check_reviews.py "
        "(default: scripts/check_reviews_results.jsonl).",
    )
    parser.add_argument(
        "--plots-dir",
        type=Path,
        default=Path("scripts/check_reviews_plots"),
        help="Directory for the generated PNG plots "
        "(default: scripts/check_reviews_plots).",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.5,
        help="Score threshold (>=) for flagging reviews in the printed "
        "report. Default: 0.5.",
    )
    parser.add_argument(
        "--schema-version",
        type=int,
        default=None,
        help="If set, only consider rows with this schema_version. By "
        "default all rows are loaded; mismatched schemas are reported.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="Print the top-N highest-scored reviews regardless of "
        "threshold. Default: 10. Use 0 to suppress.",
    )
    parser.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip plot generation; only print the text report.",
    )
    args = parser.parse_args()

    rows = load_rows(args.results, args.schema_version)
    judged, errors = split_rows(rows)

    print_summary(judged, errors)
    print_top_n(judged, args.top)
    print_flagged(judged, args.threshold)
    print_per_submission(judged, args.threshold)

    if errors:
        print()
        print("=" * 72)
        print(f"  ERROR ROWS  ({len(errors)})")
        print("=" * 72)
        kinds = Counter(r.get("error", "?") for r in errors)
        for k, c in kinds.most_common():
            print(f"  {k:<24} {c}")
        print("  (re-run check_reviews.py to retry; errors are cached by review_id)")

    if not args.no_plots and judged:
        print()
        print("=" * 72)
        print(f"  PLOTS  → {args.plots_dir}/")
        print("=" * 72)
        for p in make_plots(judged, args.plots_dir):
            print(f"  {p}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
