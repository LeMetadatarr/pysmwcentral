"""Browse the highest-rated SMW hacks."""
import pysmwcentral

page = pysmwcentral.browse(
    "smwhacks", page=1, order_by="rating", direction="desc"
)
for hack in page:
    stars = "*" * int(round(hack.rating))
    print(f"{hack.rating:>4} {stars:<5} {hack.downloads:>7} dl  {hack}")
