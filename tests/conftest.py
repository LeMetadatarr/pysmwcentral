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
