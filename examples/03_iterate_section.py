"""Iterate every hack across pages, capped, with a polite delay."""
import pysmwcentral

pysmwcentral.set_delay(1.0)

count = 0
for hack in pysmwcentral.iter_hacks("sm64hacks", max_hacks=120):
    count += 1
    print(f"{hack.id:>6}  {hack}")
print(f"\niterated {count} sm64 hacks")
