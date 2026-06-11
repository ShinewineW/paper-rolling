# paper-rolling — Glossary

Domain terms specific to the paper-rolling engine. Source of truth for
terminology; implementation lives in `.claude/skills/paper-landscape/scripts/`.

## Input

The engine's candidate set comes from one of two **binary** input modes; the
operator-supplied paper set rides the same `force_include` container in both — the
only difference is whether auto-discovery also runs.

**自发查找 (auto-discovery)**:
The default input mode — the engine finds candidate papers itself by topic via the
multi-signal source pipeline (OpenAlex/S2/arXiv/DBLP/HF). Operator `force_include`
papers, if any, are added on top.

**指定列表 (paper-list run)**:
The input mode where auto-discovery is OFF and the engine processes ONLY the
operator-supplied paper set (the `force_include` container becomes the whole work
set). Binary with 自发查找 — a campaign is one or the other, never partway.
_Avoid_: "manual mode" (ambiguous), force_include-as-a-mode (force_include is the container, not the mode)

**topic (主题)**:
The subject label that scopes a campaign, **required in both input modes**. In
自发查找 it doubles as the discovery query; in BOTH modes it is the grouping key
for landscapes AND the organizing axis the products are structured under for the
**future knowledge-graph architecture**. Kept precise (the Hard Gate rejects a
vague topic) because it is a structural key feeding the KG, not just a search
string — a 指定列表 run still declares a precise topic.

## Pipeline & products

**AI知识库 (AI-Knowledge-Base)**:
The canonical, user-facing name for the AI-facing chain product — the ARA
(Agent-Native Research Artifact) knowledge pack any AI consumes for a paper's
content and inspiration. Built by branch2; lives internally in `ai_package/<key>/`
(a.k.a. the SSOT pack — the source-of-truth product the cross-paper landscape
scans). Use this name for the distribution Release asset.
_Avoid_: ai ara, ai_package (internal directory, not the product name)

**理解阅读 (Understanding-Reading)**:
The canonical, user-facing name for the human-facing chain product — the Chinese,
illustrated, structure-aware deep report a person reads to learn a paper. Built by
branch1; lives internally in `person_vault/<key>/`. Published 1:1-atomically with
its AI知识库 counterpart (both-or-neither). Use this name for the distribution
Release asset.
_Avoid_: 人链 (human chain), person_vault (internal directory, not the product name)

## Distribution

**publish**:
The explicit, owner-triggered command that packages the two chains' products
(per domain) into a GitHub Release of products only — no engine/code/corpus, so a
consumer need not clone the repo. Not bound to the `/loop` tick; runs only when
the owner says to publish.

**全量版 / 分量版 (full / delta)**:
Each chain ships two Release variants per domain: 全量版 is the complete set;
分量版 is everything new **or updated** since the previous publish.
_Avoid_: incremental-only (分量版 includes updated papers, e.g. a v2 reprocess, not just newly added ones)

## Gates

Canonical names for the four per-paper checkpoints (communication only — code
keeps `Seal-1` / `G2` / `G3`; see ADR-0008). Order: 结构门 → 数字门 → 锚点门 → 最终门.

**结构门 (structural gate)**:
After branch2. Mechanical validation that the SSOT exploration tree is
structurally valid (node types, required fields, `also_depends_on` points to a
real node). Code: `Seal-1` / `validate_ara_tree`.
_Avoid_: Seal-1 (code-only name)

**数字门 (number gate)**:
Between branch2 and branch1. LLM skeptic (N votes) verifying every evidence
number appears in the source MD — the anti-poisoning firewall. Code: `G2`.
_Avoid_: G2 (code-only name), data-fidelity gate

**锚点门 (anchor gate)**:
Inside branch1. Mechanical + classifier check that every empirical assertion in
the human report carries a `<!--ref-->` anchor. Code: three-layer anchor /
`AnchorGateError`.

**最终门 (final gate)**:
After both chains. Composite seal of four sub-checks: anchor resolution,
entailment, 6-dim rigor, equation fidelity. Code: `G3` / seal.
_Avoid_: G3 (code-only name), 封缄门, seal gate

## Failure handling

**失败现场 (quarantine scene)**:
The preserved on-disk state of a paper that failed a gate, kept under
`_failed/<key>/` instead of being deleted. Serves two purposes at once:
human debugging AND a resume point for a later 复活赛. Rationale: products are
token-expensive and the engine is still maturing, so capturing the scene is a
first-class capability — not a nice-to-have. **Local-only (gitignored):** the
scene is diagnostic scratch, NOT a product, so `_failed/` is excluded from git
(unlike the always-tracked person_vault/ + ai_package/ products). A consequence:
revival is machine-local — scenes do not travel via git. (The currently-tracked
`_failed/*.md` nutshells are a temporary cross-machine-dev exception to be
untracked, not the policy.)
_Avoid_: 纸条 (the legacy text-only `_failed/{key}.md` record — a degenerate scene)

**复活赛 (revival round)**:
A re-attempt of failed papers that replays a preserved 失败现场 — NOT an
automatic same-input rerun (every current failure is deterministic, so a blind
rerun reproduces it). Triggered explicitly after the engine/prompt/config is
fixed. See ADR-0006 for the retry mechanics.

**盲重试 (blind retry)**:
The only retry mode 数字门 (G2) gets: re-call `resolve_analysis` (a fresh analyzer
sample) and re-render — NOT just the deterministic `write_branch2` renderer (which
would reproduce the same bad numbers). Self-heals sampling-variance fabrications
without leaking the source's near-value to the generator.
_Avoid_: 反馈重试 for G2

**反馈重试 (feedback retry)**:
A re-emit that threads the gate's `Finding.observation` back into the regenerating
seam's prompt so the LLM self-corrects. Branch-level, not section-level (ADR-0009
修订): the WHOLE failed branch regenerates with an overall feedback block. Used for
content gates (最终门 anchor → branch1; rigor/entailment → branch2 analyzer),
never for 数字门. See ADR-0006/0009.
