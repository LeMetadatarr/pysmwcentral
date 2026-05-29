"""Data models for SMW Central JSON API objects."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# Sub-dataclasses
# ---------------------------------------------------------------------------

@dataclass
class Author:
    """A hack author or moderator (an SMW Central user reference)."""

    id: int = 0
    name: str = ""

    def __str__(self) -> str:
        return self.name or str(self.id)

    @property
    def url(self) -> str:
        if not self.id:
            return ""
        return f"https://www.smwcentral.net/?p=profile&id={self.id}"

    @property
    def as_dict(self) -> dict:
        return {"id": self.id, "name": self.name}

    @classmethod
    def from_api(cls, data: dict) -> "Author":
        from pysmwcentral._clean import clean_str, to_int

        data = data or {}
        return cls(
            id=to_int(data.get("id")),
            name=clean_str(data.get("name") or ""),
        )


# ---------------------------------------------------------------------------
# Top-level model
# ---------------------------------------------------------------------------

@dataclass
class Hack:
    """A submission record from an SMW Central section listing.

    The same shape is returned by ``getsectionlist`` (rows) and ``getfile``
    (single record).  ``fields`` carries the section-specific, human-readable
    attributes (they vary per section); the common ones are surfaced as
    properties.  ``raw_fields`` carries the machine-coded equivalents.
    """

    id: int
    section: str = ""
    name: str = ""

    authors: List[Author] = field(default_factory=list)
    rating: float = 0.0
    downloads: int = 0
    size: int = 0
    tags: List[str] = field(default_factory=list)

    submitted_at: int = 0
    moderated_at: int = 0
    moderated: bool = False
    obsoleted_by: Optional[int] = None

    download_url: str = ""
    images: List[str] = field(default_factory=list)

    fields: dict = field(default_factory=dict)
    raw_fields: dict = field(default_factory=dict)

    def __str__(self) -> str:
        return self.name or str(self.id)

    # -- section-specific fields surfaced as properties --------------------

    @property
    def url(self) -> str:
        """Canonical SMW Central file page URL."""
        return f"https://www.smwcentral.net/?p=section&a=details&id={self.id}"

    @property
    def author_names(self) -> List[str]:
        return [a.name for a in self.authors if a.name]

    @property
    def type(self) -> str:
        """Display hack type, e.g. ``Standard`` or ``Kaizo``."""
        return self.fields.get("type") or ""

    @property
    def difficulty(self) -> str:
        """Display difficulty, e.g. ``Casual`` or ``Advanced``."""
        return self.fields.get("difficulty") or ""

    @property
    def length(self) -> int:
        """Exit / star count (parsed from the display ``length`` field)."""
        from pysmwcentral._clean import parse_length

        return parse_length(
            self.raw_fields.get("length", self.fields.get("length"))
        )

    @property
    def description(self) -> str:
        return self.fields.get("description") or ""

    @property
    def demo(self) -> bool:
        return bool(self.raw_fields.get("demo")) or (
            str(self.fields.get("demo", "")).lower() == "yes"
        )

    @property
    def as_dict(self) -> dict:
        return {
            "id": self.id,
            "section": self.section,
            "name": self.name,
            "url": self.url,
            "authors": [a.as_dict for a in self.authors],
            "author_names": self.author_names,
            "rating": self.rating,
            "downloads": self.downloads,
            "size": self.size,
            "tags": self.tags,
            "type": self.type,
            "difficulty": self.difficulty,
            "length": self.length,
            "demo": self.demo,
            "description": self.description,
            "submitted_at": self.submitted_at,
            "moderated_at": self.moderated_at,
            "moderated": self.moderated,
            "obsoleted_by": self.obsoleted_by,
            "download_url": self.download_url,
            "images": self.images,
            "fields": self.fields,
            "raw_fields": self.raw_fields,
        }

    @classmethod
    def from_api(cls, data: dict) -> "Hack":
        """Build a Hack from a raw SMW Central API dict."""
        from pysmwcentral._clean import clean_str, clean_tags, to_float, to_int

        data = data or {}
        return cls(
            id=to_int(data.get("id")),
            section=clean_str(data.get("section") or ""),
            name=clean_str(data.get("name") or ""),
            authors=[Author.from_api(a) for a in (data.get("authors") or [])],
            rating=to_float(data.get("rating")),
            downloads=to_int(data.get("downloads")),
            size=to_int(data.get("size")),
            tags=clean_tags(data.get("tags") or []),
            submitted_at=to_int(data.get("submitted_at")),
            moderated_at=to_int(data.get("moderated_at")),
            moderated=bool(data.get("moderated")),
            obsoleted_by=(
                to_int(data["obsoleted_by"])
                if data.get("obsoleted_by") is not None
                else None
            ),
            download_url=data.get("download_url", "") or "",
            images=list(data.get("images") or []),
            fields=dict(data.get("fields") or {}),
            raw_fields=dict(data.get("raw_fields") or {}),
        )


@dataclass
class SectionList:
    """A page of SMW Central section results with pagination metadata."""

    hacks: List[Hack] = field(default_factory=list)
    section: str = ""
    total: int = 0
    per_page: int = 0
    current_page: int = 1
    last_page: int = 1
    from_: int = 0
    to: int = 0

    def __iter__(self):
        return iter(self.hacks)

    def __len__(self) -> int:
        return len(self.hacks)

    @property
    def has_next(self) -> bool:
        return self.current_page < self.last_page

    @property
    def as_dict(self) -> dict:
        return {
            "section": self.section,
            "total": self.total,
            "per_page": self.per_page,
            "current_page": self.current_page,
            "last_page": self.last_page,
            "from": self.from_,
            "to": self.to,
            "hacks": [h.as_dict for h in self.hacks],
        }

    @classmethod
    def from_api(cls, data: dict, section: str = "") -> "SectionList":
        from pysmwcentral._clean import to_int

        data = data or {}
        return cls(
            hacks=[Hack.from_api(h) for h in (data.get("data") or [])],
            section=section,
            total=to_int(data.get("total")),
            per_page=to_int(data.get("per_page")),
            current_page=to_int(data.get("current_page"), 1),
            last_page=to_int(data.get("last_page"), 1),
            from_=to_int(data.get("from")),
            to=to_int(data.get("to")),
        )
