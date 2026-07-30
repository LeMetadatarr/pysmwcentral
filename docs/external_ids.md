# External IDs

`pysmwcentral.ids` exposes helpers that convert a `Hack` into a flat
``str -> str`` dict of namespaced external IDs anchored on the canonical
**`smwcentral_id`**.  All keys are prefixed `smwcentral_`, making them
unambiguous when merged with IDs from other data sources.

## `hack_to_extra(hack)`

```python
import pysmwcentral

hack = pysmwcentral.get_hack(42415)
extra = pysmwcentral.hack_to_extra(hack)
# {
#   'smwcentral_id': '42415',                 # anchor
#   'smwcentral_url': 'https://www.smwcentral.net/?p=section&a=details&id=42415',
#   'smwcentral_section': 'smwhacks',
#   'smwcentral_name': 'Super Alex Demo',
#   'smwcentral_authors': 'Ding_Dong',
#   'smwcentral_type': 'Standard',
#   'smwcentral_difficulty': 'Casual',
#   'smwcentral_length': '7',
#   'smwcentral_rating': '4.0',
#   'smwcentral_downloads': '56',
#   'smwcentral_tags': 'custom music, pipes',
#   'smwcentral_download': 'https://dl.smwcentral.net/42415/...zip',
# }
```

All values are strings.  Optional keys are omitted when the source value is
empty, so `smwcentral_id` and `smwcentral_url` are always present and the rest
are best-effort.

## `id_from_url(url)`

Recover the canonical id from any SMW Central URL, either a file page or a
direct download link:

```python
pysmwcentral.id_from_url(
    "https://www.smwcentral.net/?p=section&a=details&id=42415"
)  # '42415'
pysmwcentral.id_from_url("https://dl.smwcentral.net/42415/Foo.zip")  # '42415'
pysmwcentral.id_from_url("https://example.com/nope")                 # None
```

`smwcentral_id` is a stable join key: enumerate with
[`iter_hacks`](pagination.md), key on `hack_to_extra(hack)["smwcentral_id"]`,
and merge against other sources using that anchor.

---
[← Pagination](pagination.md) · [Home](README.md) · [Dataset →](dataset.md)
