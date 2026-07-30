# Sections

SMW Central groups submissions into **sections**. The same `getsectionlist`
action serves them all, switching on the `s=` parameter.

```python
import pysmwcentral
print(pysmwcentral.SECTIONS)
# ('smwhacks', 'sm64hacks', 'yihacks', 'smwromhacks', 'smwgraphics',
#  'smwmusic', 'smwblocks', 'smwsprites', 'smwpatches', 'smwuberasm', 'tools')
```

## List a page

```python
page = pysmwcentral.list_section(
    "smwhacks",
    page=1,
    order_by="rating",   # see ORDER_BY
    direction="desc",    # see DIRECTIONS
)
print(len(page), "of", page.total)
for hack in page:
    print(hack.id, hack.rating, hack)
```

`list_section` returns a [`SectionList`](hacks.md): an iterable of `Hack` with
pagination metadata (`total`, `per_page`, `current_page`, `last_page`,
`has_next`). `browse(...)` is an alias.

### Ordering

```python
pysmwcentral.ORDER_BY    # ('date', 'name', 'rating', 'downloads', 'size', 'featured')
pysmwcentral.DIRECTIONS  # ('asc', 'desc')
```

## Iterate a whole section

`iter_hacks` walks every page for you (see [pagination.md](pagination.md)):

```python
for hack in pysmwcentral.iter_hacks("sm64hacks", max_hacks=300):
    print(hack.id, hack)
```

## Search

The public API has **no server-side text filter**, so `search` streams the
section and filters client-side on each hack's name and tags
(case-insensitive):

```python
for hack in pysmwcentral.search("kaizo", section="smwhacks", max_hacks=25):
    print(hack)
```

For large sections, prefer ordering + `iter_hacks` and filter on the fields you
care about, since `search` may page deep before it finds matches.

---
[← Quickstart](quickstart.md) · [Home](README.md) · [Hacks →](hacks.md)
