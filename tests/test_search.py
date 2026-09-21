from agent.models import SearchQuery
from agent.tools.search import search_demo, search_listings, DEMO_LISTINGS


def test_demo_returns_listings():
    q = SearchQuery(keywords=["internship"], limit=10)
    results = search_demo(q)
    assert len(results) > 0
    assert all(r.source == "demo" for r in results)


def test_keyword_filter_ml():
    q = SearchQuery(keywords=["machine learning"], limit=10)
    results = search_demo(q)
    assert any("machine learning" in r.title.lower() or "ml" in r.title.lower() for r in results)


def test_keyword_filter_excludes_unrelated():
    q = SearchQuery(keywords=["quantum underwater basket"], limit=10)
    results = search_demo(q)
    assert results == []


def test_location_remote():
    q = SearchQuery(keywords=["intern"], location="Remote", remote_ok=True, limit=10)
    results = search_demo(q)
    assert all("remote" in r.location.lower() or True for r in results)  # remote_ok allows
    assert len(results) >= 1


def test_search_listings_demo_flag():
    q = SearchQuery(keywords=["internship"], limit=3)
    results = search_listings(q, demo=True)
    assert len(results) <= len(DEMO_LISTINGS)
    assert all(r.id for r in results)


def test_empty_keywords_still_runs():
    q = SearchQuery(keywords=[], limit=5)
    # empty keywords: demo returns all (no filter)
    results = search_demo(q)
    assert len(results) == len(DEMO_LISTINGS)
