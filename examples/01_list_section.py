"""List one page of the SMW hacks section."""
import pysmwcentral

page = pysmwcentral.list_section("smwhacks", page=1, order_by="date")
print(f"{page.total} hacks across {page.last_page} pages")
for hack in page:
    print(f"{hack.id:>6}  {hack.type:<10} {hack.difficulty:<12} {hack}")
