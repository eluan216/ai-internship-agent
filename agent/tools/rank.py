"""Heuristic ranking with explainable score breakdown."""

from typing import List, Dict, Any
from agent.models import Listing, SearchQuery


def score_listing(item: Listing, query: SearchQuery) -> Dict[str, Any]:
    """Return total score and human-readable reasons."""
    keywords = [k.lower() for k in query.keywords]
    reasons: List[str] = []
    score = 0.0

    title = (item.title or "").lower()
    blob = f"{item.title} {item.company} {item.description} {' '.join(item.tags)}".lower()

    for k in keywords:
        if k in title:
            score += 3.0
            reasons.append(f"title matches '{k}'")
        elif k in blob:
            score += 1.5
            reasons.append(f"description/tags match '{k}'")

    if "intern" in title or "internship" in blob:
        score += 2.0
        reasons.append("internship-level role")

    if query.remote_ok and "remote" in (item.location or "").lower():
        score += 1.0
        reasons.append("remote position")

    if query.location and query.location.lower() in (item.location or "").lower():
        score += 1.5
        reasons.append(f"location matches '{query.location}'")

    return {"score": score, "reasons": reasons}


def rank_listings(listings: List[Listing], query: SearchQuery) -> List[Listing]:
    scored = []
    for item in listings:
        result = score_listing(item, query)
        item.score = result["score"]
        # stash reasons on the object for the formatter (non-serialized helper)
        setattr(item, "_reasons", result["reasons"])
        scored.append(item)

    ranked = sorted(scored, key=lambda x: (-x.score, x.title.lower()))
    return ranked[: query.limit]
