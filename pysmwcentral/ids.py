"""metadatarr integration helpers for SMW Central objects.

These functions convert :class:`~pysmwcentral.models.Hack` instances into flat
``extra`` dicts compatible with the ``ExternalIds.extra`` field used across the
metadatarr pipeline.  Keys are namespaced with ``smwcentral_`` and anchored on
the canonical ``smwcentral_id``.
"""
from __future__ import annotations

import re
from typing import Optional

from pysmwcentral.models import Hack


def id_from_url(url: str) -> Optional[str]:
    """Extract an SMW Central file id from any smwcentral.net URL.

    Handles the ``?p=section&a=details&id=<id>`` file-page form and the
    ``dl.smwcentral.net/<id>/...`` download form.

    Args:
        url: Any SMW Central URL.

    Returns:
        The numeric id as a string, or ``None`` if the URL has none.
    """
    if not url:
        return None
    m = re.search(r"[?&]id=(\d+)", url)
    if m:
        return m.group(1)
    m = re.search(r"dl\.smwcentral\.net/(\d+)/", url)
    return m.group(1) if m else None


def hack_to_extra(hack: Hack) -> dict:
    """Convert a :class:`~pysmwcentral.models.Hack` to a metadatarr extra dict.

    Keys written:

    - ``smwcentral_id`` — canonical SMW Central file id (anchor)
    - ``smwcentral_url`` — canonical file page URL
    - ``smwcentral_section`` — section id (e.g. ``smwhacks``)
    - ``smwcentral_name`` — hack title
    - ``smwcentral_authors`` — comma-joined author names
    - ``smwcentral_type`` — hack type
    - ``smwcentral_difficulty`` — difficulty
    - ``smwcentral_length`` — exit / star count (str)
    - ``smwcentral_rating`` — rating (str)
    - ``smwcentral_downloads`` — download count (str)
    - ``smwcentral_tags`` — comma-joined tags
    - ``smwcentral_download`` — direct download URL
    """
    extra: dict = {
        "smwcentral_id": str(hack.id),
        "smwcentral_url": hack.url,
    }
    if hack.section:
        extra["smwcentral_section"] = hack.section
    if hack.name:
        extra["smwcentral_name"] = hack.name
    if hack.author_names:
        extra["smwcentral_authors"] = ", ".join(hack.author_names)
    if hack.type:
        extra["smwcentral_type"] = hack.type
    if hack.difficulty:
        extra["smwcentral_difficulty"] = hack.difficulty
    if hack.length:
        extra["smwcentral_length"] = str(hack.length)
    if hack.rating:
        extra["smwcentral_rating"] = str(hack.rating)
    if hack.downloads:
        extra["smwcentral_downloads"] = str(hack.downloads)
    if hack.tags:
        extra["smwcentral_tags"] = ", ".join(hack.tags)
    if hack.download_url:
        extra["smwcentral_download"] = hack.download_url
    return extra
