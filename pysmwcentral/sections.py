"""Section listing, browsing, and search for SMW Central."""
from __future__ import annotations

from typing import Iterator, Optional

from pysmwcentral import transport
from pysmwcentral.models import Hack, SectionList

#: Section identifiers accepted by ``getsectionlist`` (the ``s=`` parameter).
SECTIONS = (
    "smwhacks",
    "sm64hacks",
    "yihacks",
    "smwromhacks",
    "smwgraphics",
    "smwmusic",
    "smwblocks",
    "smwsprites",
    "smwpatches",
    "smwuberasm",
    "tools",
)

#: Valid ``o`` (order-by) values for :func:`list_section`.
ORDER_BY = ("date", "name", "rating", "downloads", "size", "featured")

#: Valid ``d`` (direction) values.
DIRECTIONS = ("asc", "desc")


def list_section(
    section: str = "smwhacks",
    page: int = 1,
    order_by: str = "date",
    direction: str = "desc",
    moderated: int = 0,
) -> SectionList:
    """List one page of an SMW Central section.

    Args:
        section: Section id; see :data:`SECTIONS`.
        page: Page number (1-based).
        order_by: Sort key; see :data:`ORDER_BY`.
        direction: ``asc`` or ``desc``; see :data:`DIRECTIONS`.
        moderated: Restrict to moderated entries (``1``) or include all (``0``).

    Returns:
        A :class:`~pysmwcentral.models.SectionList`.
    """
    params = {
        "s": section,
        "n": page,
        "o": order_by,
        "d": direction,
        "u": moderated,
    }
    data = transport.get_json("getsectionlist", params)
    return SectionList.from_api(data, section=section)


def browse(
    section: str = "smwhacks",
    page: int = 1,
    order_by: str = "date",
    direction: str = "desc",
) -> SectionList:
    """Alias for :func:`list_section` reading the newest entries by default."""
    return list_section(
        section=section, page=page, order_by=order_by, direction=direction
    )


def iter_hacks(
    section: str = "smwhacks",
    order_by: str = "date",
    direction: str = "desc",
    max_hacks: int = 0,
    start_page: int = 1,
) -> Iterator[Hack]:
    """Iterate over every entry in a section across pages.

    Args:
        section: Section id; see :data:`SECTIONS`.
        order_by: Sort key; see :data:`ORDER_BY`.
        direction: ``asc`` or ``desc``.
        max_hacks: Stop after yielding this many entries (``0`` = no limit).
        start_page: Page to begin from (1-based), for resuming.

    Yields:
        :class:`~pysmwcentral.models.Hack` instances.
    """
    page = start_page
    yielded = 0
    while True:
        result = list_section(
            section=section, page=page, order_by=order_by, direction=direction
        )
        if not result.hacks:
            break
        for hack in result.hacks:
            yield hack
            yielded += 1
            if max_hacks and yielded >= max_hacks:
                return
        if not result.has_next:
            break
        page += 1


def search(
    query: str,
    section: str = "smwhacks",
    order_by: str = "date",
    direction: str = "desc",
    max_hacks: int = 0,
) -> Iterator[Hack]:
    """Client-side name/tag search over a section.

    The public ``getsectionlist`` action has no server-side text filter, so
    this streams the section (see :func:`iter_hacks`) and yields entries whose
    name or tags contain *query* (case-insensitive).

    Args:
        query: Substring to match against hack name and tags.
        section: Section id; see :data:`SECTIONS`.
        order_by: Sort key; see :data:`ORDER_BY`.
        direction: ``asc`` or ``desc``.
        max_hacks: Stop after yielding this many matches (``0`` = no limit).

    Yields:
        Matching :class:`~pysmwcentral.models.Hack` instances.
    """
    needle = (query or "").strip().lower()
    yielded = 0
    for hack in iter_hacks(section=section, order_by=order_by, direction=direction):
        haystack = " ".join([hack.name, *hack.tags]).lower()
        if needle in haystack:
            yield hack
            yielded += 1
            if max_hacks and yielded >= max_hacks:
                return
