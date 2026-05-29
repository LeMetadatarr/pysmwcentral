"""Client-side name/tag search over a section."""
import pysmwcentral

pysmwcentral.set_delay(1.0)

for hack in pysmwcentral.search("kaizo", section="smwhacks", max_hacks=20):
    print(f"{hack.id:>6}  {hack.difficulty:<12} {hack}  tags={hack.tags}")
