# Failure Recovery & Workspace State [MUST]

The paper-rolling engine is built to SURVIVE mid-run failures: an append-only
ledger, per-paper failure scenes under `_failed/`, and a batch revival driver
(`scripts/revival.py`). When a `/loop` tick or rerun fails partway, these ARE the
recovery surface — do not discard them.

## Never reset state to "protect" it [MUST]
- **Do NOT `git checkout HEAD` / restore products / reset the ledger to "protect"
  committed output when a run fails or is interrupted.** HEAD is already safe;
  resetting to it instead erases in-progress progress, orphans the `_failed/` scenes
  from the ledger, and forces re-burning tokens to redo completed work.
- **Do NOT clean or delete products/artifacts before the work is finished.** Cleanup
  is the final step, never a reflex at the first sign of trouble.
- On a mid-run failure: LEAVE the ledger (`deferred`/`failed` rows) and `_failed/`
  scenes intact, then RESUME in place via revival / the next tick (skips `done`,
  retries `deferred`). Resume — do not restart from scratch.

## Diagnose from the preserved scene, not inference [MUST]
- Before concluding WHY a paper failed, READ its scene first: `_failed/<key>.md`
  carries the authoritative `failure_class` + `failure_reason`. Do not infer the
  cause from indirect log signals.
- Pitfall (2026-06-12): a stall (`failure_class: stalled`, wall-clock budget exceeded)
  was misread as a "codex quality failure" from skeptic-log inference — wrong
  diagnosis, wasted a whole night. The scene had the real reason all along.
