"""Deterministic listing deduplication before ranking."""

from typing import List
from urllib.parse import urlparse, urlunparse

from agent.models import Listing


def _norm_url(url: str) -> str:
    if not url:
        return ""
    try:
        p = urlparse(url.strip().lower())
        # drop query/fragment noise
        return urlunparse((p.scheme, p.netloc, p.path.rstrip("/"), "", "", ""))
    except Exception:
        return url.strip().lower()


def _norm_text(s: str) -> str:
    return " ".join((s or "").lower().split())


def dedupe_key(item: Listing) -> str:
    """Stable identity: prefer normalized URL, else title+company."""
    url_key = _norm_url(item.url)
    if url_key and url_key not in ("http://", "https://"):
        return f"url:{url_key}"
    return f"tc:{_norm_text(item.title)}|{_norm_text(item.company)}"


def deduplicate(listings: List[Listing]) -> List[Listing]:
    """Keep first occurrence of each key (stable order)."""
    seen = set()
    out: List[Listing] = []
    for item in listings:
        key = dedupe_key(item)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out
