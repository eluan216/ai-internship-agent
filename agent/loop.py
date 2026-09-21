"""
Agent loop: parse intent → search tool → rank → save cache → markdown.

Designed so an LLM can later call the same tools; the default path is
deterministic and works without an API key.
"""

from typing import List, Optional

from agent.models import SearchQuery, Listing
from agent.tools.search import search_listings
from agent.tools.rank import rank_listings
from agent.tools.format import to_markdown
from agent.cache import save_listings


def build_query(
    keywords: Optional[List[str]] = None,
    location: str = "",
    remote_ok: bool = True,
    limit: int = 10,
) -> SearchQuery:
    kw = keywords or ["internship", "intern"]
    return SearchQuery(
        keywords=kw,
        location=location,
        remote_ok=remote_ok,
        limit=limit,
    )


def run_agent(
    keywords: Optional[List[str]] = None,
    location: str = "",
    remote_ok: bool = True,
    limit: int = 10,
    demo: bool = False,
) -> str:
    query = build_query(keywords=keywords, location=location, remote_ok=remote_ok, limit=limit)

    # Tool 1: search
    raw = search_listings(query, demo=demo)

    # Tool 2: rank (heuristic; swap for LLM later if desired)
    ranked = rank_listings(raw, query)

    # Tool 3: persist
    cache_key = "_".join(query.keywords)[:40] or "default"
    save_listings(cache_key, ranked)

    # Output
    return to_markdown(ranked, query)
