"""
Audit OpenReview reviews for likely LLM-generated content.

For each submission in ``submissions.csv``, this script fetches the
``Official_Review`` notes from OpenReview and asks the local ``claude``
CLI (Claude Code in headless ``-p`` mode) to judge how likely each review
was written or substantially rewritten by an LLM. Verdicts are appended
to a JSONL cache as they are produced, so the script is resumable: a
second run only judges reviews not already in the cache.

The cache is intentionally kept out of git — see the ``.gitignore`` entry
added alongside this script. Review content is confidential.

Usage:
    OPENREVIEW_USERNAME=... OPENREVIEW_PASSWORD=... \\
        .venv/bin/python scripts/check_reviews.py [options]

Run with ``--max-submissions 1`` first to smoke-test the pipeline before
committing to a full pass.
"""

from __future__ import annotations

import argparse
import csv
import getpass
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qs, urlparse

import openreview  # noqa: F401  (ensures the package is importable up-front)
import openreview.api


# ---------------------------------------------------------------------------
# Schema & prompts
# ---------------------------------------------------------------------------

# Bump this when the prompt or output schema changes meaningfully — old
# rows are then re-judged on the next run. Cached rows whose schema does
# not match the current value are ignored at startup.
#
# v2: widened review body field detection beyond
#     ``summary``/``strengths``/``weaknesses``/``questions`` so venues
#     using different review templates (e.g. ``review``, ``main_review``,
#     ``comments``) are picked up correctly.
SCHEMA_VERSION = 2

# Fixed signal vocabulary. Constraining the judge to these tags keeps the
# output aggregatable (``jq '.signals[]' ... | sort | uniq -c``).
SIGNAL_VOCAB = [
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
]

VERDICT_VALUES = ["human", "unclear", "likely_llm", "definitely_llm"]

JUDGE_SYSTEM_PROMPT = f"""You are an expert peer-review auditor.

Given a single conference paper review, judge how likely it is that the
review was *generated or substantially rewritten by a large language
model* rather than written by a human reviewer.

Consider, non-exhaustively:
- Section structure that mechanically mirrors the OpenReview form
  (Summary / Strengths / Weaknesses / Questions) without paper-specific
  flow.
- Generic praise or generic criticism that could apply to any paper.
- Repetitive transition words ("Moreover", "Furthermore", "Additionally"),
  high em-dash density, "delve into", "tapestry", "in the realm of",
  "comprehensive", suspicious balance of pros and cons.
- Direct giveaways: "Chat.openai.com", "As an AI", "I cannot provide", "Certainly! Here is",
  copy-pasted system prompts, references to GPT/Claude.
- Lack of paper-specific engagement: no equation/figure/page numbers, no
  technical critiques tied to concrete claims, hallucinated citations.
- Counter-evidence (push toward human): specific section/equation
  references, idiosyncratic phrasing, narrow domain critique, typos /
  irregular formatting consistent with hand-written prose.

Respond with JSON ONLY (no prose, no code fences) matching this schema:
{{
  "score": <float 0.0-1.0, where 0 = clearly human, 1 = clearly LLM>,
  "verdict": <one of {VERDICT_VALUES}>,
  "signals": <list of up to 5 tags drawn ONLY from this fixed vocabulary:
              {SIGNAL_VOCAB}>,
  "rationale": <<= 280 chars, a single sentence justification>
}}
"""


# ---------------------------------------------------------------------------
# OpenReview helpers (mirrored from generate_accepted.py — kept local so the
# scripts directory stays a flat collection of one-shot tools without a
# shared module).
# ---------------------------------------------------------------------------

OPENREVIEW_API2 = "https://api2.openreview.net"


def make_client(username: str | None, password: str | None) -> openreview.api.OpenReviewClient:
    return openreview.api.OpenReviewClient(
        baseurl=OPENREVIEW_API2,
        username=username,
        password=password,
    )


def _content_value(content: dict, key: str):
    """Return the value of a note content field, handling v1/v2 shapes."""
    if key not in content:
        return None
    field = content[key]
    if isinstance(field, dict) and "value" in field:
        return field["value"]
    return field


def extract_forum_id(forum_url: str) -> str:
    parsed = urlparse(forum_url.strip())
    qs = parse_qs(parsed.query)
    if "id" not in qs or not qs["id"]:
        raise ValueError(f"could not parse forum id from URL: {forum_url!r}")
    return qs["id"][0]


def is_review_note(note) -> bool:
    """A note is an Official Review iff one of its invitations ends so."""
    invs = getattr(note, "invitations", None) or []
    return any(inv.endswith("/Official_Review") for inv in invs)


# Review fields the modern OpenReview review template uses. Different
# venues label the body fields differently (some use ``summary`` /
# ``strengths`` / ``weaknesses`` / ``questions``, others use ``review`` /
# ``main_review`` / ``comments``, older venues use ``Q*_review``). Rather
# than maintain a per-venue allow-list, we render *every* string-valued
# content field except the known metadata fields below. The rendering
# preserves field names as section headings so the judge sees the
# structure of the review.
REVIEW_METADATA_FIELDS = frozenset(
    {
        "rating",
        "confidence",
        "title",
        "soundness",
        "presentation",
        "contribution",
        "code_of_conduct",
        "ethics_review_needed",
        "ethics_flag",
        "flag_for_ethics_review",
        "details_of_ethics_concerns",
        "venue",
        "venueid",
        "writing_quality",
        "originality",
        "significance",
        "clarity",
        "quality",
    }
)

# Preferred ordering for fields we recognise — anything else is appended
# in alphabetical order so the rendering is stable.
PREFERRED_FIELD_ORDER = (
    "summary",
    "paper_summary",
    "main_review",
    "review",
    "strengths",
    "weaknesses",
    "strengths_and_weaknesses",
    "questions",
    "limitations",
    "comments",
    "additional_comments",
)


def render_review_text(note) -> str:
    """Render every text body field of a review note as Markdown sections."""
    content = note.content or {}
    parts: list[tuple[str, str]] = []
    for field, raw in content.items():
        if field in REVIEW_METADATA_FIELDS:
            continue
        v = _content_value(content, field)
        if not isinstance(v, str):
            continue
        v = v.strip()
        # Skip empty / placeholder values ("N/A", "-") but keep anything
        # with real prose, even single-line answers.
        if len(v) < 4 or v.lower() in {"n/a", "na", "none", "-", "--"}:
            continue
        parts.append((field, v))

    # Sort by preferred order, then alphabetical for the rest.
    order = {name: i for i, name in enumerate(PREFERRED_FIELD_ORDER)}
    parts.sort(key=lambda kv: (order.get(kv[0], len(order)), kv[0]))

    return "\n\n".join(
        f"## {field.replace('_', ' ').title()}\n{value}" for field, value in parts
    ).strip()


# ---------------------------------------------------------------------------
# Cache (JSONL)
# ---------------------------------------------------------------------------


def load_done_review_ids(path: Path, schema_version: int) -> set[str]:
    """Return the set of review_ids already judged at the current schema."""
    if not path.exists():
        return set()
    done: set[str] = set()
    with path.open("r", encoding="utf-8") as f:
        for lineno, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                print(
                    f"warning: {path}:{lineno}: skipping malformed line ({exc})",
                    file=sys.stderr,
                )
                continue
            if row.get("schema_version") != schema_version:
                continue
            rid = row.get("review_id")
            if rid:
                done.add(rid)
    return done


def append_row(path: Path, row: dict) -> None:
    """Append one JSON object as a single line, then flush+fsync."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
    # Open in append+binary so the OS guarantees atomic O_APPEND for the
    # full line on POSIX. Writes from a single process never interleave.
    with open(path, "ab") as f:
        f.write(line.encode("utf-8"))
        f.flush()
        os.fsync(f.fileno())


# ---------------------------------------------------------------------------
# Claude CLI judge
# ---------------------------------------------------------------------------


class JudgeError(RuntimeError):
    """Wraps any failure that should be recorded but not abort the run."""


def call_claude(
    review_text: str,
    *,
    model: str,
    timeout: float,
    claude_bin: str,
) -> dict:
    """Invoke ``claude -p`` and return the parsed judgment dict.

    Raises :class:`JudgeError` on any CLI failure or unparseable output.
    """
    cmd = [
        claude_bin,
        "-p",
        "--output-format",
        "json",
        "--model",
        model,
        "--system-prompt",
        JUDGE_SYSTEM_PROMPT,
        review_text,
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise JudgeError(f"claude CLI timed out after {timeout}s") from exc
    except FileNotFoundError as exc:
        raise JudgeError(f"claude CLI not found at {claude_bin!r}") from exc

    if proc.returncode != 0:
        stderr_tail = (proc.stderr or "").strip().splitlines()[-3:]
        raise JudgeError(
            f"claude exited {proc.returncode}: {' | '.join(stderr_tail) or '(no stderr)'}"
        )

    try:
        envelope = json.loads(proc.stdout)
    except json.JSONDecodeError as exc:
        raise JudgeError(f"claude stdout not valid JSON: {exc}") from exc

    # ``--output-format json`` wraps the model reply in a metadata envelope;
    # the textual reply is in the ``result`` field.
    result_text = envelope.get("result")
    if not isinstance(result_text, str):
        raise JudgeError(f"claude envelope missing 'result' string: keys={list(envelope)}")

    judgment = _parse_judgment(result_text)
    return judgment


def _parse_judgment(raw: str) -> dict:
    """Pull out the JSON judgment, tolerating stray prose or fences."""
    s = raw.strip()
    # Strip a single ```json ... ``` fence if the model added one.
    if s.startswith("```"):
        s = s.strip("`")
        # remove a leading "json\n" tag if present
        if s.lower().startswith("json"):
            s = s[4:].lstrip()
    # If there's still text around the JSON, locate the outermost braces.
    if not s.startswith("{"):
        first, last = s.find("{"), s.rfind("}")
        if first == -1 or last == -1 or last <= first:
            raise JudgeError(f"no JSON object in judge output: {raw[:200]!r}")
        s = s[first : last + 1]

    try:
        obj = json.loads(s)
    except json.JSONDecodeError as exc:
        raise JudgeError(f"judge output not valid JSON: {exc}; head={s[:200]!r}") from exc

    # Light schema validation — fix obvious model slop, otherwise raise.
    score = obj.get("score")
    if not isinstance(score, (int, float)):
        raise JudgeError(f"judgment missing numeric 'score': {obj!r}")
    obj["score"] = max(0.0, min(1.0, float(score)))

    verdict = obj.get("verdict")
    if verdict not in VERDICT_VALUES:
        raise JudgeError(f"judgment 'verdict' not in {VERDICT_VALUES}: {verdict!r}")

    signals = obj.get("signals") or []
    if not isinstance(signals, list):
        raise JudgeError(f"judgment 'signals' must be a list: {signals!r}")
    obj["signals"] = [s for s in signals if s in SIGNAL_VOCAB][:5]

    rationale = obj.get("rationale") or ""
    if not isinstance(rationale, str):
        raise JudgeError(f"judgment 'rationale' must be a string: {rationale!r}")
    obj["rationale"] = rationale.strip()[:280]

    return obj


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_submissions(csv_path: Path, only_decision: str | None) -> list[dict]:
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if only_decision is not None:
        rows = [r for r in rows if r["decision"] == only_decision]
    return rows


def iter_review_notes(client, forum_id: str) -> Iterable:
    """Yield Official_Review notes for one forum, oldest first."""
    notes = client.get_all_notes(forum=forum_id)
    reviews = [n for n in notes if is_review_note(n)]
    # Oldest first: stable across runs even though we cache by review_id.
    reviews.sort(key=lambda n: getattr(n, "cdate", 0) or 0)
    return reviews


def process_submission(
    client,
    row: dict,
    *,
    out_path: Path,
    done: set[str],
    model: str,
    timeout: float,
    claude_bin: str,
    dry_run: bool,
) -> tuple[int, int, int]:
    """Process one submission row.

    Returns a tuple ``(n_judged, n_cached, n_errors)``.
    """
    forum_url = row["forum"].strip()
    forum_id = extract_forum_id(forum_url)
    submission_number = int(row["number"]) if row.get("number") else None

    try:
        reviews = list(iter_review_notes(client, forum_id))
    except Exception as exc:  # noqa: BLE001
        print(f"  ! forum {forum_id}: failed to fetch reviews: {exc}", file=sys.stderr)
        return (0, 0, 1)

    n_judged = n_cached = n_errors = 0
    for note in reviews:
        if note.id in done:
            n_cached += 1
            continue

        review_text = render_review_text(note)
        if not review_text:
            # Empty review body — nothing to judge. Record it so we don't
            # keep re-checking on every run.
            row_out = {
                "schema_version": SCHEMA_VERSION,
                "submission_number": submission_number,
                "forum_id": forum_id,
                "review_id": note.id,
                "reviewer_signature": _first_signature(note),
                "review_length": 0,
                "rating": _maybe_int(_content_value(note.content, "rating")),
                "confidence": _maybe_int(_content_value(note.content, "confidence")),
                "judged_at": now_iso(),
                "model": model,
                "error": "empty_review",
                "content_keys": sorted((note.content or {}).keys()),
            }
            append_row(out_path, row_out)
            done.add(note.id)
            n_errors += 1
            print(
                f"  ! review {note.id}: empty body "
                f"(content keys: {sorted((note.content or {}).keys())})",
                file=sys.stderr,
            )
            continue

        if dry_run:
            print(
                f"  · would judge review_id={note.id} ({len(review_text)} chars)",
                file=sys.stderr,
            )
            continue

        base_row = {
            "schema_version": SCHEMA_VERSION,
            "submission_number": submission_number,
            "forum_id": forum_id,
            "review_id": note.id,
            "reviewer_signature": _first_signature(note),
            "review_length": len(review_text),
            "rating": _maybe_int(_content_value(note.content, "rating")),
            "confidence": _maybe_int(_content_value(note.content, "confidence")),
            "judged_at": now_iso(),
            "model": model,
        }
        try:
            judgment = call_claude(
                review_text, model=model, timeout=timeout, claude_bin=claude_bin
            )
        except JudgeError as exc:
            base_row["error"] = str(exc)
            append_row(out_path, base_row)
            done.add(note.id)
            n_errors += 1
            print(f"  ! review {note.id}: {exc}", file=sys.stderr)
            continue

        base_row.update(judgment)
        append_row(out_path, base_row)
        done.add(note.id)
        n_judged += 1
        print(
            f"    {note.id} → {judgment['verdict']} "
            f"(score={judgment['score']:.2f}, signals={judgment['signals']})",
            file=sys.stderr,
        )

    return (n_judged, n_cached, n_errors)


def _first_signature(note) -> str | None:
    sigs = getattr(note, "signatures", None) or []
    return sigs[0] if sigs else None


def _maybe_int(v) -> int | None:
    if v is None:
        return None
    # OpenReview ratings are usually formatted "5: ..." — keep just the int.
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v).strip()
    head = s.split(":", 1)[0].strip()
    try:
        return int(head)
    except ValueError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, default=Path("submissions.csv"))
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("scripts/check_reviews_results.jsonl"),
        help="JSONL cache file (default: scripts/check_reviews_results.jsonl).",
    )
    parser.add_argument(
        "--username", default=os.environ.get("OPENREVIEW_USERNAME"),
        help="OpenReview username (default: $OPENREVIEW_USERNAME).",
    )
    parser.add_argument(
        "--password", default=os.environ.get("OPENREVIEW_PASSWORD"),
        help="OpenReview password (default: $OPENREVIEW_PASSWORD).",
    )
    parser.add_argument(
        "--prompt-password", action="store_true",
        help="Prompt for the OpenReview password interactively.",
    )
    parser.add_argument(
        "--model", default="claude-sonnet-4-6",
        help="Claude model id passed to the CLI (default: claude-sonnet-4-6).",
    )
    parser.add_argument(
        "--claude-bin", default="claude",
        help="Path to the claude CLI (default: looked up on $PATH).",
    )
    parser.add_argument(
        "--timeout", type=float, default=120.0,
        help="Per-review CLI timeout in seconds (default: 120).",
    )
    parser.add_argument(
        "--max-submissions", type=int, default=None,
        help="Process at most N submissions (useful for smoke-testing).",
    )
    parser.add_argument(
        "--only-decision", default=None,
        help="Only process rows whose decision exactly matches this string.",
    )
    parser.add_argument(
        "--redo", action="store_true",
        help="Ignore the cache and re-judge everything.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Fetch reviews and report what would be judged, but don't call claude.",
    )
    args = parser.parse_args()

    if not args.csv.is_file():
        print(f"error: CSV file not found: {args.csv}", file=sys.stderr)
        return 1

    if args.prompt_password and not args.password:
        args.password = getpass.getpass("OpenReview password: ")
    if args.username and not args.password:
        print(
            "error: --username given but no password (set $OPENREVIEW_PASSWORD "
            "or pass --password / --prompt-password).",
            file=sys.stderr,
        )
        return 1

    rows = load_submissions(args.csv, args.only_decision)
    if args.max_submissions is not None:
        rows = rows[: args.max_submissions]
    print(f"Loaded {len(rows)} submissions from {args.csv}", file=sys.stderr)

    done = set() if args.redo else load_done_review_ids(args.out, SCHEMA_VERSION)
    if done:
        print(
            f"Cache: {len(done)} reviews already judged at schema_version={SCHEMA_VERSION}",
            file=sys.stderr,
        )

    client = make_client(args.username, args.password)

    total_judged = total_cached = total_errors = 0
    t0 = time.monotonic()
    for i, row in enumerate(rows, 1):
        title = (row.get("title") or "").strip()[:60]
        forum_url = row["forum"].strip()
        print(
            f"[{i}/{len(rows)}] {forum_url}  {title!r}",
            file=sys.stderr,
        )
        n_j, n_c, n_e = process_submission(
            client,
            row,
            out_path=args.out,
            done=done,
            model=args.model,
            timeout=args.timeout,
            claude_bin=args.claude_bin,
            dry_run=args.dry_run,
        )
        total_judged += n_j
        total_cached += n_c
        total_errors += n_e
        print(
            f"  = {n_j} judged, {n_c} cached, {n_e} errors",
            file=sys.stderr,
        )

    elapsed = time.monotonic() - t0
    print(
        f"\nDone in {elapsed:.1f}s — judged={total_judged} "
        f"cached={total_cached} errors={total_errors}",
        file=sys.stderr,
    )
    print(f"Output: {args.out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
