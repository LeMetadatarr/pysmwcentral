"""Data cleaning utilities for SMW Central JSON API responses."""
from __future__ import annotations

import re
import unicodedata
from typing import List, Optional


def clean_str(text: str) -> str:
    """Normalise unicode, collapse whitespace, strip."""
    if not text:
        return ""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_or_none(text: str) -> Optional[str]:
    """Like :func:`clean_str` but returns ``None`` for empty / placeholder values."""
    val = clean_str(text)
    if not val or val.lower() in ("none", "n/a", "-", "unknown"):
        return None
    return val


def clean_tags(raw) -> List[str]:
    """Clean a list of tag strings: trim, drop empties, de-duplicate (order-stable)."""
    if not raw:
        return []
    seen: set = set()
    out: List[str] = []
    for part in raw:
        tag = clean_str(part)
        if not tag:
            continue
        low = tag.lower()
        if low in seen:
            continue
        seen.add(low)
        out.append(tag)
    return out


def parse_length(value) -> int:
    """Coerce a hack ``length`` to an exit/star count.

    The display field is a string like ``"8 exit(s)"`` while ``raw_fields``
    carries a plain integer.  Both reduce to the leading number; non-numeric
    values yield ``0``.
    """
    if value is None or value == "":
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    m = re.search(r"\d+", str(value))
    return int(m.group(0)) if m else 0


def to_int(value, default: int = 0) -> int:
    """Coerce a value to int, tolerating strings and None."""
    if value is None or value == "":
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(value))
        except (TypeError, ValueError):
            return default


def to_float(value, default: float = 0.0) -> float:
    """Coerce a value to float, tolerating strings and None."""
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default
