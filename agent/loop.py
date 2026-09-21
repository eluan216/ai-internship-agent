"""
Agent loop: parse intent → search sources → dedupe → rank → cache → markdown.
"""

from typing import List, Optional

from agent.models import SearchQuery, Listing
from agent.tools.search import search_listings
from agent.tools.dedupe import deduplicate
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

    raw = search_listings(query, demo=demo)
    unique = deduplicate(raw)
    ranked = rank_listings(unique, query)

    cache_key = "_".join(query.keywords)[:40] or "default"
    save_listings(cache_key, ranked)

    return to_markdown(ranked, query)
