# Quickstart

## Install

```bash
pip install pysmwcentral            # core (requests + unblock_requests)
pip install pysmwcentral[stealth]   # adds curl-cffi browser-impersonation fallback
pip install pysmwcentral[test]      # adds pytest + vcr for the test suite
```

Requires Python >= 3.8.

## First calls

```python
import pysmwcentral

# A page of the newest SMW hacks
page = pysmwcentral.list_section("smwhacks", page=1, order_by="date")
print(page.total, "hacks total,", page.last_page, "pages")
for hack in page:
    print(hack.id, hack.type, hack.difficulty, hack)

# Look up one file by its numeric id
hack = pysmwcentral.get_hack(42415)
print(hack.name, "by", ", ".join(hack.author_names))
print("type:", hack.type, "difficulty:", hack.difficulty, "exits:", hack.length)
print("rating:", hack.rating, "downloads:", hack.downloads)
print("tags:", hack.tags)
```

## Be polite

The site rate-limits the API (HTTP 429). The default delay is 0.5 s; raise it
for bulk work:

```python
pysmwcentral.set_delay(1.5)
```

## Transport backends

`pysmwcentral` prefers `unblock_requests`' `CloudflareSession`, falling back to
`curl-cffi` impersonation, then plain `requests`. Force plain `requests` (for
test recording) with `pysmwcentral.use_requests(True)`.
