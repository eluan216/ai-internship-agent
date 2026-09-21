from agent.models import Listing
from agent.cache import save_listings, load_listings
import uuid


def test_cache_roundtrip(tmp_path, monkeypatch):
    import agent.cache as cache_mod

    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path)

    items = [
        Listing(
            id="1",
            title="ML Intern",
            company="Acme",
            location="Remote",
            url="https://example.com",
            source="demo",
            score=4.0,
        )
    ]
    key = f"test-{uuid.uuid4().hex[:8]}"
    path = save_listings(key, items)
    assert path.exists()

    loaded = load_listings(key)
    assert loaded is not None
    assert len(loaded) == 1
    assert loaded[0].title == "ML Intern"
    assert loaded[0].score == 4.0


def test_cache_missing_returns_none(tmp_path, monkeypatch):
    import agent.cache as cache_mod

    monkeypatch.setattr(cache_mod, "CACHE_DIR", tmp_path)
    assert load_listings("does-not-exist-xyz") is None
