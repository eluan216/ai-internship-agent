"""
Listing search orchestration.

Sources implement JobSource and return normalized Listing objects.
Live mode merges Remotive + RemoteOK, then the caller deduplicates.
Demo mode uses DemoSource only.
"""

from typing import List

from agent.models import Listing, SearchQuery
from agent.sources.demo import DemoSource, DEMO_LISTINGS
from agent.sources.remotive import RemotiveSource
from agent.sources.remoteok import RemoteOKSource

# Re-export for tests that import from agent.tools.search
__all__ = [
    "DEMO_LISTINGS",
    "_keyword_matches",
    "search_demo",
    "search_remotive",
    "search_listings",
]


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
    return DemoSource().search(query)
