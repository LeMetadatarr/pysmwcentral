# Hacks

## The `Hack` model

A `Hack` is one submission. The listing rows and the single-file record share
the same shape, so the same dataclass covers both.

| Attribute | Type | Notes |
| --- | --- | --- |
| `id` | int | canonical SMW Central file id |
| `section` | str | e.g. `smwhacks` |
| `name` | str | submission title |
| `authors` | list[`Author`] | each has `id`, `name`, `url` |
| `rating` | float | 0–5 |
| `downloads` | int | download count |
| `size` | int | file size in bytes |
| `tags` | list[str] | de-duplicated tag list |
| `submitted_at` / `moderated_at` | int | unix timestamps |
| `moderated` | bool | |
| `obsoleted_by` | int \| None | id of a superseding file |
| `download_url` | str | site's direct download link |
| `images` | list[str] | screenshot URLs |
| `fields` | dict | section-specific display fields |
| `raw_fields` | dict | machine-coded equivalents |

### Properties

`type`, `difficulty`, `length`, `demo`, `description` are surfaced from the
per-section `fields` / `raw_fields` dicts:

```python
hack = pysmwcentral.get_hack(42415)
hack.type         # 'Standard'
hack.difficulty   # 'Casual'
hack.length       # 7   (parsed from "7 exit(s)" or the raw int)
hack.demo         # True / False
hack.author_names # ['Ding_Dong']
hack.url          # canonical file page URL
```

> `fields` keys vary by section. `smwhacks` carries `type`/`difficulty`;
> `sm64hacks` carries `video`. Read `hack.fields` / `hack.raw_fields` for
> anything not surfaced as a property.

### Serialise

```python
import json
print(json.dumps(hack.as_dict, indent=2))
```

## Single-file lookup

```python
hack = pysmwcentral.get_hack(42415)        # raises RuntimeError on a miss
maybe = pysmwcentral.find_hack(999999999)  # returns None on a miss
```

An unknown id makes the `getfile` action answer HTTP 404; `get_hack` converts
that one status into `RuntimeError`, and `find_hack` returns `None`. Other HTTP
errors propagate.
