# Naming & the single-writer ledger

How papers get a **stable identity** and how processed state is tracked
**crash-safely**. These two subsystems are why the engine is idempotent across
`/loop` ticks and safe to re-run.

## Vault key — the one naming authority

`scripts/output/naming.py` is the **sole** authority for a paper's vault key.
Nothing else (paths helpers, ledger, hub) may re-derive a key — they record and
reuse what `naming` produced.

- `identity_base(arxiv_id, doi) -> str` — the version-stripped identity stem.
  For an arXiv id it strips a trailing version with `re.sub(r"v\d+$", "", arxiv_id)`
  (so `2401.01234v3` and `2401.01234v1` share one identity `2401.01234`); for a
  non-arXiv paper it derives the stem from the DOI.
- `vault_key(...)` — composes the full key `{入库日期}_{Name}_{idbase}`
  (ingest-date `_` deterministic author-derived `Name` `_` `identity_base`). The
  `Name` is deterministic (no LLM ad-hoc naming), so the key is stable across
  runs and gives a **1:1 `person_vault/ ↔ ai_package/` pairing**.

Both output branches live under the same key:

| Branch | Directory | Ledger field |
|--------|-----------|--------------|
| branch1 (human report) | `person_vault/{key}/` | `person_vault_path` |
| branch2 (AI knowledge pack) | `ai_package/{key}/` | `ai_package_path` |

The pair `(person_vault_path, ai_package_path)` is `paths.VAULT_BRANCH_PATH_FIELDS`
— the canonical list both the ledger and the hub iterate to check completeness.

## The single-writer ledger

`scripts/ledger/store.py` (`class Ledger`) is the processed-state store. Its
invariants are what make unattended `/loop` runs safe:

- **Single writer (LS-1)**: the **hub** is the only writer. `Ledger.acquire()`
  takes a **non-blocking `flock`** on a persistent `_ledger/.lock`
  (`paths.LEDGER_LOCK_FILENAME`); a second concurrent instance fails fast with
  `LedgerLockError` instead of racing. The lock is held for the whole tick by
  the `run_campaign` driver — never inside `run_campaign_tick` (so the hub tests
  can call the tick directly with their own ledger).
- **Atomic append (LS-2)**: `processed_ledger.yaml`
  (`paths.LEDGER_FILENAME`, under `_ledger/`) is append-only; every write goes
  through `_atomic_write` — a temp file in the same dir + `os.replace` (atomic
  POSIX rename), so a crash mid-write never corrupts the ledger.
- **Spoke never writes the ledger**: a spoke returns the exact
  `person_vault_path` / `ai_package_path` that `produce_outputs` created; the hub
  records those **verbatim** (it never re-derives a key — see naming above).

### Startup consistency check (drift self-heal)

`Ledger.consistency_check()` runs at tick start. For every `done` paper it
confirms **both** vault branches actually exist on disk (iterating
`paths.VAULT_BRANCH_PATH_FIELDS`). A paper whose branches are not all present is
**demoted** for re-processing, and orphaned vault directories are pruned. This
reconciles ledger ↔ filesystem so a half-finished or hand-deleted paper from a
crashed prior tick self-heals instead of being falsely skipped.

## See also

- `wiring-the-seams.md` — the hub/spoke composition that drives the ledger.
- `glossary.md` — one-line definitions of *ledger*, *vault key*, *idbase*, *spoke*.
