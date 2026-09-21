# AI Internship Agent

Python agent that searches public internship/job listings, filters them, ranks matches, and writes a markdown shortlist you can act on.

**Learning / portfolio project.** It does not auto-apply and does not scrape login-walled sites.

---

## What it does

1. **Search** – live listings from a public API (Remotive), or offline **demo** data
2. **Filter** – keywords, location, remote preference
3. **Rank** – transparent heuristic scores (title/keyword/internship signals)
4. **Cache** – local JSON under `cache/`
5. **Output** – clean markdown shortlist (stdout or file)

No API key required for demo mode or for the default ranking path.

---

## Quick start

```bash
cd ai-internship-agent
python -m venv .venv

# Windows PowerShell
.\\.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

# Offline demo (always works)
python cli.py --demo -k machine learning internship -n 5

# Live search (needs network)
python cli.py -k "data science" intern -l Remote -n 8 -o shortlist.md
```

---

## CLI

| Flag | Meaning |
|------|---------|
| `-k / --keywords` | One or more keywords |
| `-l / --location` | Location substring |
| `--no-remote` | Do not boost remote roles |
| `-n / --limit` | Max items in shortlist |
| `--demo` | Use built-in sample listings |
| `-o / --output` | Write markdown to a file |

---

## Architecture

```
cli.py
  └── agent/loop.py          # search → rank → cache → format
        ├── tools/search.py  # Remotive API + demo fixtures
        ├── tools/rank.py    # heuristic ranking
        ├── tools/format.py  # markdown shortlist
        ├── cache.py         # local JSON cache
        └── models.py        # Listing, SearchQuery
```

The loop is structured so an LLM tool-calling layer can be added later without changing the tools.

---

## Design rules

- Results stay grounded in real or demo listings (no invented jobs)
- Demo mode runs with zero credentials
- No automatic applications
- No scraping of authenticated job boards

---

## Status

MVP scaffold complete: demo + live search, ranking, cache, markdown output.

See [PRD.md](./PRD.md).

---

eluan216
