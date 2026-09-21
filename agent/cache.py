"""Simple local JSON cache for listings."""

from pathlib import Path
import json
from typing import List, Optional
from datetime import datetime, timezone

from agent.models import Listing

CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"


def _path(key: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in key)[:80]
    return CACHE_DIR / f"{safe}.json"


def save_listings(key: str, listings: List[Listing]) -> Path:
    path = _path(key)
    payload = {
        "saved_at": datetime.now(timezone.utc).isoformat(),
        "count": len(listings),
        "listings": [x.to_dict() for x in listings],
    }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def load_listings(key: str) -> Optional[List[Listing]]:
    path = _path(key)
    if not path.exists():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return [Listing(**item) for item in data.get("listings", [])]
