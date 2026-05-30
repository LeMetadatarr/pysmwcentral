# Hugging Face dataset

`pysmwcentral.dataset` flattens an SMW Central section into tabular rows, one
Hugging Face dataset **config** per build. Each config is a streaming row
flattener over [`iter_hacks`](sections.md) — it never materialises a whole
section in memory.

> ## Provenance & licence (read this first)
>
> Rows carry **metadata only** — no ROM, patch, graphics, music, or image
> binary is fetched or stored; `download_url` is the site's own link. Submissions
> belong to their authors and SMW Central's terms apply. See
> [../PROVENANCE.md](../PROVENANCE.md). Credit SMW Central and the listed authors
> in any dataset card, and keep the `smwcentral_id` / `url` anchor in every row.

## Configs

| config | source | join key | notable columns |
| --- | --- | --- | --- |
| `hacks` | `getsectionlist` (any section) | `smwcentral_id` | name, authors, type, difficulty, length, rating, downloads, tags, dates |

Every row carries `smwcentral_id` as a stable join key for cross-referencing.
Pick the section with `section=` (`smwhacks`, `sm64hacks`, `yihacks`, ...).

## Streaming rows

```python
from pysmwcentral import dataset

for row in dataset.iter_rows("hacks", section="smwhacks", limit=100):
    print(row["smwcentral_id"], row["name"], row["type"])
```

Each row is a flat, JSON-serialisable dict:

```json
{
  "smwcentral_id": 42415,
  "section": "smwhacks",
  "name": "Super Alex Demo",
  "authors": ["Ding_Dong"],
  "type": "Standard",
  "difficulty": "Casual",
  "length": 7,
  "rating": 0.0,
  "downloads": 56,
  "size": 251138,
  "tags": [],
  "demo": true,
  "submitted_at": 1779632214,
  "moderated_at": 1779976938,
  "url": "https://www.smwcentral.net/?p=section&a=details&id=42415",
  "download_url": "https://dl.smwcentral.net/42415/Super%20Alex%20Demo.zip",
  "extra": {"smwcentral_id": "42415", "smwcentral_url": "...", "..."}
}
```

## Export to JSON Lines

```python
from pysmwcentral import dataset

dataset.export_jsonl("hacks", "hacks.jsonl", section="smwhacks", limit=1000)
```

Or from the command line:

```bash
python -m pysmwcentral.dataset hacks --section smwhacks --out hacks.jsonl --delay 1
python -m pysmwcentral.dataset hacks --section sm64hacks --limit 200 --delay 1
```

`--delay` raises the inter-request delay so a full-section pull stays under the
site's HTTP 429 rate limit.

## Building a `datasets.Dataset`

```python
from datasets import Dataset
from pysmwcentral import dataset

rows = list(dataset.iter_rows("hacks", section="smwhacks", limit=5000))
ds = Dataset.from_list(rows)
ds.push_to_hub("your-org/smwcentral-hacks", config_name="hacks")  # carry the licence in the card
```
