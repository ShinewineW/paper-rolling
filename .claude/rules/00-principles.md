# Rules — control plane (00-principles)

`.claude/rules/` is the machine-facing rule surface for paper-rolling: it loads
into context every session, so each line must earn its place. `.claude/CLAUDE.md`
is the project's architecture / commands / invariants DOC; this hub is the rules
index.

## Load model
- **Always-loaded** — a `rules/*.md` with NO `paths:` frontmatter loads every
  session. Reserve for every-session red-lines. Keep this set SMALL.
- **Path-scoped** — a `rules/<domain>/*.md` with `paths:` frontmatter loads only
  when Claude reads a matching file. Use for domain conventions.
- `alwaysApply:` is a Cursor field Claude Code IGNORES — never write it; absence of
  `paths:` is what makes a rule always-loaded.

## Always-loaded set (keep small)
- `00-principles.md` — this hub.
- `failure-recovery.md` — mid-run failure handling: never reset/clean state to
  "protect" it; resume via the ledger + `_failed/` scenes + `revival.py`; diagnose
  from the preserved scene, not inference.

## Path-scoped domains
- `ingest/` — heavy ingest (MinerU) offload to a borrowed remote pod (`paths:`
  scoped to the ingest + preflight source).

## Where other conventions live (do NOT duplicate here)
- **Project architecture, commands, env, non-obvious invariants** → `.claude/CLAUDE.md`.
- **`docs/` placement + naming governance** → `docs/INDEX.md` (the governing index).

## Rule-change discipline
- New every-session red-line → an always-loaded `rules/*.md` (no `paths:`); add it to
  the always-loaded list above.
- New domain convention → a path-scoped `rules/<domain>/*.md` with `paths:`.
- Keep each rule DENSE and durable — behavior/preference, not a code index (no file
  paths / symbols / config values that go stale). Every line loads every session.
