"""Offline demo fixtures."""

from typing import List

from agent.models import Listing, SearchQuery
from agent.sources.base import JobSource
from agent.tools.search import DEMO_LISTINGS, _keyword_matches


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


# Protocol compliance check at import time (structural)
def _check() -> JobSource:
    return DemoSource()
