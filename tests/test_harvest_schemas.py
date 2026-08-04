"""Row-schema equivalence tests for the Last.fm scraper.

Relocated verbatim (assertions untouched) from metadatarr's
test_scrapers_batch4.py, keeping only the tests for the scraper that
lives in this package, re-pointed at pylastfm.harvest.*. These lock the
exact flat-row shape the scraper emits (the contract the LeData datasets
depend on) against a realistic upstream sample, so a future engine change
can't silently alter the output schema.
"""
from __future__ import annotations

from harvestkit.engine import all_sources

from pylastfm.harvest.lastfm_artists import LastfmArtistsSource, TAGS


def test_lastfm_artists_parse_artist_info_schema():
    src = LastfmArtistsSource()
    info = {
        "artist": {
            "mbid": "abc-123", "name": "Daft Punk", "url": "http://lastfm/daftpunk",
            "stats": {"listeners": "1000000", "playcount": "5000000"},
            "tags": {"tag": [{"name": "electronic"}, {"name": "house"}]},
            "bio": {"summary": "French duo. <a href=\"...\">Read more</a>"},
            "similar": {"artist": [{"name": "Justice"}]},
        }
    }
    row = src._parse_artist_info(info)
    assert row["mbid"] == "abc-123"
    assert row["listeners"] == 1000000
    assert row["tags"] == ["electronic", "house"]
    assert row["similar_artists"] == ["Justice"]
    assert row["bio_summary"] == "French duo."
    assert row["entity_type"] == "musician"
    assert set(row) == {
        "mbid", "name", "url", "listeners", "playcount", "tags",
        "similar_artists", "bio_summary", "entity_type",
    }


def test_lastfm_artists_fetch_dedups_by_name_and_advances_page():
    src = LastfmArtistsSource()
    src._api_key = "key"
    src.throttle.wait = lambda: None

    def fake_api(method, **params):
        if method == "tag.gettopartists":
            return {"topartists": {"artist": [{"name": "A"}], "@attr": {"totalPages": "1"}}}
        return {"artist": {"mbid": "m1", "name": "A", "stats": {}}}

    src._api = fake_api
    rows, cursor = src.fetch({"tag_idx": 0, "tag_page": 1})
    assert len(rows) == 1
    assert cursor == {"tag_idx": 1, "tag_page": 1}

    # already-seen name is skipped on a subsequent page
    rows2, _ = src.fetch({"tag_idx": 0, "tag_page": 1})
    assert rows2 == []


def test_lastfm_artists_fetch_no_api_key_returns_nothing():
    src = LastfmArtistsSource()
    src._api_key = ""
    rows, cursor = src.fetch({"tag_idx": 0, "tag_page": 1})
    assert rows == []
    assert cursor is None


def test_lastfm_artists_tags_registry_size():
    assert len(TAGS) > 150


def test_lastfm_artists_registered():
    assert all_sources().get("lastfm_artists") is LastfmArtistsSource
