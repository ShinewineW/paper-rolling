# paper-rolling

> Autonomous AI paper-knowledge-processing engine — the `paper-landscape` v2 workspace.
> License: **CC-BY-NC 4.0** (research-only; see `LICENSE` and `NOTICE`).

`paper-rolling` is a standalone, self-contained git workspace that surveys, ingests,
analyzes, and dual-publishes deep-learning / computer-vision / autonomous-driving /
robotics research papers. It is **both an engine and a product**: the engine lives in
`.claude/skills/paper-landscape/`, and every run accumulates knowledge artifacts
(`corpus/`, `person_vault/`, `ai_package/`, `landscapes/`) directly into this repo.

## Usage

This is a project-specific engine, not a globally installable skill. Drive it from
inside the workspace:

```bash
cd ~/Coding/paper-rolling
# In Claude Code, invoke the workspace-local skill:
/paper-landscape
```

On first invocation the skill runs a one-time **campaign Hard Gate**: you must
explicitly confirm a precise **topic** and a per-round paper **count** (`top_k`).
Those are locked into `config/campaign.yaml`. After that, schedule daily incremental
runs with no further prompting:

```bash
# Run once per day; each tick ingests N new papers per the locked campaign.
/loop 1d /paper-landscape
```

The daily `/loop` tick reads the locked campaign config and runs fully autonomously
(no mid-pipeline questions). Re-running the Hard Gate is only needed to change the
topic or the per-round count.

## What gets tracked

Git tracks **products** (derived knowledge): converted `corpus/{ID}/{ID}.md`,
`person_vault/` human reports, `ai_package/` ARA knowledge packs, `_ledger/`,
`landscapes/`, the engine + `config/`. Git **ignores inputs** (regenerable):
original `*.pdf`, MinerU `images/` dumps, `content_list.json`, `.cache/`, `.env`.

## Layout

```
corpus/{ID}/      source + intermediate (md tracked; pdf/images/content_list local)
_ledger/          processed_ledger.yaml (single-writer) + .lock
person_vault/     human-facing illustrated reports, keyed {date}_{Name}_{id}
ai_package/       AI-facing ARA knowledge packs, same key (1:1 with person_vault)
landscapes/       cross-paper synthesis reports
_failed/          per-paper failure records for manual follow-up
config/           campaign.yaml (locked campaign parameters)
.claude/skills/paper-landscape/   the engine (scripts/, sub-skills/, references/)
```

## Tradeoff note (LS-6): we accept unbounded local growth

Local original PDFs + full image dumps and the git-tracked `branch1` figures grow
without bound across long-running daily campaigns. This is a **deliberate accepted
tradeoff** (LS-6): there is **no capacity cap and no auto-archival**. If disk pressure
becomes a problem, prune `corpus/**/{*.pdf,images/}` manually — they are gitignored,
regenerable inputs and removing them does not affect the tracked knowledge products.

## Development

```bash
uv sync --group dev      # set up the venv
uv run pytest            # run the test suite
uv run ruff check .      # lint
```
