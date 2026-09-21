from agent.models import Listing
from agent.tools.dedupe import deduplicate, dedupe_key


def _job(title, company, url, source="a", id_=None):
    return Listing(
        id=id_ or f"{source}-{title}",
        title=title,
        company=company,
        location="Remote",
        url=url,
        source=source,
    )


def test_dedupe_by_url():
    a = _job("ML Intern", "Acme", "https://example.com/job/1?ref=x", source="remotive")
    b = _job("ML Intern", "Acme", "https://example.com/job/1", source="remoteok")
    out = deduplicate([a, b])
    assert len(out) == 1
    assert out[0].source == "remotive"  # first wins


def test_dedupe_by_title_company_when_no_url():
    a = _job("ML Intern", "Acme", "", source="a")
    b = _job("ML Intern", "Acme", "", source="b")
    out = deduplicate([a, b])
    assert len(out) == 1


def test_different_companies_same_title_kept():
    a = _job("ML Intern", "Acme", "https://a.example/1")
    b = _job("ML Intern", "OtherCo", "https://b.example/2")
    out = deduplicate([a, b])
    assert len(out) == 2


def test_dedupe_preserves_order():
    jobs = [
        _job("A", "C1", "https://ex.com/a"),
        _job("B", "C2", "https://ex.com/b"),
        _job("A", "C1", "https://ex.com/a"),  # dup
    ]
    out = deduplicate(jobs)
    assert [j.title for j in out] == ["A", "B"]


def test_dedupe_key_stable():
    a = _job("ML Intern", "Acme", "https://Example.COM/Job/1/")
    b = _job("ML Intern", "Acme", "https://example.com/job/1")
    assert dedupe_key(a) == dedupe_key(b)
