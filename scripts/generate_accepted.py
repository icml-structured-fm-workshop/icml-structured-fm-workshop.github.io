"""
Generate ``_bibliography/papers.bib`` for the FMSD workshop website
from an OpenReview submissions CSV export.

Reads ``submissions.csv`` (OpenReview export), drops rejected papers, and
emits a BibTeX file with one ``@inproceedings`` entry per accepted paper.
Author names are resolved by querying the OpenReview API (v2) for each
paper's forum note.

Usage:
    python scripts/generate_accepted.py \
        [--csv submissions.csv] \
        [--out _bibliography/papers.bib] \
        [--username USER] [--password PW]

Credentials may also be supplied via the ``OPENREVIEW_USERNAME`` /
``OPENREVIEW_PASSWORD`` environment variables. Anonymous access works
only for public venues; FMSD submissions typically require a logged-in
PC/organizer account.
"""

from __future__ import annotations

import argparse
import csv
import getpass
import os
import re
import sys
from pathlib import Path
from urllib.parse import parse_qs, urlparse

import openreview  # noqa: F401  (ensures the package is importable up-front)
import openreview.api


# Decision strings as they appear in the OpenReview CSV export.
SPOTLIGHT_DECISION = "Accept (Spotlight Oral)"
POSTER_DECISION = "Accept (Poster)"
ACCEPT_DECISIONS = {SPOTLIGHT_DECISION, POSTER_DECISION}

# Booktitle used for every entry — matches the convention in papers-2025.bib.
BOOKTITLE = "2nd ICML Workshop on Foundation Models for Structured Data"
YEAR = "2026"

OPENREVIEW_API2 = "https://api2.openreview.net"


def load_accepted(csv_path: Path) -> list[dict]:
    """Read the CSV and return only accepted rows."""
    # ``utf-8-sig`` strips the BOM that OpenReview includes on the header line.
    with csv_path.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        return [row for row in reader if row["decision"] in ACCEPT_DECISIONS]


def extract_forum_id(forum_url: str) -> str:
    """Extract the ``id=...`` parameter from an OpenReview forum URL."""
    parsed = urlparse(forum_url.strip())
    qs = parse_qs(parsed.query)
    if "id" not in qs or not qs["id"]:
        raise ValueError(f"could not parse forum id from URL: {forum_url!r}")
    return qs["id"][0]


def make_client(username: str | None, password: str | None) -> openreview.api.OpenReviewClient:
    """Create an OpenReview API v2 client, optionally authenticated."""
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
    # API v2 wraps values in {"value": ...}; API v1 stores them directly.
    if isinstance(field, dict) and "value" in field:
        return field["value"]
    return field


def fetch_authors(client: openreview.api.OpenReviewClient, forum_id: str) -> list[str]:
    """Return the list of author names for an OpenReview forum note."""
    note = client.get_note(forum_id)
    authors = _content_value(note.content, "authors")
    if not authors:
        raise RuntimeError(f"no authors found for forum {forum_id}")
    if isinstance(authors, str):
        # Defensive: occasionally a single author may come back as a string.
        authors = [authors]
    return list(authors)


def make_citekey(first_author: str, title: str, year: str, used: set[str]) -> str:
    """Build a stable BibTeX citation key, deduplicating against ``used``."""
    last = first_author.strip().split()[-1] if first_author.strip() else "anon"
    last = re.sub(r"[^A-Za-z]", "", last).lower() or "anon"
    first_word = ""
    for word in re.findall(r"[A-Za-z]+", title):
        if word.lower() in {"a", "an", "the", "on", "of", "for", "to", "in", "and", "or"}:
            continue
        first_word = word.lower()
        break
    base = f"{last}{year}{first_word}" if first_word else f"{last}{year}"
    key = base
    n = 2
    while key in used:
        key = f"{base}{n}"
        n += 1
    used.add(key)
    return key


# Characters that need escaping inside a brace-delimited BibTeX field.
_BRACE_RE = re.compile(r"([{}])")


def bib_escape(value: str) -> str:
    """Escape a value for inclusion inside ``{...}`` in a BibTeX field.

    We deliberately keep this minimal: OpenReview titles and author names
    are already plain Unicode, which biblatex / jekyll-scholar handle fine.
    We only protect against unbalanced braces and strip surrounding
    whitespace.
    """
    return _BRACE_RE.sub(r"\\\1", value).strip()


def render_entry(citekey: str, title: str, authors: list[str], forum_url: str) -> str:
    """Render a single ``@inproceedings`` entry, matching the 2025 style."""
    author_field = " and ".join(bib_escape(a) for a in authors)
    return (
        f"@inproceedings{{\n"
        f"{citekey},\n"
        f"title={{{bib_escape(title)}}},\n"
        f"author={{{author_field}}},\n"
        f"booktitle={{{BOOKTITLE}}},\n"
        f"year={{{YEAR}}},\n"
        f"url={{{forum_url.strip()}}}\n"
        f"}}\n"
    )


def render_bib(entries: list[str]) -> str:
    """Wrap the entries in the YAML front matter required by jekyll-scholar."""
    return "---\n---\n" + "\n".join(entries)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path("submissions.csv"),
        help="Path to the OpenReview submissions CSV (default: submissions.csv).",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("_bibliography/papers.bib"),
        help="Output BibTeX file (default: _bibliography/papers.bib).",
    )
    parser.add_argument(
        "--username",
        default=os.environ.get("OPENREVIEW_USERNAME"),
        help="OpenReview username (default: $OPENREVIEW_USERNAME).",
    )
    parser.add_argument(
        "--password",
        default=os.environ.get("OPENREVIEW_PASSWORD"),
        help="OpenReview password (default: $OPENREVIEW_PASSWORD).",
    )
    parser.add_argument(
        "--prompt-password",
        action="store_true",
        help="Prompt for the OpenReview password interactively.",
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

    rows = load_accepted(args.csv)
    n_spot = sum(1 for r in rows if r["decision"] == SPOTLIGHT_DECISION)
    n_post = sum(1 for r in rows if r["decision"] == POSTER_DECISION)
    print(
        f"Found {len(rows)} accepted papers "
        f"({n_spot} spotlight oral, {n_post} poster).",
        file=sys.stderr,
    )
    if not rows:
        print("warning: no accepted papers — writing an empty .bib file.", file=sys.stderr)

    client = make_client(args.username, args.password)

    # Sort by title for stable output, matching the on-page ordering.
    rows = sorted(rows, key=lambda r: r["title"].strip().lower())

    entries: list[str] = []
    used_keys: set[str] = set()
    failures: list[tuple[str, str]] = []
    for row in rows:
        title = row["title"].strip()
        forum_url = row["forum"].strip()
        try:
            forum_id = extract_forum_id(forum_url)
            authors = fetch_authors(client, forum_id)
        except Exception as exc:  # noqa: BLE001 — surface any API/parse error
            print(f"  ! {title!r}: {exc}", file=sys.stderr)
            failures.append((title, str(exc)))
            continue

        citekey = make_citekey(authors[0], title, YEAR, used_keys)
        entries.append(render_entry(citekey, title, authors, forum_url))
        print(f"  ✓ {citekey}: {len(authors)} author(s)", file=sys.stderr)

    output = render_bib(entries)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(output, encoding="utf-8")
    print(
        f"Wrote {len(entries)} entries to {args.out}"
        + (f" ({len(failures)} failed)" if failures else ""),
        file=sys.stderr,
    )

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
