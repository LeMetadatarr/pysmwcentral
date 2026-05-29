"""Single-hack (file) lookup for SMW Central."""
from __future__ import annotations

from typing import Optional

from pysmwcentral import transport
from pysmwcentral.models import Hack


def get_hack(hack_id: int) -> Hack:
    """Fetch a single SMW Central file by its numeric id.

    Uses the ``getfile`` action with ``v=2`` so the full record (tags, images,
    size, downloads, download_url, versions) is returned.

    Args:
        hack_id: SMW Central file id (the number in the file page URL).

    Returns:
        A :class:`~pysmwcentral.models.Hack` instance.

    Raises:
        RuntimeError: when no file matches the given id.
        requests.HTTPError: on transport errors other than a 404 miss.
    """
    import requests

    try:
        data = transport.get_json("getfile", {"v": 2, "id": int(hack_id)})
    except requests.HTTPError as exc:
        # An unknown id answers 404; surface that as a clean "not found".
        status = getattr(getattr(exc, "response", None), "status_code", None)
        if status == 404:
            raise RuntimeError(f"Hack not found: {hack_id!r}") from exc
        raise
    if not data or not isinstance(data, dict) or not data.get("id"):
        raise RuntimeError(f"Hack not found: {hack_id!r}")
    return Hack.from_api(data)


def find_hack(hack_id: int) -> Optional[Hack]:
    """Like :func:`get_hack` but returns ``None`` instead of raising on a miss."""
    try:
        return get_hack(hack_id)
    except (RuntimeError, ValueError):
        return None
