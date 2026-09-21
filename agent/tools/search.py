"""
Listing search tools.

Uses public, key-free sources where possible.
Remotive (remote jobs API) is the primary live source.
A curated demo set is used when offline or when --demo is set.
"""

from typing import List
import hashlib
import requests

from agent.models import Listing, SearchQuery

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"


DEMO_LISTINGS = [
    Listing(
        id="demo-1",
        title="Machine Learning Intern",
        company="Northstar Health",
        location="Remote",
        url="https://example.com/jobs/ml-intern",
        source="demo",
        posted_at="2026-09-10",
        description="Work on clinical NLP prototypes and evaluation pipelines.",
        tags=["ml", "python", "nlp", "internship"],
    ),
    Listing(
        id="demo-2",
        title="Data Science Intern",
        company="Rivian",
        location="Irvine, CA",
        url="https://example.com/jobs/ds-intern",
        source="demo",
        posted_at="2026-09-12",
        description="Support analytics for manufacturing and vehicle telemetry.",
        tags=["data science", "python", "sql", "internship"],
    ),
    Listing(
        id="demo-3",
        title="AI Research Intern",
        company="University Lab Collaborations",
        location="Remote",
        url="https://example.com/jobs/ai-research",
        source="demo",
        posted_at="2026-09-08",
        description="Literature review, experiment tracking, and model fine-tuning.",
        tags=["ai", "research", "pytorch", "internship"],
    ),
    Listing(
        id="demo-4",
        title="Software Engineering Intern – Backend",
        company="Fintech Startup",
        location="New York, NY",
        url="https://example.com/jobs/swe-backend",
        source="demo",
        posted_at="2026-09-15",
        description="APIs, databases, and internal tooling in Python.",
        tags=["software", "python", "backend", "internship"],
    ),
    Listing(
        id="demo-5",
        title="Cybersecurity Intern",
        company="Regional Bank",
        location="Hybrid – NYC",
        url="https://example.com/jobs/cyber-intern",
        source="demo",
        posted_at="2026-09-05",
        description="Assist with vulnerability assessment and security monitoring.",
        tags=["security", "cyber", "internship"],
    ),
    Listing(
        id="demo-6",
        title="Bioinformatics Intern",
        company="Biotech Research Group",
        location="Boston, MA",
        url="https://example.com/jobs/bioinfo",
        source="demo",
        posted_at="2026-09-14",
        description="Genomics data pipelines and statistical analysis.",
        tags=["bioinformatics", "python", "r", "internship"],
    ),
]


def _id_from(title: str, company: str, url: str) -> str:
    raw = f"{title}|{company}|{url}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]


def _keyword_matches(text: str, keywords) -> bool:
    """True if any keyword phrase matches the text.

    A phrase matches if the full phrase appears, or (for multi-word phrases)
    every token longer than 2 characters appears somewhere in the text.
    """
    if not keywords:
        return True
    text = text.lower()
    for k in keywords:
        k = (k or "").lower().strip()
        if not k:
            continue
        if k in text:
            return True
        parts = [p for p in k.split() if len(p) > 2]
        if parts and all(p in text for p in parts):
            return True
    return False


def search_remotive(query: SearchQuery) -> List[Listing]:
    """Fetch remote jobs from Remotive public API and filter locally."""
    try:
        resp = requests.get(REMOTIVE_URL, timeout=20)
        resp.raise_for_status()
        jobs = resp.json().get("jobs", [])
    except Exception:
        return []

    keywords = query.keywords or []
    results: List[Listing] = []

    for job in jobs:
        title = (job.get("title") or "").strip()
        company = (job.get("company_name") or "").strip()
        location = (job.get("candidate_required_location") or "Remote").strip()
        url = (job.get("url") or "").strip()
        desc = (job.get("description") or "")[:500]
        cats = [str(c).lower() for c in (job.get("tags") or [])]
        category = (job.get("category") or "").lower()
        text = f"{title} {company} {desc} {category} {' '.join(cats)}".lower()

        if keywords and not _keyword_matches(text, keywords):
            continue
        if query.location and query.location.lower() not in location.lower():
            if not (query.remote_ok and "remote" in location.lower()):
                if not query.remote_ok:
                    continue

        results.append(
            Listing(
                id=_id_from(title, company, url),
                title=title or "Untitled",
                company=company or "Unknown",
                location=location or "Remote",
                url=url,
                source="remotive",
                posted_at=job.get("publication_date"),
                description=desc,
                tags=cats[:8],
            )
        )
        if len(results) >= query.limit * 3:
            break

    return results[: query.limit * 2]


def search_demo(query: SearchQuery) -> List[Listing]:
    out = []
    for item in DEMO_LISTINGS:
        text = f"{item.title} {item.company} {item.description} {' '.join(item.tags)}".lower()
        if query.keywords and not _keyword_matches(text, query.keywords):
            continue
        if query.location and query.location.lower() not in item.location.lower():
            if not (query.remote_ok and "remote" in item.location.lower()):
                continue
        out.append(item)
    return out[: query.limit]


def search_listings(query: SearchQuery, demo: bool = False) -> List[Listing]:
    if demo:
        return search_demo(query)
    live = search_remotive(query)
    if live:
        return live
    return search_demo(query)
