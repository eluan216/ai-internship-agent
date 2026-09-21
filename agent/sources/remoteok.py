"""
RemoteOK public API — second live source.

Endpoint: https://remoteok.com/api
No API key required. First row may be metadata; job rows include id/url/position.
"""

from typing import List
import hashlib
import requests

from agent.models import Listing, SearchQuery
from agent.tools.search import _keyword_matches

REMOTEOK_URL = "https://remoteok.com/api"


def _id_from(title: str, company: str, url: str) -> str:
    raw = f"{title}|{company}|{url}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]


class RemoteOKSource:
    name = "remoteok"

    def search(self, query: SearchQuery) -> List[Listing]:
        try:
            resp = requests.get(
                REMOTEOK_URL,
                timeout=20,
                headers={"User-Agent": "ai-internship-agent/0.1 (portfolio)"},
            )
            resp.raise_for_status()
            rows = resp.json()
        except Exception:
            return []

        if not isinstance(rows, list):
            return []

        keywords = query.keywords or []
        results: List[Listing] = []

        for row in rows:
            if not isinstance(row, dict):
                continue
            # skip metadata banner row
            if "position" not in row and "title" not in row:
                continue

            title = (row.get("position") or row.get("title") or "").strip()
            company = (row.get("company") or "").strip()
            url = (row.get("url") or row.get("apply_url") or "").strip()
            location = (row.get("location") or "Remote").strip() or "Remote"
            desc = (row.get("description") or "")[:500]
            tags = [str(t).lower() for t in (row.get("tags") or [])][:8]

            if not title:
                continue

            text = f"{title} {company} {desc} {' '.join(tags)}".lower()
            if keywords and not _keyword_matches(text, keywords):
                continue
            if query.location and query.location.lower() not in location.lower():
                if not (query.remote_ok and "remote" in location.lower()):
                    if not query.remote_ok:
                        continue

            # prefer RemoteOK's own id when present
            rid = str(row.get("id") or "")
            lid = f"remoteok-{rid}" if rid else _id_from(title, company, url)

            results.append(
                Listing(
                    id=lid,
                    title=title,
                    company=company or "Unknown",
                    location=location,
                    url=url or f"https://remoteok.com/remote-jobs/{rid}",
                    source=self.name,
                    posted_at=str(row.get("date") or row.get("epoch") or "") or None,
                    description=desc,
                    tags=tags,
                )
            )
            if len(results) >= query.limit * 3:
                break

        return results[: query.limit * 2]
