"""
Listing search orchestration.

Sources implement JobSource and return normalized Listing objects.
Live mode merges Remotive + RemoteOK, then the caller deduplicates.
Demo mode uses DemoSource only.
"""

from typing import List

from agent.models import Listing, SearchQuery
from agent.sources.demo import DemoSource
from agent.sources.remotive import RemotiveSource
from agent.sources.remoteok import RemoteOKSource

# Re-export fixtures for tests / DemoSource
from agent.sources.demo import DemoSource as _DS  # noqa: F401

DEMO_LISTINGS = None  # populated below after import cycle safe path


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


# Demo listings live here so tests that import DEMO_LISTINGS keep working
from agent.models import Listing as _L

DEMO_LISTINGS = [
    _L(
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
    _L(
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
    _L(
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
    _L(
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
    _L(
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
    _L(
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


def search_demo(query: SearchQuery) -> List[Listing]:
    return DemoSource().search(query)


def search_remotive(query: SearchQuery) -> List[Listing]:
    return RemotiveSource().search(query)


def search_listings(query: SearchQuery, demo: bool = False) -> List[Listing]:
    """Aggregate sources. Deduplication is applied by the agent loop."""
    if demo:
        return DemoSource().search(query)

    merged: List[Listing] = []
    for source in (RemotiveSource(), RemoteOKSource()):
        try:
            merged.extend(source.search(query))
        except Exception:
            continue

    if merged:
        return merged
    # graceful fallback
    return DemoSource().search(query)
