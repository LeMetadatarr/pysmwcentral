"""Recover the canonical smwcentral_id from URLs, then fetch the hack."""
import pysmwcentral

urls = [
    "https://www.smwcentral.net/?p=section&a=details&id=42415",
    "https://dl.smwcentral.net/42415/Super%20Alex%20Demo.zip",
    "https://example.com/not-a-hack",
]

for url in urls:
    hid = pysmwcentral.id_from_url(url)
    print(f"{url}\n  -> smwcentral_id = {hid}")

# Round-trip: id -> hack -> extra anchor
hack = pysmwcentral.get_hack(42415)
print("\nextra anchor:", pysmwcentral.hack_to_extra(hack)["smwcentral_id"])
