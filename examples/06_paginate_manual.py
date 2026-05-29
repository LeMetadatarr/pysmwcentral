"""Walk pages manually using SectionList pagination metadata."""
import pysmwcentral

pysmwcentral.set_delay(1.0)

page = pysmwcentral.list_section("smwhacks", page=1, order_by="downloads")
seen = 0
while True:
    print(f"-- page {page.current_page}/{page.last_page} "
          f"(rows {page.from_}-{page.to} of {page.total}) --")
    for hack in page:
        seen += 1
        print(f"  {hack.downloads:>8} dl  {hack}")
    if not page.has_next or page.current_page >= 3:  # stop after 3 pages
        break
    page = pysmwcentral.list_section(
        "smwhacks", page=page.current_page + 1, order_by="downloads"
    )
print(f"\nsaw {seen} hacks")
