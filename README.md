# pysmwcentral

Python client for the [smwcentral.net](https://www.smwcentral.net) public JSON API.

SMW Central exposes a key-free JSON API through `ajax.php`. The `getsectionlist`
action returns paginated section listings (Super Mario World, SM64, and
Yoshi's Island hacks, music, graphics, patches, and more) and `getfile` returns
a single file record. `pysmwcentral` wraps both in typed dataclasses. It uses a
rate-limited HTTP transport and offers an optional `curl-cffi`
browser-impersonation fallback.

## Install

```bash
pip install pysmwcentral            # core (requests)
pip install pysmwcentral[stealth]   # adds curl-cffi fallback
pip install pysmwcentral[test]      # adds pytest + vcr for the test suite
```

## Quick start

```python
import pysmwcentral

# List a section page
page = pysmwcentral.list_section("smwhacks", page=1, order_by="rating")
print(page.total, "hacks across", page.last_page, "pages")
for hack in page:
    print(hack.id, hack.type, hack.difficulty, hack.rating, hack)

# Single hack by id
hack = pysmwcentral.get_hack(42415)
print(hack.name, hack.author_names, hack.length, hack.tags)

# Paginate everything in a section
for hack in pysmwcentral.iter_hacks("sm64hacks", max_hacks=200):
    print(hack.id, hack)

# Client-side name/tag search
for hack in pysmwcentral.search("kaizo", section="smwhacks", max_hacks=20):
    print(hack)

# Serialize
import json
print(json.dumps(hack.as_dict, indent=2))

# Flat external-ID dict anchored on smwcentral_id
print(pysmwcentral.hack_to_extra(hack))
```

## API surface

| Function | Purpose |
| --- | --- |
| `list_section(section, page, order_by, direction)` | One page of a section |
| `browse(section, page, order_by, direction)` | Alias of `list_section` |
| `iter_hacks(section, max_hacks)` | Iterate every entry across pages |
| `search(query, section, max_hacks)` | Client-side name/tag filter |
| `get_hack(id)` / `find_hack(id)` | Look up one file by id |
| `hack_to_extra(hack)` | Flat `smwcentral_*` external-ID dict |
| `id_from_url(url)` | Extract the file id from any smwcentral URL |
| `set_delay(seconds)` | Adjust the inter-request delay |

Sections: see `pysmwcentral.SECTIONS` (`smwhacks`, `sm64hacks`, `yihacks`, ...).

See [docs/](docs/) for details and [examples/](examples/) for runnable scripts.
The `ajax.php` endpoint is undocumented; see [docs/reverse-engineering.md](docs/reverse-engineering.md) for the observed action contracts.

## Dataset

`pysmwcentral.dataset` flattens a section into HF-publishable JSONL rows, one per
hack, anchored on `smwcentral_id`. See [docs/dataset.md](docs/dataset.md) and
[PROVENANCE.md](PROVENANCE.md).

```bash
python -m pysmwcentral.dataset hacks --section smwhacks --out hacks.jsonl --delay 1
```

## Related projects

- [pyromhacking](https://github.com/LeMetadatarr/pyromhacking) — client for romhacking.net (RHDN), the sibling ROM-hacking archive.
- [metadatarr](https://github.com/LeMetadatarr/metadatarr) — cross-source metadata clients and entity resolver that these clients feed into.
- [unblock_requests](https://github.com/LeMetadatarr/unblock_requests) — the `requests.Session` subclass this library uses for its default transport.

## License

Apache-2.0
