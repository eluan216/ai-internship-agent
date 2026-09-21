"""Remotive public remote-jobs API."""

from typing import List
import hashlib
import requests

from agent.models import Listing, SearchQuery

REMOTIVE_URL = "https://remotive.com/api/remote-jobs"


def _keyword_matches(text: str, keywords) -> bool:
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


def _id_from(title: str, company: str, url: str) -> str:
    raw = f"{title}|{company}|{url}".encode("utf-8")
    return hashlib.sha1(raw).hexdigest()[:12]


class RemotiveSource:
    name = "remotive"

    def search(self, query: SearchQuery) -> List[Listing]:
        try:
            resp = requests.get(REMOTIVE_URL, timeout=20)
            resp.raise_for_status()
            jobs = resp.json().get("jobs", [])
        except Exception:
            return []

        keywords = query.keywords or []
        results: List[Listing] = []

        for job in jobs:
            title = (job.get("title") or "").strip()
            company = (job.get("company_name") or "").strip()
            location = (job.get("candidate_required_location") or "Remote").strip()
            url = (job.get("url") or "").strip()
            desc = (job.get("description") or "")[:500]
            cats = [str(c).lower() for c in (job.get("tags") or [])]
            category = (job.get("category") or "").lower()
            text = f"{title} {company} {desc} {category} {' '.join(cats)}".lower()

            if keywords and not _keyword_matches(text, keywords):
                continue
            if query.location and query.location.lower() not in location.lower():
                if not (query.remote_ok and "remote" in location.lower()):
                    if not query.remote_ok:
                        continue

            results.append(
                Listing(
                    id=_id_from(title, company, url),
                    title=title or "Untitled",
                    company=company or "Unknown",
                    location=location or "Remote",
                    url=url,
                    source=self.name,
                    posted_at=job.get("publication_date"),
                    description=desc,
                    tags=cats[:8],
                )
            )
            if len(results) >= query.limit * 3:
                break

        return results[: query.limit * 2]
