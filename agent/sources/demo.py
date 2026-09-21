"""Offline demo fixtures source."""

from typing import List

from agent.models import Listing, SearchQuery


def _keyword_matches(text: str, keywords) -> bool:
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


class DemoSource:
    name = "demo"

    def search(self, query: SearchQuery) -> List[Listing]:
        out: List[Listing] = []
        for item in DEMO_LISTINGS:
            text = f"{item.title} {item.company} {item.description} {' '.join(item.tags)}".lower()
            if query.keywords and not _keyword_matches(text, query.keywords):
                continue
            if query.location and query.location.lower() not in item.location.lower():
                if not (query.remote_ok and "remote" in item.location.lower()):
                    continue
            out.append(item)
        return out[: query.limit]
