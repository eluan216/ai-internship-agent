"""Regression tests for mocked multi-source pipeline."""

from agent.models import SearchQuery
from evaluation.evaluate_multisource import merge_sources, run_pipeline, MockSourceA, MockSourceB
from agent.tools.dedupe import deduplicate
from agent.tools.rank import rank_listings


def test_merge_counts():
    q = SearchQuery(keywords=["internship"], limit=10)
    raw = merge_sources(q)
    assert len(raw) == 6


def test_dedupe_removes_url_overlap():
    q = SearchQuery(keywords=["internship"], limit=10)
    raw = merge_sources(q)
    unique = deduplicate(raw)
    assert len(unique) == 5
    assert len(raw) - len(unique) == 1


def test_ml_query_ranks_ml_first():
    q = SearchQuery(keywords=["machine learning", "internship"], limit=10)
    ranked = run_pipeline(q)
    assert ranked[0].title == "Machine Learning Intern"


def test_pipeline_deterministic():
    q = SearchQuery(keywords=["machine learning", "internship"], limit=10)
    a = [r.title for r in run_pipeline(q)]
    b = [r.title for r in run_pipeline(q)]
    assert a == b


def test_both_mock_sources_present_after_dedupe():
    q = SearchQuery(keywords=["internship"], limit=10)
    unique = deduplicate(merge_sources(q))
    sources = {r.source for r in unique}
    assert "mock-a" in sources and "mock-b" in sources
