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

_VALID_KINDS = frozenset({"quote", "page", "section", "paragraph", "none"})

# A ref marker (slug + 0-2 status tokens) immediately followed by an anchor.
_REF_ANCHOR = re.compile(
    r"<!--ref:[A-Za-z][A-Za-z0-9_:-]*(?:\s+[\w-]+){0,2}\s*-->"
    r"\s*<!--anchor:([a-z]+):([^>]*?)-->"
)
# Any anchor at all (to associate sentences with their anchors).
_ANY_ANCHOR = re.compile(r"<!--anchor:[a-z]+:[^>]*?-->")
# An empirical sentence cue: contains a number (the load-bearing surface for
# the grounding requirement).
_NUMBER = re.compile(r"\d+(?:\.\d+)?")
# Sentence splitter that respects CJK and Latin terminators.
_SENTENCE_SPLIT = re.compile(r"[。！？\n]|(?<=[.!?])\s+")
# Fenced code blocks (mermaid diagrams, code stubs) — blanked before the
# anchorless-number scan so diagram/code digits never count as empirical
# assertions (mirrors branch1's own authoring gate, anchor_lint._strip_code_fences).
_FENCE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
# Empirical PERFORMANCE cue (吸收-D1 contract, mirrored from anchor_lint): a
# number alone (file paths, math exponents, the literal "branch2") is
# illustrative and does NOT require an anchor; only a number co-occurring with a
# metric/comparison cue (or a percent) is an empirical claim that MUST anchor.
_PERCENT = re.compile(r"\d+(?:\.\d+)?\s*%|\d+(?:\.\d+)?\s*个百分点")
_METRIC_CUE = re.compile(
    r"\b(NDS|mAP|AP|IoU|mIoU|BLEU|F1|AUC|ROUGE|PSNR|SSIM|FID|accuracy|acc|recall|"
    r"precision|score|top-?\d|准确率|精度|召回|提升|超过|高于|达到|outperform\w*|"
    r"improv\w*|reduc\w*|gain|百分点)\b",
    re.IGNORECASE,
)


def _is_empirical_performance(sentence: str) -> bool:
    """True iff `sentence` asserts an empirical performance number (must anchor).

    Mirrors anchor_lint's authoring-side contract so the G3 auditor and the
    branch1 author agree on which sentences require a three-layer anchor.
    """
    if _PERCENT.search(sentence):
        return True
    return bool(_NUMBER.search(sentence) and _METRIC_CUE.search(sentence))


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
    classify = is_empirical or _is_empirical_performance
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

    # 2. Every empirical PERFORMANCE sentence must carry an anchor. Code fences
    #    (mermaid diagrams) are blanked first, and bare numbers without a
    #    metric/comparison cue (math exponents, file paths, the literal
    #    "branch2") are illustrative — only performance assertions must anchor,
    #    matching branch1's own authoring gate (吸收-D1).
    scan = _FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), report)
    fault = 0
    for sentence in _SENTENCE_SPLIT.split(scan):
        s = sentence.strip()
        if not s or not classify(s):
            continue
        if not _ANY_ANCHOR.search(s):
            fault += 1
            findings.append(
                Finding(
                    finding_id=f"NA{fault:02d}",
                    severity=Severity.CRITICAL,
                    target=str(report_path.name),
                    observation=(
                        f"empirical sentence carries a number but has no anchor "
                        f"(吸收-D1 hard gate): {_normalize(s)[:80]!r}"
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
