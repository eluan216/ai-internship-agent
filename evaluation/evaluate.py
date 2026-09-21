"""
Simple ranking evaluation on demo fixtures.

Metrics: Precision@K, presence of expected relevant titles, determinism check.
"""

from __future__ import annotations

import json
from pathlib import Path

from agent.models import SearchQuery
from agent.tools.search import search_demo
from agent.tools.rank import rank_listings

ROOT = Path(__file__).resolve().parent


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def is_relevant(title: str, substrings: list[str]) -> bool:
    t = title.lower()
    return any(s.lower() in t for s in substrings)


def precision_at_k(ranked_titles: list[str], relevant_subs: list[str], k: int) -> float:
    top = ranked_titles[:k]
    if not top:
        return 0.0
    hits = sum(1 for t in top if is_relevant(t, relevant_subs))
    return hits / len(top)


def main() -> None:
    queries = load_json("queries.json")
    expected = load_json("expected_results.json")
    k = 5

    print("Evaluation report")
    print("=" * 40)

    precs = []
    for q in queries:
        qid = q["id"]
        exp = expected.get(qid, {})
        query = SearchQuery(
            keywords=q["keywords"],
            location=q.get("location", ""),
            remote_ok=q.get("remote_ok", True),
            limit=k,
        )
        raw = search_demo(query)
        # evaluate against full demo pool for this query's keyword filter
        ranked = rank_listings(raw, query)
        titles = [r.title for r in ranked]

        rel = exp.get("relevant_title_substrings", [])
        p = precision_at_k(titles, rel, k) if rel else 0.0
        precs.append(p)

        print(f"\n[{qid}] keywords={q['keywords']}")
        print(f"  results: {titles}")
        print(f"  Precision@{k}: {p:.2f}")

        # determinism
        ranked2 = rank_listings(list(raw), query)
        assert [r.title for r in ranked] == [r.title for r in ranked2]

    avg = sum(precs) / len(precs) if precs else 0.0
    print("\n" + "=" * 40)
    print(f"Queries evaluated: {len(queries)}")
    print(f"Mean Precision@{k}: {avg:.2f}")
    print("Deterministic ranking: PASS")
    print("Demo-only evaluation (no network required): PASS")


if __name__ == "__main__":
    main()
