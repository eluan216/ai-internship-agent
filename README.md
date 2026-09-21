# AI Internship Agent

Python agent that searches public internship listings, filters them, ranks matches with **explainable scores**, caches results, and writes a markdown shortlist.

**Learning / portfolio project.** It does not auto-apply and does not scrape login-walled sites.

---

## Architecture

```
User query
   ↓
SearchQuery
   ↓
Search tool ── Remotive API (live)
            └─ Demo fixtures (offline)
   ↓
Listing objects
   ↓
Heuristic ranker (scored + reasons)
   ↓
JSON cache
   ↓
Markdown shortlist (CLI)
```

Tools are independent so an LLM tool-calling layer can be added later without rewriting search/rank/cache.

---

## Quick start

```bash
python -m venv .venv

# Windows PowerShell
.\\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

# Offline demo (no API key, no network required)
python cli.py --demo -k machine learning internship -n 5

# Live search
python cli.py -k "data science" intern -l Remote -n 8 -o shortlist.md
```

---

## Tests

```bash
pip install pytest
pytest tests/ -v
```

Coverage includes models, search filters, deterministic ranking, cache round-trip, markdown formatting, agent loop, and CLI.

---

## Ranking evaluation

```bash
python evaluation/evaluate.py
```

Uses demo fixtures + labeled query expectations to report **Precision@K** and a determinism check. This is a small, honest benchmark — not fabricated marketing metrics.

---

## Explainable ranking

Each shortlist item can include why it scored highly, for example:

- title matches `machine learning`
- internship-level role
- remote position

---

## Design rules

- Results stay grounded in real or demo listings (no invented jobs)
- Demo mode runs with zero credentials
- Live API failure falls back to demo
- No automatic applications

---

## Status

| Area | Status |
|------|--------|
| Demo + live search | Done |
| Explainable heuristic ranker | Done |
| Cache + markdown output | Done |
| Automated tests | Done |
| Ranking evaluation harness | Done |
| Second job source | Next |
| LLM tool-calling layer | Later (optional) |

See [PRD.md](./PRD.md).

---

eluan216
