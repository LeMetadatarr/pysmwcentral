"""Build a metadatarr ExternalIds.extra dict from a hack."""
import json

import pysmwcentral

hack = pysmwcentral.get_hack(42415)
extra = pysmwcentral.hack_to_extra(hack)
print(json.dumps(extra, indent=2, ensure_ascii=False))

assert extra["smwcentral_id"] == str(hack.id)  # the canonical anchor
print("\nanchor:", extra["smwcentral_id"])
