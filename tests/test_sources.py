from agent.models import SearchQuery, Listing
from agent.sources.base import JobSource
from agent.sources.demo import DemoSource
from agent.sources.remotive import RemotiveSource
from agent.sources.remoteok import RemoteOKSource


def test_demo_source_is_job_source():
    src = DemoSource()
    assert isinstance(src, JobSource)
    assert src.name == "demo"


def test_remotive_and_remoteok_declare_name():
    assert RemotiveSource().name == "remotive"
    assert RemoteOKSource().name == "remoteok"


def test_demo_source_returns_listings():
    q = SearchQuery(keywords=["internship"], limit=5)
    results = DemoSource().search(q)
    assert len(results) > 0
    assert all(isinstance(r, Listing) for r in results)
    assert all(r.source == "demo" for r in results)


def test_demo_source_keyword_filter():
    q = SearchQuery(keywords=["quantum underwater basket"], limit=5)
    assert DemoSource().search(q) == []
