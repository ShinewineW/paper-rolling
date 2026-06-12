"""branch1 忠实门 (ADR-0012) — verify the 理解阅读 is FAITHFUL to its verified ARA,
not that prose carries `<!--ref-->` anchors. Two layers assembled here:
(b) mechanical number-grounding of the report against the source MD (this module),
(c) a config-routed LLM judge (report ↔ ARA), assembled in check_report_faithfulness.
The report MAY carry numbers in natural prose; only an UNGROUNDED prose number is suspect.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from pathlib import Path

from scripts.audit.ara_tree import extract_numbers, number_present, source_value_set
from scripts.audit.types import Finding, Severity
from scripts.output.anchor_lint import lint_text

_FENCE = re.compile(r"^\s*```")
# Strip HTML comments BEFORE number extraction. The engine 核心结论 block carries
# anchors like `<!--ref:quote:Table%201%20reports%2028.4-->`; without stripping,
# extract_numbers parses the URL-encoded payload into bogus tokens ('201', '20',
# '2028.4') that would be flagged as ungrounded prose numbers.
_COMMENT = re.compile(r"<!--.*?-->", re.DOTALL)
# Markdown ordered-list index ("1. ", "2. ") — the LLM assembler emits numbered
# 核心结论 lines; the index is structure, not a data number.
_OL_PREFIX = re.compile(r"^\s*\d+\.\s")
# Provenance LOCATORS (English Table 1 / §4 / Eq 3 AND Chinese 图1 / 表1 / 第4节 /
# 公式1) — references, not metric values; strip so a faithful report is never blocked
# on a locator digit absent from the source MD (mirrors g2_data_fidelity._LOCATOR).
_LOCATOR = re.compile(
    r"(?i)(?:\b(?:tables?|tab|sections?|sec|figures?|fig|equations?|eq|appendix|app)\.?\s*|§\s*)\d+"
    r"|(?:图|表|公式|附录|第)\s*\d+"
)
# Markdown link targets `](...)` — strip the URL/path payload so vault-key paths
# like `../../ai_package/2026-06-05.../ara/evidence/` and arXiv IDs in hrefs are
# not parsed as ungrounded data numbers (they are infrastructure references, not
# scientific claims).
_MD_LINK_TARGET = re.compile(r"\]\([^)]*\)")
# Inline code spans `...` — the assembler/writer wraps vault-key paths, file
# names, and code refs in backticks (e.g. `ai_package/2026-06-12_..._2503.19755/`);
# those are infrastructure references, not prose data. Strip them like fenced code
# and link targets (ADR-0012 demo, ORION: a backticked vault path leaked 2026/2503).
_INLINE_CODE = re.compile(r"`[^`]*`")
# Bibliographic IDENTIFIERS — an arXiv id (`2503.19755`, YYMM.NNNNN) or a DOI
# (`10.1234/...`). These are paper-identity metadata, never scientific data, so a
# report that names the paper's own arXiv id in prose must not be number-grounded
# on it (ADR-0012 demo, ORION: the writer echoed `arXiv:2503.19755` → a bogus
# ungrounded "number"). A real metric with 4 integer + 4–5 decimal digits does not
# occur, so this shape is unambiguous.
_IDENTIFIER = re.compile(r"(?<!\d)\d{4}\.\d{4,5}(?!\d)|10\.\d{4,9}/\S+")


def prose_numbers(report_text: str) -> list[str]:
    """Distinct DATA numbers in report PROSE. Stripped/skipped before extraction:
    HTML-comment anchor payloads, fenced code blocks, markdown table rows (the
    paper's own figures, gated by 数字门 on the ARA), ordered-list indices,
    inline `code` spans, markdown link targets (vault-key paths / hrefs),
    bibliographic identifiers (arXiv id / DOI), and provenance locators
    (Table 1 / 图1 / §4). The SINGLE
    scope used by both the grounding check and its ratio denominator, so they can
    never diverge."""
    nums: list[str] = []
    in_fence = False
    for raw in report_text.splitlines():
        if _FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence or raw.lstrip().startswith("|"):
            continue
        line = _OL_PREFIX.sub("", _COMMENT.sub("", raw))  # drop anchors + list index
        line = _INLINE_CODE.sub(" ", line)  # drop inline `code` (vault paths, file/code refs)
        line = _MD_LINK_TARGET.sub(" ", line)  # drop link targets (vault-key paths, hrefs)
        line = _IDENTIFIER.sub(" ", line)  # drop arXiv id / DOI (paper-identity metadata)
        line = _LOCATOR.sub(" ", line)  # drop Table 1 / 图1 / §4
        for n in extract_numbers(line):
            if n not in nums:
                nums.append(n)
    return nums


def unconfirmed_report_numbers(report_text: str, source_md: str) -> list[str]:
    """Prose numbers whose VALUE is NOT present in `source_md`. Order-preserving."""
    source_values = source_value_set(source_md)
    return [n for n in prose_numbers(report_text) if not number_present(n, source_values)]


def check_report_faithfulness(
    report_text: str,
    source_md: str,
    ara_dir: Path,
    *,
    judge: Callable[[str, Path], dict] | None = None,
    tolerant: bool = False,
    max_unconfirmed: int = 5,
    max_unconfirmed_ratio: float = 0.2,
) -> list[Finding]:
    """The branch1 忠实门 (ADR-0012): kept anchor-form lint + (b) tolerant number
    grounding + (c) optional LLM judge. Returns the HARD-BLOCK findings (empty =
    pass). `judge` is the (c) seam; None (deterministic fallback path) skips it."""
    findings: list[Finding] = []

    # Kept anchor-form checks (well-formed engine 核心结论 block anchors).
    for v in lint_text(report_text):
        findings.append(
            Finding(
                finding_id=f"AF{len(findings) + 1:02d}",
                severity=Severity.CRITICAL,
                target="report.md",
                observation=v.message,
                is_hard_block=True,
                reasoning="A malformed/orphan <!--ref--> anchor breaks the core-block truth chain.",
                suggestion="Fix or remove the malformed anchor.",
            )
        )

    # (b) tolerant mechanical grounding of prose numbers. Numerator AND denominator
    # share prose_numbers() — same stripped/skipped scope.
    bad = unconfirmed_report_numbers(report_text, source_md)
    total = len(prose_numbers(report_text)) or 1
    # STRICT (tolerant=False, the gate primitive's default) hard-blocks ANY
    # unconfirmed number. TOLERANT (the producers' default — the 理解阅读 is a LOOSE
    # human-facing derivative per ADR-0012, NOT the strict ARA) softens within the
    # LARGER of two limits: the absolute ceiling `max_unconfirmed` is a FLOOR that
    # protects small reports (a 3-number report must not be quarantined over one
    # ungrounded value — the exact false-quarantine ADR-0012 removes), and the ratio
    # `max_unconfirmed_ratio * total` only TIGHTENS for large reports (it binds once
    # total > max_unconfirmed / max_unconfirmed_ratio, e.g. > 25). This deliberately
    # does NOT mirror 数字门's strict AND-of-both-limits — the report is looser by design.
    within_tolerance = tolerant and len(bad) <= max(max_unconfirmed, max_unconfirmed_ratio * total)
    grounding_hard = bool(bad) and not within_tolerance
    for n in bad:
        findings.append(
            Finding(
                finding_id=f"AF{len(findings) + 1:02d}",
                severity=Severity.CRITICAL if grounding_hard else Severity.MAJOR,
                target="report.md",
                observation=f"prose number {n!r} not grounded in the source MD"
                + ("" if grounding_hard else " [TOLERATED]"),
                is_hard_block=grounding_hard,
                reasoning="A report number absent from the source MD is narration drift.",
                suggestion="Re-state the number from the ARA, or cut the claim.",
            )
        )

    # (c) semantic faithfulness judge (LLM path only).
    if judge is not None:
        verdict = judge(report_text, ara_dir)
        if not verdict.get("faithful", False):
            for jf in verdict.get("findings", []) or [
                {"claim": "", "issue": "report materially misleads vs ARA"}
            ]:
                findings.append(
                    Finding(
                        finding_id=f"AF{len(findings) + 1:02d}",
                        severity=Severity.CRITICAL,
                        target="report.md",
                        observation=(
                            f"materially misleading vs ARA: {jf.get('claim', '')}"
                            f" — {jf.get('issue', '')}"
                        ),
                        is_hard_block=True,
                        reasoning=(
                            "The human report misrepresents the verified ARA"
                            " (misattribution/overclaim)."
                        ),
                        suggestion="Correct the claim to match the ARA.",
                    )
                )

    return [f for f in findings if f.is_hard_block]
