"""HF-publishable dataset builders for SMW Central.

One config, **hacks** — a stream of flat JSON rows, one per section entry,
anchored on the canonical ``smwcentral_id``.  Rows carry the catalog metadata
(name, authors, type, difficulty, length, rating, downloads, tags, dates) plus
the page and download URLs.  No ROM, patch, or image binary is fetched or
stored — rows hold metadata and URLs only.

Rows are emitted lazily so a caller can :func:`export_jsonl` straight to disk
without holding a whole section in memory.  See ``docs/dataset.md`` and
``PROVENANCE.md``.

Run::

    python -m pysmwcentral.dataset hacks --out hacks.jsonl --limit 100
    python -m pysmwcentral.dataset hacks --section sm64hacks --out sm64.jsonl
"""
from __future__ import annotations

import argparse
import json
from typing import Iterator, List, Optional

from pysmwcentral import sections
from pysmwcentral.ids import hack_to_extra
from pysmwcentral.models import Hack

#: HF dataset configs exposed by this module.
CONFIGS = ("hacks",)


def _hack_row(hack: Hack) -> dict:
    return {
        "smwcentral_id": hack.id,
        "section": hack.section,
        "name": hack.name,
        "authors": hack.author_names,
        "type": hack.type,
        "difficulty": hack.difficulty,
        "length": hack.length,
        "rating": hack.rating,
        "downloads": hack.downloads,
        "size": hack.size,
        "tags": hack.tags,
        "demo": hack.demo,
        "submitted_at": hack.submitted_at,
        "moderated_at": hack.moderated_at,
        "url": hack.url,
        "download_url": hack.download_url,
        "extra": hack_to_extra(hack),
    }


def iter_rows(
    config: str = "hacks",
    *,
    section: str = "smwhacks",
    limit: Optional[int] = None,
) -> Iterator[dict]:
    """Yield flat dataset rows for *config*.

    Args:
        config: which dataset config to build (only ``"hacks"``).
        section: SMW Central section id; see :data:`pysmwcentral.sections.SECTIONS`.
        limit: cap on rows emitted (handy for validation).

    Yields:
        Flat ``dict`` rows.
    """
    if config not in CONFIGS:
        raise ValueError(f"unknown config {config!r}; expected one of {CONFIGS}")
    gen = (_hack_row(h) for h in sections.iter_hacks(section=section))
    for n, row in enumerate(gen):
        if limit is not None and n >= limit:
            break
        yield row


def export_jsonl(
    config: str,
    path: str,
    *,
    section: str = "smwhacks",
    limit: Optional[int] = None,
    verbose: bool = False,
) -> int:
    """Stream *config* rows to a JSONL file. Returns the row count written."""
    written = 0
    with open(path, "w", encoding="utf-8") as fh:
        for row in iter_rows(config, section=section, limit=limit):
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")
            written += 1
            if verbose and written % 50 == 0:
                print(f"  {config}/{section}: {written} rows")
    if verbose:
        print(f"wrote {written} {config} rows -> {path}")
    return written


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Build the SMW Central HF dataset (hacks).")
    parser.add_argument("config", choices=CONFIGS, help="dataset config to export")
    parser.add_argument("--section", default="smwhacks",
                        help="SMW Central section id (default: smwhacks)")
    parser.add_argument("--out", help="output .jsonl file")
    parser.add_argument("--limit", type=int, default=None,
                        help="cap on rows (validation)")
    parser.add_argument("--delay", type=float, default=None,
                        help="seconds between HTTP requests")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)

    if args.delay is not None:
        from pysmwcentral import transport
        transport.set_delay(args.delay)

    out = args.out or f"{args.config}_{args.section}.jsonl"
    export_jsonl(
        args.config, out,
        section=args.section, limit=args.limit, verbose=not args.quiet,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
