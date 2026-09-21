"""Shared data models."""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class Listing:
    id: str
    title: str
    company: str
    location: str
    url: str
    source: str
    posted_at: Optional[str] = None
    description: str = ""
    tags: List[str] = field(default_factory=list)
    score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SearchQuery:
    keywords: List[str]
    location: str = ""
    remote_ok: bool = True
    max_age_days: int = 30
    limit: int = 20
