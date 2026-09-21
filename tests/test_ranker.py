from agent.models import Listing, SearchQuery
from agent.tools.rank import rank_listings, score_listing


def _job(title, company="Co", location="Remote", desc="", tags=None):
    return Listing(
        id=title,
        title=title,
        company=company,
        location=location,
        url="https://example.com",
        source="test",
        description=desc,
        tags=tags or [],
    )


def test_relevant_scores_higher():
    q = SearchQuery(keywords=["machine learning", "internship"], limit=10)
    ml = _job("Machine Learning Intern", desc="ML models")
    front = _job("Frontend Developer", desc="React UI")
    ranked = rank_listings([front, ml], q)
    assert ranked[0].title == "Machine Learning Intern"
    assert ranked[0].score > ranked[1].score


def test_ranking_deterministic():
    q = SearchQuery(keywords=["python", "intern"], limit=10)
    jobs = [
        _job("Python Intern"),
        _job("Data Intern", desc="python"),
        _job("Marketing Intern"),
    ]
    a = rank_listings(list(jobs), q)
    b = rank_listings(list(jobs), q)
    assert [x.title for x in a] == [x.title for x in b]
    assert [x.score for x in a] == [x.score for x in b]


def test_limit_respected():
    q = SearchQuery(keywords=["intern"], limit=2)
    jobs = [_job(f"Intern {i}") for i in range(5)]
    ranked = rank_listings(jobs, q)
    assert len(ranked) == 2


def test_missing_fields_do_not_crash():
    q = SearchQuery(keywords=["ml"], limit=5)
    bare = Listing(id="x", title="", company="", location="", url="", source="t")
    ranked = rank_listings([bare], q)
    assert len(ranked) == 1


def test_explain_reasons_present():
    q = SearchQuery(keywords=["machine learning"], remote_ok=True, limit=5)
    job = _job("Machine Learning Intern", location="Remote")
    info = score_listing(job, q)
    assert info["score"] > 0
    assert any("title matches" in r for r in info["reasons"])
