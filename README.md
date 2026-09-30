# AI Internship Agent

I built a tool-oriented internship discovery system that pulls listings from multiple sources, normalizes them into one model, removes duplicates, ranks with an explainable heuristic, and measures retrieval quality with Precision@K — including a mocked multi-source path that does not depend on the network.

This is engineering work by **eluan216**. It is not an auto-apply bot, not an LLM wrapper, and it does not scrape login-walled sites.

---

## Problem

Internship search is fragmented. I wanted a shortlist I could trust: real postings, visible ranking reasons, and an evaluation story that survives a skeptical reviewer.

---

## Architecture

```
SearchQuery
     │
┌────┴────┬─────────┐
▼         ▼         ▼
Demo   Remotive  RemoteOK
│         │         │
└────┬────┴─────────┘
     ▼
Normalize → Listing
     ▼
Deduplicate (URL, then title+company)
     ▼
Heuristic rank + explanations
     ▼
Cache + markdown shortlist
```

Every source implements the same `JobSource` contract. Ranking code never special-cases an API.

---

## What I optimized for

| Concern | Approach |
|---------|----------|
| Source failures | Live merge; total failure falls back to demo fixtures |
| Duplicate postings | Deterministic dedupe before rank |
| Opaque ranking | Each item can show score reasons |
| Unstable live eval | Mocked multi-source suite in CI |
| Overclaiming quality | Demo Precision@K baseline kept at 0.20 and explained |

---

## Evaluation

| Suite | What it proves |
|-------|----------------|
| `evaluation/evaluate.py` | 15 demo queries; category breakdown; determinism |
| `evaluation/evaluate_multisource.py` | Merge → dedupe → rank without network |
| `evaluation/baseline.json` | Historical 4-query Precision@5 = 0.20 preserved |

I did not tune ranking just to inflate Precision@K. The low demo score is a property of a small fixture set and broad keyword matching; it is documented on purpose.

---

## Run

```bash
pip install -r requirements.txt
python cli.py --demo -k "machine learning internship" -n 5
pytest tests/ -v
python evaluation/evaluate.py
python evaluation/evaluate_multisource.py
```

Example shortlist: [`examples/machine-learning-shortlist.md`](examples/machine-learning-shortlist.md)

---

## Limits

- Live boards change shape and rate limits  
- Heuristic rank is not a learned ranking model  
- No authentication, no apply automation, no LLM tool router in this freeze  

---

## Status

Frozen for portfolio presentation. CI runs tests, evaluation, and a demo CLI smoke path on every push to `main`.

eluan216
