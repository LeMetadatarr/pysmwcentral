"""HTTP transport for the SMW Central public JSON API.

SMW Central (`https://www.smwcentral.net`) exposes a public, key-free JSON API
through ``ajax.php``.  The ``getsectionlist`` action returns paginated section
listings (hacks, music, graphics, ...) and ``getfile`` returns a single file
record.  This module owns the shared HTTP session, polite rate limiting, and an
optional ``curl-cffi`` browser-impersonation fallback for environments where
plain ``requests`` is blocked.
"""
from __future__ import annotations

import time
from typing import Any, Dict, Optional

BASE_URL = "https://www.smwcentral.net"
API_URL = "https://www.smwcentral.net/ajax.php"

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
    ),
    "Accept": "application/json",
}

_session: Optional[Any] = None
_last_request: float = 0.0
_min_delay: float = 0.5
_force_requests: bool = False


def set_delay(seconds: float) -> None:
    """Set the minimum delay between HTTP requests (default: 0.5 s)."""
    global _min_delay
    _min_delay = max(0.0, seconds)


def use_requests(enabled: bool = True) -> None:
    """Force the plain ``requests`` backend instead of ``curl-cffi``.

    Useful for test recording, since ``vcrpy`` can only intercept ``requests``.
    Resets any existing session.
    """
    global _force_requests
    _force_requests = enabled
    reset_session()


def _make_session() -> Any:
    if _force_requests:
        import requests

        session = requests.Session()
        session.headers.update(_HEADERS)
        return session
    try:
        from unblock_requests import CloudflareSession

        session = CloudflareSession()
        session.headers.update(_HEADERS)
        return session
    except ImportError:
        pass
    try:
        import curl_cffi.requests as cffi_requests  # type: ignore
        from curl_cffi import BrowserType

        supported = {e.value for e in BrowserType}
        for candidate in ("firefox120", "firefox135", "chrome124", "chrome136"):
            if candidate in supported:
                impersonate = candidate
                break
        else:
            impersonate = next(iter(supported))
        session = cffi_requests.Session(impersonate=impersonate)
        session.headers.update(_HEADERS)
        return session
    except ImportError:
        import requests

        session = requests.Session()
        session.headers.update(_HEADERS)
        return session


def get_session() -> Any:
    global _session
    if _session is None:
        _session = _make_session()
    return _session


def reset_session() -> None:
    """Force a new HTTP session on the next request."""
    global _session
    _session = None


def _throttle() -> None:
    global _last_request
    elapsed = time.time() - _last_request
    if elapsed < _min_delay:
        time.sleep(_min_delay - elapsed)
    _last_request = time.time()


def get_json(action: str, params: Optional[Dict[str, Any]] = None) -> Any:
    """GET an ``ajax.php`` action and return the decoded JSON.

    Args:
        action: API action name, e.g. ``"getsectionlist"`` or ``"getfile"``.
        params: Query parameters (the ``a=`` action is added automatically).

    Returns:
        The decoded JSON body (``dict`` or ``list``).

    Raises:
        requests.HTTPError: on non-2xx HTTP responses.
    """
    _throttle()
    session = get_session()

    query: Dict[str, Any] = {"a": action}
    query.update(params or {})

    resp = session.get(API_URL, params=query)
    resp.raise_for_status()
    return resp.json()
