"""Shared pytest / VCR configuration for pysmwcentral tests."""
import os

import pytest

import pysmwcentral


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "record_mode": "once",
        "match_on": ["method", "scheme", "host", "path", "query"],
        "cassette_library_dir": "tests/cassettes",
        # SMW Central serves brotli-encoded bodies (Content-Encoding: br).
        # vcrpy does not run replayed bytes back through urllib3's content
        # decoder, so without this the cassette stores the still-compressed
        # body and every replay fails JSON-decoding it, regardless of
        # whether the `brotli` package happens to be installed. Decoding at
        # record time stores plain JSON in the cassette instead.
        "decode_compressed_response": True,
    }


@pytest.fixture(autouse=True)
def _test_transport():
    """Disable throttling and force the requests backend so vcrpy can record.

    Set ``SMWC_TEST_DELAY`` (seconds) when recording fresh cassettes to stay
    polite and avoid the site's HTTP 429 rate limit; replay leaves it at 0.
    """
    pysmwcentral.set_delay(float(os.environ.get("SMWC_TEST_DELAY", "0")))
    pysmwcentral.transport.use_requests(True)
    yield
