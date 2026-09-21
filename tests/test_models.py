from agent.models import Listing, SearchQuery


def test_listing_to_dict():
    item = Listing(
        id="1",
        title="ML Intern",
        company="Acme",
        location="Remote",
        url="https://example.com",
        source="demo",
    )
    d = item.to_dict()
    assert d["title"] == "ML Intern"
    assert d["score"] == 0.0


def test_search_query_defaults():
    q = SearchQuery(keywords=["ml"])
    assert q.remote_ok is True
    assert q.limit == 20
