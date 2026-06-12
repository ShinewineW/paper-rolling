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
  3. HARD-BLOCKS any anchor that does not resolve — prose faithfulness
     (ADR-0012) is branch1_gate's job; this gate only validates anchors present.

Marker shape and quote-word conventions follow
`references/academic-research-skills/scripts/check_v3_7_3_three_layer_citation.py`
(borrowed pattern shape; our own net-new code, CC-BY-NC repo).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from scripts.audit.types import Finding, GateVerdict, Severity

_VALID_KINDS = frozenset({"quote", "page", "section", "paragraph", "none"})

# A ref marker (slug + 0-2 status tokens) immediately followed by an anchor.
_REF_ANCHOR = re.compile(
    r"<!--ref:[A-Za-z][A-Za-z0-9_:-]*(?:\s+[\w-]+){0,2}\s*-->"
    r"\s*<!--anchor:([a-z]+):([^>]*?)-->"
)


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
) -> GateVerdict:
    """Hard-block anchors that do not resolve to a real span in the source MD.

    ADR-0012: prose no longer requires <!--ref--> markers; faithfulness is
    branch1_gate's responsibility. This gate only validates that every anchor
    present in the report resolves to an actual span in the source MD.
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

    # ADR-0012: prose-anchor requirement dropped — 最终门 only RESOLVES the anchors
    # present (the engine 核心结论 block); prose faithfulness is branch1_gate's job.
    return GateVerdict(gate="G3-anchor", findings=tuple(findings))
