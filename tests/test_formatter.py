from agent.models import Listing, SearchQuery
from agent.tools.format import to_markdown
from agent.tools.rank import rank_listings


def test_markdown_contains_title():
    q = SearchQuery(keywords=["ml"], limit=5)
    job = Listing(
        id="1",
        title="ML Intern",
        company="Acme",
        location="Remote",
        url="https://example.com/x",
        source="demo",
        description="Train models",
    )
    ranked = rank_listings([job], q)
    md = to_markdown(ranked, q)
    assert "ML Intern" in md
    assert "Acme" in md
    assert "https://example.com/x" in md


def test_markdown_empty_results():
    q = SearchQuery(keywords=["zzz"], limit=5)
    md = to_markdown([], q)
    assert "No matching listings" in md


def test_markdown_includes_why_when_ranked():
    q = SearchQuery(keywords=["machine learning"], limit=5)
    job = Listing(
        id="1",
        title="Machine Learning Intern",
        company="Acme",
        location="Remote",
        url="https://example.com",
        source="demo",
    )
    ranked = rank_listings([job], q)
    md = to_markdown(ranked, q, explain=True)
    assert "Why this rank" in md
