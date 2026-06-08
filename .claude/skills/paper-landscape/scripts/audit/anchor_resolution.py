"""branch1 <-> MD anchor resolution (吸收-D1, the K4 grounding fix).

The bug being fixed: branch1 (the human report) is derived from branch2, and
G3 originally only checked branch1<->branch2 — a self-referential loop. If
branch2 mis-extracted a value, branch1 inherited it and the loop "self-verified"
the error, severing the MD-only truth chain (branch1 never reads the MD).

The fix (吸收-D1): every empirical sentence in branch1 carries a three-layer
citation marker `<!--ref:slug--><!--anchor:kind:value-->` that points DIRECTLY
at an MD span, and G3 checks branch1<->MD. This module:
  1. parses ref/anchor markers (borrowing the v3.7.3 three-layer-citation
     marker shape — pure regex, zero dependency),
  2. resolves each anchor against the source MD (quote substring / page-or-
     section presence),
  3. HARD-BLOCKS (a) any anchor that does not resolve and (b) any empirical
     sentence that carries a number but no anchor at all (lint = hard gate,
     吸收-D1 option a — forces full anchoring, same disposition as G2's
     fabrication block).

Marker shape and quote-word conventions follow
`references/academic-research-skills/scripts/check_v3_7_3_three_layer_citation.py`
(borrowed pattern shape; our own net-new code, CC-BY-NC repo).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from scripts.audit.types import Finding, GateVerdict, Severity
from scripts.output.anchor_lint import unanchored_empirical_lines

_VALID_KINDS = frozenset({"quote", "page", "section", "paragraph", "none"})

# A ref marker (slug + 0-2 status tokens) immediately followed by an anchor.
_REF_ANCHOR = re.compile(
    r"<!--ref:[A-Za-z][A-Za-z0-9_:-]*(?:\s+[\w-]+){0,2}\s*-->"
    r"\s*<!--anchor:([a-z]+):([^>]*?)-->"
)

# "Which lines must be anchored" is decided by the SHARED detector in anchor_lint
# (`unanchored_empirical_lines`), so the G3 auditor and the branch1 author agree
# exactly — line-based, skips fences / ref-lines / table rows. (Previously G3 used
# its own sentence-based scan that disagreed and rejected reports branch1 passed.)


@dataclass(frozen=True)
class AnchorMarker:
    kind: str
    value: str


def iter_ref_anchor_markers(report_text: str):
    """Yield AnchorMarker for each well-formed ref+anchor pair, URL-decoded."""
    for m in _REF_ANCHOR.finditer(report_text):
        kind = m.group(1)
        value = unquote(m.group(2)) if m.group(2) else ""
        yield AnchorMarker(kind=kind, value=value)


def _normalize(text: str) -> str:
    """Collapse whitespace for forgiving substring matching across line wraps."""
    return re.sub(r"\s+", " ", text).strip()


def resolves_in_md(kind: str, value: str, md_text: str) -> bool:
    """Does an anchor of `kind`=`value` resolve to a real span in the MD?

    - quote: normalized value must be a substring of the normalized MD.
    - page/section/paragraph: the locator string must appear in the MD
      (best-effort — these are coarse locators).
    - none: always resolves (explicitly no locator).
    """
    if kind == "none":
        return True
    if kind not in _VALID_KINDS:
        return False
    needle = _normalize(value)
    if not needle:
        return False
    return needle.lower() in _normalize(md_text).lower()


def check_branch1_md_anchors(
    report_path: Path,
    md_path: Path,
    *,
    is_empirical: Callable[[str], bool] | None = None,
) -> GateVerdict:
    """Hard-block unresolvable anchors and anchorless empirical sentences.

    `is_empirical` (ROADMAP C4 / deferred B9): an OPTIONAL injected classifier
    `(sentence) -> bool` deciding which sentences are empirical-performance claims
    that MUST anchor. Defaults to the metric-cue heuristic; production may plug a
    trained NLI / factual-consistency model that generalizes beyond keyword cues.
    """
    report = report_path.read_text(encoding="utf-8")
    md_text = md_path.read_text(encoding="utf-8")
    findings: list[Finding] = []

    # 1. Every anchor must resolve to a real MD span.
    for idx, marker in enumerate(iter_ref_anchor_markers(report), start=1):
        if not resolves_in_md(marker.kind, marker.value, md_text):
            findings.append(
                Finding(
                    finding_id=f"AN{idx:02d}",
                    severity=Severity.CRITICAL,
                    target=str(report_path.name),
                    observation=(
                        f"branch1 anchor ({marker.kind}: {marker.value!r}) does "
                        f"not resolve to any span in the source MD"
                    ),
                    is_hard_block=True,
                    reasoning=(
                        "An unresolvable anchor means the human report asserts "
                        "something the source MD does not contain — narration "
                        "drift that breaks the MD-only truth chain."
                    ),
                    suggestion="Re-anchor the sentence to a real MD quote, or remove the claim.",
                )
            )

    # 2. Every empirical PERFORMANCE LINE must carry an anchor — via the SHARED
    #    line-based detector (anchor_lint.unanchored_empirical_lines). Identical to
    #    branch1's own authoring gate (skips fences / ref-lines / table rows), so a
    #    report that passes branch1 is never rejected here on a divergent scan.
    #    `is_empirical` (ROADMAP C4) still injects a custom classifier if provided.
    for fault, (lineno, prose) in enumerate(
        unanchored_empirical_lines(report, is_empirical=is_empirical), start=1
    ):
        findings.append(
            Finding(
                finding_id=f"NA{fault:02d}",
                severity=Severity.CRITICAL,
                target=str(report_path.name),
                observation=(
                    f"empirical line carries a number but has no anchor "
                    f"(吸收-D1 hard gate) [L{lineno}]: {prose[:80]!r}"
                ),
                is_hard_block=True,
                reasoning=(
                    "An un-anchored empirical statement cannot be traced to "
                    "the MD and is treated as ungrounded."
                ),
                suggestion=(
                    "Add a <!--ref:slug--><!--anchor:quote:...--> pointing at the MD span."
                ),
            )
        )
    return GateVerdict(gate="G3-anchor", findings=tuple(findings))
