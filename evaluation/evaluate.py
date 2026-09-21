"""
Demo-fixture ranking evaluation (no network).

Reports Precision@K, determinism, and category breakdown.
Does not exercise live multi-source merge — see evaluate_multisource.py.
"""

from __future__ import annotations

import json
from pathlib import Path
from collections import defaultdict

from agent.models import SearchQuery
from agent.tools.search import search_demo
from agent.tools.rank import rank_listings
from agent.tools.dedupe import deduplicate

ROOT = Path(__file__).resolve().parent
K = 5


def load_json(name: str):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def is_relevant(title: str, substrings: list) -> bool:
    t = title.lower()
    return any(s.lower() in t for s in substrings)


def precision_at_k(titles: list, relevant_subs: list, k: int) -> float:
    top = titles[:k]
    if not top:
        return 0.0
    hits = sum(1 for t in top if is_relevant(t, relevant_subs))
    return hits / len(top)


def main() -> None:
    queries = load_json("queries.json")
    expected = load_json("expected_results.json")

    print("Evaluation report (demo fixtures)")
    print("=" * 50)

    precs = []
    by_cat = defaultdict(list)

    for q in queries:
        qid = q["id"]
        cat = q.get("category", "other")
        exp = expected.get(qid, {})
        query = SearchQuery(
            keywords=q["keywords"],
            location=q.get("location", ""),
            remote_ok=q.get("remote_ok", True),
            limit=K,
        )
        raw = search_demo(query)
        unique = deduplicate(raw)
        ranked = rank_listings(unique, query)
        titles = [r.title for r in ranked]

        rel = exp.get("relevant_title_substrings", [])
        p = precision_at_k(titles, rel, K) if rel else 0.0
        precs.append(p)
        by_cat[cat].append(p)

        print(f"[{qid}] ({cat}) P@{K}={p:.2f}  n={len(titles)}")

        ranked2 = rank_listings(deduplicate(search_demo(query)), query)
        assert [r.title for r in ranked] == [r.title for r in ranked2]

    avg = sum(precs) / len(precs) if precs else 0.0
    print("\n" + "=" * 50)
    print(f"Queries evaluated: {len(queries)}")
    print(f"Mean Precision@{K}: {avg:.2f}")
    for cat, vals in sorted(by_cat.items()):
        print(f"  {cat}: mean P@{K} = {sum(vals)/len(vals):.2f} (n={len(vals)})")
    print("Deterministic ranking: PASS")
    print("Note: demo-only; multi-source merge is evaluated separately.")


if __name__ == "__main__":
    main()
