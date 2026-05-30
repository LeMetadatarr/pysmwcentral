---
name: pysmwcentral
description: Search SMW Central hacks and resources for accessible voice-first access on behalf of users who cannot navigate the website.
---
# pysmwcentral — SMW Central for agents

## When to use

Use this skill when a blind or voice-only user asks to find, browse, or describe Super Mario World ROM hacks, graphics, music, patches, sprites, or tools hosted on smwcentral.net. The user cannot operate the website directly; the agent acts as their proxy — searching, summarising, and speaking results aloud.

## Install

```bash
pip install pysmwcentral
```

## Core operations

### `list_section(section, page, order_by, direction, moderated) -> SectionList`

Fetch one page of any SMW Central section. Use for "show me the newest hacks" or "browse page 2 of kaizo hacks".

```python
import pysmwcentral as smw
result = smw.list_section(section="smwhacks", page=1, order_by="date", direction="desc")
for hack in result:
    print(hack.name, hack.rating, hack.type)
# result.total, result.has_next available for pagination
```

Key returned fields on each `Hack`: `id`, `name`, `authors` (list of `Author`), `rating` (float), `downloads` (int), `tags` (list), `type`, `difficulty`, `length`, `description`, `download_url`, `url` (page link).

---

### `browse(section, page, order_by, direction) -> SectionList`

Convenience alias for `list_section` — identical behaviour, cleaner call for "browse" intents.

```python
result = smw.browse(section="smwhacks", page=1, order_by="rating", direction="desc")
```

---

### `search(query, section, order_by, direction, max_hacks) -> Iterator[Hack]`

Client-side substring search across hack name and tags. Use when the user asks for hacks "about X" or "tagged Y".

```python
for hack in smw.search("kaizo", section="smwhacks", max_hacks=5):
    print(hack.name, hack.author_names, hack.rating)
```

Note: streams the full section internally; set `max_hacks` to cap results and avoid excessive fetches.

---

### `iter_hacks(section, order_by, direction, max_hacks, start_page) -> Iterator[Hack]`

Page-transparent iterator over an entire section. Use for dataset collection or "give me all featured hacks".

```python
for hack in smw.iter_hacks(section="smwhacks", order_by="rating", max_hacks=20):
    print(hack.name, hack.type)
```

---

### `get_hack(hack_id) -> Hack` / `find_hack(hack_id) -> Hack | None`

Fetch a single entry by its numeric SMW Central file id. `get_hack` raises `RuntimeError` on a miss; `find_hack` returns `None`.

```python
hack = smw.find_hack(36736)
if hack:
    print(hack.name, hack.description, hack.download_url)
```

Returned `Hack` includes full fields: `images`, `fields`, `raw_fields`, `submitted_at`, `moderated`, `obsoleted_by`.

---

## Access notes

Reverse-engineered `ajax.php` JSON endpoints — no API key or login needed. Two actions are used: `getsectionlist` (listing/search) and `getfile` (single record). There is no server-side text search; `search()` streams pages client-side. All transport goes through `unblock_requests` (CloudFlare bypass + Wayback fallback). No headed browser required.

Valid section ids: `smwhacks`, `sm64hacks`, `yihacks`, `smwromhacks`, `smwgraphics`, `smwmusic`, `smwblocks`, `smwsprites`, `smwpatches`, `smwuberasm`, `tools`.

## Speaking the results (accessibility)

- Introduce a hack as: "[name] by [author] — rated [rating]/5, type [type], [length] exits."
- Offer to read the description: "Want me to describe it? [description]"
- Offer the download: "I can give you the download link: [download_url]"
- For browse/search queries: "I found [total] hacks matching '[query]'. Here are the top results: …"
