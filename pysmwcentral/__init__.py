"""pysmwcentral — Python client for the smwcentral.net public JSON API."""
from __future__ import annotations

from pysmwcentral.version import __version__
from pysmwcentral import transport
from pysmwcentral.transport import set_delay, reset_session, get_json, use_requests
from pysmwcentral.models import Author, Hack, SectionList
from pysmwcentral.sections import (
    list_section,
    browse,
    iter_hacks,
    search,
    SECTIONS,
    ORDER_BY,
    DIRECTIONS,
)
from pysmwcentral.hack import get_hack, find_hack
from pysmwcentral.ids import hack_to_extra, id_from_url


def crawl(sections=None, *, seen=None, max_entries=0):
    if sections is None:
        sections = list(SECTIONS)
    if seen is None:
        seen = set()
    yielded = 0
    for section in sections:
        for hack in iter_hacks(section):
            if hack.id in seen:
                continue
            seen.add(hack.id)
            try:
                d = hack.as_dict()
            except Exception:
                continue
            yield d
            yielded += 1
            if max_entries and yielded >= max_entries:
                return


__all__ = [
    "__version__",
    # transport
    "set_delay",
    "reset_session",
    "get_json",
    "use_requests",
    "transport",
    # models
    "Author",
    "Hack",
    "SectionList",
    # sections
    "list_section",
    "browse",
    "iter_hacks",
    "search",
    "SECTIONS",
    "ORDER_BY",
    "DIRECTIONS",
    # hack lookup
    "get_hack",
    "find_hack",
    # ids
    "hack_to_extra",
    "id_from_url",
    # crawl
    "crawl",
]
