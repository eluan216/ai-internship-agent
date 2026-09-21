"""
Reproducible multi-source evaluation using mock sources (no network).

Exercises: merge → normalize (Listing) → deduplicate → rank.
Simulates two sources with intentional overlap to validate dedupe.
"""

from __future__ import annotations

from typing import List

from agent.models import Listing, SearchQuery
from agent.tools.dedupe import deduplicate
from agent.tools.rank import rank_listings


class MockSourceA:
    name = "mock-a"

    def search(self, query: SearchQuery) -> List[Listing]:
        return [
            Listing(
                id="a-1",
                title="Machine Learning Intern",
                company="Northstar Health",
                location="Remote",
                url="https://example.com/jobs/ml-intern",
                source=self.name,
                description="Clinical NLP and evaluation pipelines.",
                tags=["ml", "python", "internship"],
            ),
            Listing(
                id="a-2",
                title="Data Science Intern",
                company="Rivian",
                location="Irvine, CA",
                url="https://example.com/jobs/ds-intern",
                source=self.name,
                description="Telemetry analytics.",
                tags=["data science", "internship"],
            ),
            Listing(
                id="a-3",
                title="Marketing Intern",
                company="BrandCo",
                location="Remote",
                url="https://example.com/jobs/mkt",
                source=self.name,
                description="Social campaigns.",
                tags=["marketing"],
            ),
        ]


class MockSourceB:
    name = "mock-b"

    def search(self, query: SearchQuery) -> List[Listing]:
        return [
            # intentional duplicate of A (same URL)
            Listing(
                id="b-1",
                title="Machine Learning Intern",
                company="Northstar Health",
                location="Remote",
                url="https://example.com/jobs/ml-intern",
                source=self.name,
                description="Same role from another board.",
                tags=["ml", "internship"],
            ),
            Listing(
                id="b-2",
                title="AI Research Intern",
                company="University Lab",
                location="Remote",
                url="https://example.com/jobs/ai-research",
                source=self.name,
                description="Research and fine-tuning.",
                tags=["ai", "research", "internship"],
            ),
            Listing(
                id="b-3",
                title="Cybersecurity Intern",
                company="Regional Bank",
                location="Hybrid – NYC",
                url="https://example.com/jobs/cyber",
                source=self.name,
                description="Vulnerability assessment.",
                tags=["security", "cyber", "internship"],
            ),
        ]


def merge_sources(query: SearchQuery) -> List[Listing]:
    merged: List[Listing] = []
    for src in (MockSourceA(), MockSourceB()):
        merged.extend(src.search(query))
    return merged


def run_pipeline(query: SearchQuery) -> List[Listing]:
    raw = merge_sources(query)
    unique = deduplicate(raw)
    return rank_listings(unique, query)


def main() -> None:
    query = SearchQuery(
        keywords=["machine learning", "internship"],
        remote_ok=True,
        limit=10,
    )

    raw = merge_sources(query)
    unique = deduplicate(raw)
    ranked = rank_listings(unique, query)

    print("Mocked multi-source evaluation")
    print("=" * 50)
    print(f"Source A jobs:     {len(MockSourceA().search(query))}")
    print(f"Source B jobs:     {len(MockSourceB().search(query))}")
    print(f"Merged jobs:       {len(raw)}")
    print(f"Duplicates removed:{len(raw) - len(unique)}")
    print(f"Final unique jobs: {len(unique)}")
    print(f"Ranked (limit={query.limit}): {len(ranked)}")
    print()

    assert len(raw) == 6
    assert len(unique) == 5  # one URL duplicate removed
    assert len(raw) - len(unique) == 1

    # ML intern should rank first for this query
    assert ranked[0].title == "Machine Learning Intern"

    # determinism
    ranked2 = run_pipeline(query)
    assert [r.title for r in ranked] == [r.title for r in ranked2]

    print("Duplicate handling: PASS")
    print("Deterministic ranking: PASS")
    print("Top result:", ranked[0].title, f"(score={ranked[0].score:.1f})")
    print("Sources represented:", sorted({r.source for r in unique}))
    print("=" * 50)
    print("Multi-source mock pipeline: PASS")


if __name__ == "__main__":
    main()
