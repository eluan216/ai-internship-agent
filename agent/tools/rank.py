"""Heuristic ranking — keeps results grounded without requiring an LLM."""

from typing import List
from agent.models import Listing, SearchQuery


def rank_listings(listings: List[Listing], query: SearchQuery) -> List[Listing]:
    keywords = [k.lower() for k in query.keywords]

    for item in listings:
        score = 0.0
        blob = f"{item.title} {item.company} {item.description} {' '.join(item.tags)}".lower()

        for k in keywords:
            if k in item.title.lower():
                score += 3.0
            elif k in blob:
                score += 1.5

        if query.remote_ok and "remote" in item.location.lower():
            score += 1.0
        if "intern" in item.title.lower() or "internship" in blob:
            score += 2.0

        item.score = score

    ranked = sorted(listings, key=lambda x: x.score, reverse=True)
    return ranked[: query.limit]
