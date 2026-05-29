"""Export a small SMW hacks dataset to JSON Lines."""
from pysmwcentral import dataset, transport

transport.set_delay(1.0)

n = dataset.export_jsonl(
    "hacks", "smwhacks.jsonl", section="smwhacks", limit=50, verbose=True
)
print(f"wrote {n} rows to smwhacks.jsonl")
