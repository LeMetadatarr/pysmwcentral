# Provenance

## Source

Data comes from [smwcentral.net](https://www.smwcentral.net), the community
archive for Super Mario World, Super Mario 64, and Yoshi's Island ROM hacks plus
the music, graphics, blocks, sprites, and patches that build them.

`pysmwcentral` reads the site's **public, key-free JSON API** (`ajax.php`):

- `getsectionlist` — paginated listing of a section (one row per submission).
- `getfile&v=2` — the full record for a single file id.

It reads **structured metadata only** — submission id, name, authors, type,
difficulty, length, rating, downloads, tags, dates, and the page / direct
download URLs. It does **not** download, host, or redistribute any ROM, patch,
graphics, music, or image binary. The `download_url` field is the site's own
link; following it is left to the caller and subject to the site's terms.

## Canonical id

Every record carries the canonical `smwcentral_id` (the numeric file id). It is
the anchor for the metadatarr `ExternalIds.extra` dict (`hack_to_extra`) and the
join key for derived datasets.

## Licensing

Submissions are authored by SMW Central's community and remain the property of
their respective authors; the site hosts them under its own
[terms and rules](https://www.smwcentral.net/?p=static&page=rules). Any dataset
derived with this tool carries metadata about those submissions, not the works
themselves:

- **Attribution** — credit SMW Central and the listed authors; each record keeps
  a canonical `smwcentral_id` / `url` back to the source page.
- **Non-redistribution of binaries** — this tool never fetches the hosted files;
  do not use it to mirror or rehost them.

## Polite scraping

- Default 0.5 s delay between requests (`pysmwcentral.set_delay`); bump it for
  bulk pulls — the API answers HTTP 429 when hammered.
- Browser User-Agent; HTTP/JSON only, no FlareSolverr / headed browser.
- Enumeration walks the paginated API, not a blind crawl.

Respect `robots.txt` and the site's terms. This client is intended for
legitimate metadata and dataset work, not bulk mirroring.
