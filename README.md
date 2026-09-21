# AI Internship Agent

Python agent that searches public internship listings from **multiple sources**, normalizes them, **deduplicates**, ranks with **explainable scores**, caches results, and writes a markdown shortlist.

**Learning / portfolio project.** It does not auto-apply and does not scrape login-walled sites.

---

## Architecture

```
SearchQuery
     │
┌────┴────┐
↓         ↓
Remotive  RemoteOK   (+ Demo offline)
│         │
└────┬────┘
     ↓
Normalize → Listing
     ↓
Deduplicate (URL / title+company)
     ↓
Heuristic ranker + explanations
     ↓
JSON cache → markdown shortlist
```

Each source implements a common `JobSource` interface and returns the same `Listing` model. Ranking does not special-case any API.

---

## Quick start

```bash
python -m venv .venv
# Windows: .\.venv\Scripts\Activate.ps1
source .venv/bin/activate
pip install -r requirements.txt

python cli.py --demo -k "machine learning internship" -n 5
python cli.py -k data science intern -n 8 -o shortlist.md
```

---

## Tests & evaluation

```bash
pytest tests/ -v
python evaluation/evaluate.py
```

**Baseline (demo fixtures, before second source):** Mean Precision@5 = **0.20**  
See `evaluation/baseline.json`. The score reflects a small fixture set and broad `internship` matching — documented, not optimized away.

---

## Design rules

- Results stay grounded in real or demo listings (no invented jobs)
- Demo mode runs with zero credentials
- Live mode merges Remotive + RemoteOK; failures fall back to demo
- Deduplication is deterministic (normalized URL, then title+company)
- No automatic applications

---

## Status

| Area | Status |
|------|--------|
| JobSource interface | Done |
| Remotive + RemoteOK + Demo | Done |
| Deduplication | Done |
| Explainable ranking | Done |
| Tests | Done |
| Evaluation + baseline | Done |
| LLM / frontend / auto-apply | Out of scope |

See [PRD.md](./PRD.md).

---

eluan216
