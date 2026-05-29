# AGENTS.md — pysmwcentral

Python client for the smwcentral.net public JSON API (`https://www.smwcentral.net/ajax.php`, no API key). Wraps the `getsectionlist` (paginated section listings) and `getfile` (single file) actions in typed dataclasses with a polite, rate-limited HTTP transport and an optional `curl-cffi` browser-impersonation fallback.

## Setup

```bash
pip install -e .
pip install -e ".[stealth]"   # adds curl-cffi transport
pip install -e ".[test]"      # adds pytest + vcr for the cassette tests
```

Pure-Python, requires Python >= 3.8. Hard runtime deps: `requests`, `unblock_requests`; `curl-cffi` is an optional stealth backend.

## Test

```bash
pytest -m "not live"          # offline, replays cassettes under tests/cassettes/
pytest -m live                # one network smoke test
```

Offline tests replay recorded `vcrpy` cassettes; no live call is made. `tests/conftest.py` forces the plain `requests` backend (`use_requests(True)`) so `vcrpy` can intercept. To re-record cassettes, delete them and run with `SMWC_TEST_DELAY=3` so recording stays under the site's HTTP 429 rate limit.

> The shared env carries a broken third-party pytest plugin; run with `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 -p pytest_vcr` if collection fails on unrelated plugins.

## Lint/Typecheck

No linter or type-checker is configured. Source uses `from __future__ import annotations` and `typing` hints throughout.

## Layout

- `pysmwcentral/__init__.py` — public API surface; re-exports transport, models, sections, hack, ids.
- `pysmwcentral/transport.py` — single shared HTTP session with throttling (`set_delay`, default 0.5s), optional `curl-cffi` impersonation, `get_json(action, params)`. `use_requests(True)` forces plain `requests`; `reset_session()` drops the cached session.
- `pysmwcentral/models.py` — `Hack`, `SectionList`, `Author` dataclasses. Each has `as_dict` and `from_api`. Section-specific attrs live in `Hack.fields` / `Hack.raw_fields`; common ones (`type`, `difficulty`, `length`, `demo`, `description`) are surfaced as properties.
- `pysmwcentral/sections.py` — `list_section`, `browse`, `iter_hacks`, `search`, plus `SECTIONS`, `ORDER_BY`, `DIRECTIONS`.
- `pysmwcentral/hack.py` — `get_hack` (raises on miss) / `find_hack` (returns `None`); uses `getfile&v=2`.
- `pysmwcentral/ids.py` — `hack_to_extra` / `id_from_url`: bridge a `Hack` into the metadatarr `ExternalIds.extra` dict, anchored on `smwcentral_id`.
- `pysmwcentral/dataset.py` — HF dataset builder; config `hacks`, `iter_rows` / `export_jsonl`, plus a `python -m pysmwcentral.dataset` CLI.
- `pysmwcentral/_clean.py` — internal string/number cleaning helpers.
- `examples/` — runnable one-call scripts; `docs/` — usage docs; `PROVENANCE.md` — source/licence.

## Conventions (org hard rules)

- Branches: work on `dev`, stable on `master`. Never use `main`. `dev` is the GitHub default branch.
- New repos are private by default, under the `TigreGotico` org.
- Never edit `pysmwcentral/version.py`; gh-automations bumps semver from conventional-commit prefixes.
- Commit identity: JarbasAi <jarbasai@mailfence.com>.
- Reference `OpenVoiceOS/gh-automations` reusable workflows at `@dev`.
- No Neon / `neon-*` references. No meta-commentary in code/docs/commits/PRs.

## Gotchas

- The public `getsectionlist` action has **no server-side text filter**; `search()` streams the section and filters client-side on name + tags.
- An unknown id makes `getfile` answer HTTP **404** (not an empty body); `get_hack` converts that one status into `RuntimeError`, and `find_hack` returns `None`.
- `fields` keys vary per section (e.g. `smwhacks` carries `type`/`difficulty`, `sm64hacks` carries `video`); only the common ones are surfaced as `Hack` properties — read `hack.fields` / `hack.raw_fields` for the rest.
- `length` is `"8 exit(s)"` in `fields` but an int in `raw_fields`; the `Hack.length` property parses either to an int.
- Throttling is process-global state in `transport.py`; `set_delay`/`reset_session`/`use_requests` mutate module globals.
