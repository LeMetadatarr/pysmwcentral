# Reverse-Engineering Notes: smwcentral.net `ajax.php`

SMW Central does not publish documentation for `ajax.php`. The endpoint powers
the site's own JavaScript UI; its actions, parameters, and response shapes were
determined by observing browser network traffic. There is no published API
contract, versioning guarantee, or terms of use specific to programmatic access.

Use this document as the sole canonical reference for the two actions this
library calls.

---

## Base URL

```
https://www.smwcentral.net/ajax.php
```

All requests are HTTP GET with query parameters. No authentication or API key is
required. The endpoint answers `application/json`.

---

## Action: `getsectionlist`

Returns a paginated listing of one section (hacks, music, graphics, etc.).

### Request

```
GET https://www.smwcentral.net/ajax.php?a=getsectionlist&s=smwhacks&n=1&o=date&d=desc&u=0
```

| Parameter | Type   | Required | Description |
|-----------|--------|----------|-------------|
| `a`       | string | yes      | Fixed: `getsectionlist` |
| `s`       | string | yes      | Section id (see below) |
| `n`       | int    | no       | Page number, 1-based (default: 1) |
| `o`       | string | no       | Order-by: `date`, `name`, `rating`, `downloads`, `size`, `featured` |
| `d`       | string | no       | Direction: `asc` or `desc` |
| `u`       | int    | no       | `1` = moderated entries only; `0` = all |

**Known section ids (`s`):**
`smwhacks`, `sm64hacks`, `yihacks`, `smwromhacks`, `smwgraphics`, `smwmusic`,
`smwblocks`, `smwsprites`, `smwpatches`, `smwuberasm`, `tools`

### Response

Top-level pagination envelope:

```json
{
  "data":         [ /* array of file objects */ ],
  "total":        1234,
  "per_page":     20,
  "current_page": 1,
  "last_page":    62,
  "from":         1,
  "to":           20
}
```

Each item in `data` is a **file object** (same shape as `getfile`, see below).

### Rate limiting

The server answers HTTP 429 when hit too fast. The library defaults to a 0.5 s
inter-request delay.

---

## Action: `getfile`

Returns the full record for a single file by its numeric id.

### Request

```
GET https://www.smwcentral.net/ajax.php?a=getfile&v=2&id=42415
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `a`       | string | yes | Fixed: `getfile` |
| `id`      | int    | yes | Numeric file id (appears in every file page URL) |
| `v`       | int    | no  | Response version; `2` returns the full record including `tags`, `images`, `download_url`, and `versions` |

An unknown `id` answers HTTP 404.

### Response (v=2)

```json
{
  "id":           42415,
  "section":      "smwhacks",
  "name":         "Hack Name",
  "authors": [
    { "id": 7, "name": "AuthorName" }
  ],
  "rating":       4.2,
  "downloads":    9800,
  "size":         131072,
  "tags":         ["Kaizo", "Pit"],
  "submitted_at": 1234567890,
  "moderated_at": 1234567900,
  "moderated":    true,
  "obsoleted_by": null,
  "download_url": "https://dl.smwcentral.net/...",
  "images":       ["https://..."],
  "fields": {
    "type":        "Kaizo",
    "difficulty":  "Advanced",
    "length":      "7 exit(s)",
    "demo":        "No",
    "description": "..."
  },
  "raw_fields": {
    "type":       "kaizo",
    "difficulty": "advanced",
    "length":     7,
    "demo":       false
  }
}
```

`fields` contains human-readable display values; `raw_fields` contains the
machine-coded equivalents. Keys vary by section: `smwhacks` carries
`type`/`difficulty`/`length`/`demo`/`description`, `sm64hacks` carries `video`,
and other sections may omit or rename keys.

---

## Stability

No versioning is published. The endpoint has been stable in observed usage, but
breaking changes are possible without notice. If `getsectionlist` returns an
empty `data` array or `getfile` returns HTTP 404 or an object with no `id`,
treat it as a miss rather than a bug.

---
[← Dataset](dataset.md) · [Home](README.md)
