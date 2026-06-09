# Foundation Models for Structured Data

Source Code for the [website](https://icml-structured-fm-workshop.github.io/) of the Second Workshop on Foundation Models for Structured Data at the Forty-Third [International Conference on Machine Learning (ICML)](https://icml.cc/), July 2026, Seoul, South Korea.

## Accepted papers

### Preparation

Export the paper list from OpenReview and save it as `submissions.csv` at the repo root.

Create a local Python venv and install the OpenReview Python client:

```bash
python -m venv .venv
source .venv/bin/activate
pip install openreview-py
```

### Update accepted papers

To regenerate the accepted-papers bibfile, run:

```bash
.venv/bin/python scripts/generate_accepted.py --username USERNAME --prompt-password
```

This reads `submissions.csv`, filters out rejected papers, resolves author names
via the OpenReview API, and writes `_bibliography/papers.bib`.

Credentials are required unless papers are already public. 
Use any account with read access to the venue (typically a PC/organizer login).

