"""Tests for pysmwcentral — sections, hack lookup, models, ids, dataset."""
import json

import pytest

import pysmwcentral
from pysmwcentral._clean import clean_tags, parse_length, to_float, to_int
from pysmwcentral.ids import hack_to_extra, id_from_url
from pysmwcentral.models import Author, Hack, SectionList


# ---------------------------------------------------------------------------
# Section listing
# ---------------------------------------------------------------------------

class TestSections:
    @pytest.mark.vcr()
    def test_returns_section_list(self):
        result = pysmwcentral.list_section("smwhacks", page=1)
        assert isinstance(result, SectionList)

    @pytest.mark.vcr()
    def test_has_hacks(self):
        result = pysmwcentral.list_section("smwhacks", page=1)
        assert len(result) > 0
        assert result.section == "smwhacks"

    @pytest.mark.vcr()
    def test_pagination_fields(self):
        result = pysmwcentral.list_section("smwhacks", page=1)
        assert result.total > 0
        assert result.last_page > 0
        assert result.current_page == 1
        assert result.has_next is True

    @pytest.mark.vcr()
    def test_hacks_are_dataclasses(self):
        result = pysmwcentral.list_section("smwhacks", page=1)
        for h in result:
            assert isinstance(h, Hack)
            assert h.id
            assert h.section == "smwhacks"
            assert h.url.startswith("https://")
            for a in h.authors:
                assert isinstance(a, Author)

    @pytest.mark.vcr()
    def test_iterable(self):
        result = pysmwcentral.list_section("smwhacks", page=1)
        ids = [h.id for h in result]
        assert ids


# ---------------------------------------------------------------------------
# Single-hack lookup
# ---------------------------------------------------------------------------

class TestHack:
    @pytest.mark.vcr()
    def test_get_hack(self):
        hack = pysmwcentral.get_hack(42415)
        assert isinstance(hack, Hack)
        assert hack.id == 42415
        assert hack.name

    @pytest.mark.vcr()
    def test_hack_fields(self):
        hack = pysmwcentral.get_hack(42415)
        assert hack.section == "smwhacks"
        assert hack.url.startswith("https://")
        assert isinstance(hack.fields, dict)
        assert isinstance(hack.raw_fields, dict)
        assert hack.type

    @pytest.mark.vcr()
    def test_find_missing_returns_none(self):
        assert pysmwcentral.find_hack(999999999) is None


# ---------------------------------------------------------------------------
# Models (offline, no network)
# ---------------------------------------------------------------------------

class TestModels:
    def test_hack_from_api(self):
        raw = {
            "id": 1,
            "section": "smwhacks",
            "name": "Test Hack",
            "authors": [{"id": 5, "name": "Alice"}],
            "rating": 4,
            "downloads": 120,
            "size": 4096,
            "tags": ["asm", "asm", "music"],
            "fields": {"type": "Kaizo", "difficulty": "Advanced", "length": "8 exit(s)"},
            "raw_fields": {"type": ["kaizo"], "difficulty": "diff_4", "length": 8, "demo": True},
            "download_url": "https://dl.smwcentral.net/1/foo.zip",
        }
        h = Hack.from_api(raw)
        assert h.id == 1
        assert h.author_names == ["Alice"]
        assert h.tags == ["asm", "music"]
        assert h.type == "Kaizo"
        assert h.difficulty == "Advanced"
        assert h.length == 8
        assert h.demo is True

    def test_length_from_display_string(self):
        h = Hack(id=2, fields={"length": "11 exit(s)"})
        assert h.length == 11

    def test_as_dict_roundtrip(self):
        h = Hack(
            id=3,
            section="smwhacks",
            name="X",
            authors=[Author(id=1, name="A")],
            tags=["t"],
            fields={"type": "Standard"},
        )
        d = h.as_dict
        for key in ("id", "section", "name", "url", "authors", "tags", "type", "length"):
            assert key in d
        assert d["authors"][0]["name"] == "A"

    def test_section_list_as_dict(self):
        sl = SectionList(hacks=[Hack(id=1)], total=10, last_page=3, current_page=1)
        d = sl.as_dict
        assert d["total"] == 10
        assert len(d["hacks"]) == 1
        assert sl.has_next is True


# ---------------------------------------------------------------------------
# _clean helpers
# ---------------------------------------------------------------------------

class TestClean:
    def test_clean_tags_dedup_and_trim(self):
        assert clean_tags([" asm ", "music", "asm", ""]) == ["asm", "music"]

    def test_clean_tags_empty(self):
        assert clean_tags([]) == []
        assert clean_tags(None) == []

    def test_parse_length(self):
        assert parse_length("8 exit(s)") == 8
        assert parse_length(11) == 11
        assert parse_length("") == 0
        assert parse_length(None) == 0
        assert parse_length("no exits") == 0

    def test_to_int(self):
        assert to_int("123") == 123
        assert to_int(None) == 0
        assert to_int("5.0") == 5

    def test_to_float(self):
        assert to_float("4") == 4.0
        assert to_float(None) == 0.0


# ---------------------------------------------------------------------------
# ids helpers
# ---------------------------------------------------------------------------

class TestIds:
    def test_id_from_url(self):
        assert id_from_url(
            "https://www.smwcentral.net/?p=section&a=details&id=42415"
        ) == "42415"
        assert id_from_url("https://dl.smwcentral.net/42415/Foo.zip") == "42415"
        assert id_from_url("https://example.com/nope") is None

    def test_hack_to_extra(self):
        h = Hack(
            id=42415,
            section="smwhacks",
            name="Super Alex",
            authors=[Author(id=1, name="Ding_Dong")],
            rating=4.0,
            downloads=56,
            tags=["a", "b"],
            fields={"type": "Standard", "difficulty": "Casual", "length": "7 exit(s)"},
            download_url="https://dl.smwcentral.net/42415/x.zip",
        )
        extra = hack_to_extra(h)
        assert extra["smwcentral_id"] == "42415"
        assert extra["smwcentral_section"] == "smwhacks"
        assert extra["smwcentral_authors"] == "Ding_Dong"
        assert extra["smwcentral_type"] == "Standard"
        assert extra["smwcentral_length"] == "7"
        assert extra["smwcentral_tags"] == "a, b"


# ---------------------------------------------------------------------------
# dataset
# ---------------------------------------------------------------------------

class TestDataset:
    def test_iter_rows_offline(self, monkeypatch):
        from pysmwcentral import dataset, sections

        fake = [
            Hack(id=1, section="smwhacks", name="One",
                 authors=[Author(id=1, name="A")], tags=["x"],
                 fields={"type": "Standard"}),
            Hack(id=2, section="smwhacks", name="Two", fields={"type": "Kaizo"}),
        ]
        monkeypatch.setattr(sections, "iter_hacks", lambda **kw: iter(fake))
        rows = list(dataset.iter_rows("hacks"))
        assert len(rows) == 2
        assert rows[0]["smwcentral_id"] == 1
        assert rows[0]["extra"]["smwcentral_id"] == "1"
        # rows are JSON-serialisable
        json.dumps(rows)

    def test_export_jsonl_offline(self, tmp_path, monkeypatch):
        from pysmwcentral import dataset, sections

        fake = [Hack(id=i, section="smwhacks", name=f"H{i}") for i in range(3)]
        monkeypatch.setattr(sections, "iter_hacks", lambda **kw: iter(fake))
        out = tmp_path / "hacks.jsonl"
        n = dataset.export_jsonl("hacks", str(out))
        assert n == 3
        lines = out.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 3
        assert json.loads(lines[0])["smwcentral_id"] == 0

    def test_bad_config(self):
        from pysmwcentral import dataset

        with pytest.raises(ValueError):
            list(dataset.iter_rows("nope"))


# ---------------------------------------------------------------------------
# Live smoke test (network) — run with: pytest -m live
# ---------------------------------------------------------------------------

@pytest.mark.live
class TestLive:
    def test_live_section_fetch(self):
        result = pysmwcentral.list_section("smwhacks", page=1)
        assert len(result) > 0
        first = result.hacks[0]
        assert isinstance(first, Hack)
        assert first.id
        assert first.name
