# 5. Stay public + CC-BY-NC 4.0; embed original paper figures as-is (do NOT relicense, do NOT redraw-only)

- Status: Accepted — 2026-06-09

## Context

The workspace is a **public** GitHub repo (`ShinewineW/paper-rolling`) licensed
CC-BY-NC 4.0, and the human chain already commits **original paper figures** into
`person_vault/**/images/` (92 tracked at decision time). Embedding the originals
is a deliberate, hard quality requirement: it forces the model to produce a
structure-aware, illustrated, learnable human report (the figure hard-gate in
`output/branch1_llm.py` / `output/figures.py` makes the core method/architecture
figure mandatory). Re-distributing third-party figures from a public repo is not
something CC-BY-NC grants — NC governs *our* terms to others, not our right to
redistribute *third-party* content; most sources are arXiv, whose default license
grants redistribution to arXiv, not third parties. So the originals carry a
real-but-unenforced infringement exposure, amplified by the planned product
Release (ADR-distribution work).

## Decision

**Keep the repo public, keep CC-BY-NC 4.0, keep original figures embedded as-is.**
The figure hard-gate stays unchanged. The basis is a deliberate risk judgement,
not a legal cure: this is a **personal, non-commercial, low-visibility academic
project** (verified: near-zero stars), and the illustrated-with-originals human
report is a hard product requirement. A figure-attribution clause is added to
`NOTICE` ("figures © original authors; non-commercial academic citation") as the
zero-cost good-faith mitigation.

## Considered Options

- **Go Private** — would dissolve the redistribution exposure cleanly and still
  serve cross-device use. Rejected: the owner wants the repo public/open, and the
  real driver (ship *products* to other machines without cloning the engine) is
  met by a product-only Release, not by privacy.
- **Relicense to Apache 2.0** — rejected on two grounds: (1) it does nothing for
  the figure problem (third-party content is outside our licensing power); (2) it
  is currently blocked — the repo vendors two CC-BY-NC modules (`discovery/_text.py`,
  `discovery/cache.py`), and NC (no-commercial) is incompatible with Apache-2.0
  (commercial-permissive) without first rewriting them. The owner confirmed the
  project is non-commercial and chose NOT to rewrite.
- **Redraw-only public copy** (originals local, Mermaid + "see Figure N" link in
  the public/distributed artifact) — the safe path, rejected because it defeats the
  hard "原图必须有" quality requirement for the shared copy.

## Consequences

- Public distribution Releases (the #8 product packs) **include the original
  figures** in the human-chain assets; this is an accepted, eyes-open exposure.
- A maintainer who later wants Apache/MIT must first remove the two vendored
  CC-BY-NC modules; until then the repo stays NC.
- If visibility/stakes ever rise, revisit toward the redraw-only or private option.
