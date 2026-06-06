# Reference Provenance Archive

> **Scope**: `docs/reference/` — full clones of the three upstream repositories
> paper-rolling drew code and design from, kept for provenance and offline
> reference. This `index.md` is the **only** git-tracked file in this directory;
> the cloned repos are gitignored (they carry their own `.git` and are large).

---

## What this is

paper-rolling vendored / cherry-picked from three open-source research-skill
repositories. This directory holds full clones of those repos so the provenance
is **self-contained**: you can inspect exactly what was drawn from, and trace the
in-repo attribution (root `NOTICE`) back to its upstream source, without
depending on the original development workspace (`skills_workspace`).

**Decoupling note**: paper-rolling no longer depends on `skills_workspace` for
these references. They were re-cloned fresh from GitHub on **2026-06-07**.

## Git policy

- **Tracked**: only this `index.md` (the manifest).
- **Ignored**: every cloned repo under `docs/reference/` — see the root
  `.gitignore` rule:
  ```
  /docs/reference/*
  !/docs/reference/index.md
  ```
- **Rationale**: the repos are large (~152 MB total) and regenerable from the
  URLs below; they are local-only provenance inputs, not paper-rolling products.
  The manifest records the exact URL + pinned commit so the clones are
  reproducible.

## The three repositories

| Repo | Upstream | License | Cloned | Pinned HEAD (clone-time) |
|------|----------|---------|--------|--------------------------|
| `academic-research-skills` | github.com/Imbad0202/academic-research-skills | **CC-BY-NC 4.0** | 2026-06-07 | `c703c11` (committed 2026-06-06, branch `main`) |
| `AI-Research-SKILLs` | github.com/Orchestra-Research/AI-Research-SKILLs | MIT | 2026-06-07 | `28f2d29` (committed 2026-04-27, branch `main`) |
| `scientific-agent-skills` | github.com/K-Dense-AI/scientific-agent-skills | MIT (+ Apache-2.0 parts) | 2026-06-07 | `b2a969e` (committed 2026-06-04, branch `main`) |

> The pinned HEAD is the commit present at clone time and the record of what this
> archive was taken against. `git -C <repo> pull` will advance it. This is not a
> hard version pin — the material paper-rolling actually relies on is vendored
> in-repo with per-file attribution (root `NOTICE`); these clones are provenance
> context, not a build dependency.

## What paper-rolling drew from each

### `academic-research-skills` (Imbad0202) — CC-BY-NC 4.0 — **VENDORED**

The only repo paper-rolling vendors source code from. Two modules, logic
unchanged (the root `NOTICE` carries the per-file attribution + the
behavior-preserving changes, i.e. public-alias trailers and ruff autofixes):

- `scripts/_text_similarity.py` → `discovery/_text.py` (title-similarity dedup)
- `scripts/verification_cache.py` → `discovery/cache.py` (citation-lookup cache)

Design patterns also drawn (reimplemented, not copied): the claim↔evidence
adversarial audit (`scripts/claim_audit_pipeline.py`), three-layer citation
anchors, `shared/cross_model_verification.md`, and the 7-mode integrity gate
(the *Nature* "AI Scientist" failure-mode checklist). These informed the G2/G3
gates and the capability rail (ROADMAP C2 cross-model / C3 defect taxonomy /
C4 entailment).

**License caveat**: CC-BY-NC 4.0 is NonCommercial. paper-rolling is itself
research-only / CC-BY-NC 4.0 (root `LICENSE`) in large part *because* it vendors
this module — do not relicense the vendored files permissively.

### `AI-Research-SKILLs` (Orchestra-Research) — MIT — cherry-picked

- `22-agent-native-research-artifact/compiler` — the ARA (Agent-Native Research
  Artifact) schema that paper-rolling's `ai_package/` (branch2) implements:
  claims / concepts / heuristics / evidence as machine-readable structured
  knowledge. Its `references/validation-checklist.md` informed the G2
  evidence-fidelity requirements.
- `22-agent-native-research-artifact/rigor-reviewer` — the cognitive-review
  rubric behind G3's 6-dimension seal.

### `scientific-agent-skills` (K-Dense-AI) — MIT (+ Apache-2.0) — cherry-picked

- `skills/paper-lookup/references/openalex.md` — the OpenAlex / Unpaywall query
  recipes used by `discovery/openalex.py`.
- The markdown-mermaid `classDef` palette (Apache-2.0) embedded in
  `output/branch1_report.py` for the illustrated Chinese reports.

## Excluded (deliberately)

- **`auto-deep-researcher-24x7`** (github.com/Xiangyue-Zhang/auto-deep-researcher-24x7)
  — present in the old `skills_workspace/references/`, but attributed there to a
  *different* skill (`alpha-experiment`), with **zero** references in
  paper-rolling's design spec, impl spec, `NOTICE`, or source. It is not part of
  this workspace's provenance, so it is not cloned here.

## Updating

```bash
# refresh one repo to its latest upstream
git -C docs/reference/<repo> pull

# or re-clone from scratch (URLs in the table above)
rm -rf docs/reference/<repo>
git clone <url> docs/reference/<repo>
```

After updating, refresh the **Pinned HEAD** column above so the manifest stays
an accurate record of what is on disk.
