# AI Internship Agent

A **tool-oriented job discovery and ranking system** that aggregates internship listings from multiple sources, normalizes and deduplicates results, ranks opportunities with an **explainable heuristic model**, and evaluates retrieval quality with reproducible Precision@K benchmarks.

**Learning / portfolio project.** Not an auto-apply bot. Not an LLM wrapper. No login-walled scraping.

---

## Problem

Internship search is fragmented across boards. Candidates need a short, ranked list they can act on — not invented jobs, not silent ranking, and not another opaque “AI” box.

---

## Architecture

```
                 SearchQuery
                     │
          ┌──────────┼──────────┐
          ↓          ↓          ↓
       Demo      Remotive    RemoteOK
          │          │          │
          └──────────┼──────────┘
                     ↓
                Normalize → Listing
                     ↓
                Deduplicate
                     ↓
                  Ranker
                     ↓
             Explainable score
                     ↓
               Cache + Markdown
```

Each source implements a common `JobSource` interface and returns the same `Listing` model. Ranking does not special-case any API.

---

## Supported sources

| Source | Mode | Notes |
|--------|------|--------|
| Demo | Offline | Built-in fixtures for tests and demos |
| Remotive | Live | Public remote-jobs API |
| RemoteOK | Live | Public API, no key |

Live mode merges Remotive + RemoteOK, then deduplicates. On total failure, falls back to demo.

---

## Ranking methodology

Transparent heuristic scores, for example:

- title keyword match
- description / tag match
- internship-level role signal
- remote preference
- location preference

Each shortlist item can include **why it ranked** (inspectable, not opaque).

---

## Deduplication strategy

1. Normalized URL (scheme + host + path; query stripped) when present  
2. Else normalized `title + company`  

First occurrence wins (stable order). Same title at different companies is kept.

---

## Evaluation methodology

| Suite | Purpose |
|-------|---------|
| `evaluation/evaluate.py` | Demo fixtures, **15 queries** across exact / skill / broad / constraint / multi-word |
| `evaluation/evaluate_multisource.py` | **Mocked** two-source merge → dedupe → rank (no network) |
| `evaluation/baseline.json` | Historical 4-query baseline (Precision@5 = 0.20) — **unchanged** |

Demo Precision@K reflects a small fixture set and broad `internship` matching. It is measured and documented, not optimized away.

Multi-source quality is validated with mocks so results are reproducible without live API variance.

---

## Quick start

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
source .venv/bin/activate
pip install -r requirements.txt

python cli.py --demo -k "machine learning internship" -n 5
python cli.py -k data science intern -n 8 -o shortlist.md

pytest tests/ -v
python evaluation/evaluate.py
python evaluation/evaluate_multisource.py
```

Example output: [`examples/machine-learning-shortlist.md`](examples/machine-learning-shortlist.md)

---

## Limitations

- Demo Precision@K is limited by fixture size and OR-style keyword matching
- Live APIs can change shape or rate-limit; failures fall back to demo
- Ranking is heuristic, not a trained learning-to-rank model
- No auto-apply, no authenticated boards, no LLM tool-calling (by design)

---

## Status

Feature-complete for portfolio freeze of the deterministic agent.  
Optional later path: LLM tool selection on top of the same tools — without rewriting sources, dedupe, or rank.

See [PRD.md](./PRD.md).

---

eluan216
