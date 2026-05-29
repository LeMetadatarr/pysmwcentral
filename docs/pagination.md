# Pagination

`getsectionlist` is paginated (50 rows per page by default). A `SectionList`
carries the page metadata:

```python
page = pysmwcentral.list_section("smwhacks", page=1)
page.total          # total submissions in the section
page.per_page       # rows per page
page.current_page   # this page (1-based)
page.last_page      # number of pages
page.from_, page.to # 1-based row span on this page
page.has_next       # current_page < last_page
```

## Manual paging

```python
page = pysmwcentral.list_section("smwhacks", page=1, order_by="downloads")
while True:
    for hack in page:
        print(hack.id, hack.downloads, hack)
    if not page.has_next:
        break
    page = pysmwcentral.list_section(
        "smwhacks", page=page.current_page + 1, order_by="downloads"
    )
```

## Automatic iteration

`iter_hacks` does the loop for you and stops at `last_page`:

```python
# Every SM64 hack, newest first
for hack in pysmwcentral.iter_hacks("sm64hacks"):
    ...

# Cap the total and resume from a page
for hack in pysmwcentral.iter_hacks(
    "smwhacks", order_by="rating", max_hacks=500, start_page=3
):
    ...
```

## Rate limiting

Bulk iteration makes one request per page. The site answers HTTP 429 when
hammered, so raise the inter-request delay for large pulls:

```python
pysmwcentral.set_delay(1.5)
```
