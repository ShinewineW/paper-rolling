"""branch1 忠实门 (ADR-0012) — verify the 理解阅读 is FAITHFUL to its verified ARA,
not that prose carries `<!--ref-->` anchors. Two layers assembled here:
(b) mechanical number-grounding of the report against the source MD (this module),
(c) a config-routed LLM judge (report ↔ ARA), wired in a later task. The report MAY
carry numbers in natural prose; only an UNGROUNDED prose number is suspect.
"""

from __future__ import annotations

import re

from scripts.audit.ara_tree import extract_numbers, number_present, source_value_set

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


def prose_numbers(report_text: str) -> list[str]:
    """Distinct DATA numbers in report PROSE. Stripped/skipped before extraction:
    HTML-comment anchor payloads, fenced code blocks, markdown table rows (the
    paper's own figures, gated by 数字门 on the ARA), ordered-list indices, and
    provenance locators (Table 1 / 图1 / §4). The SINGLE scope used by both the
    grounding check and its ratio denominator, so they can never diverge."""
    nums: list[str] = []
    in_fence = False
    for raw in report_text.splitlines():
        if _FENCE.match(raw):
            in_fence = not in_fence
            continue
        if in_fence or raw.lstrip().startswith("|"):
            continue
        line = _OL_PREFIX.sub("", _COMMENT.sub("", raw))  # drop anchors + list index
        line = _LOCATOR.sub(" ", line)  # drop Table 1 / 图1 / §4
        for n in extract_numbers(line):
            if n not in nums:
                nums.append(n)
    return nums


def unconfirmed_report_numbers(report_text: str, source_md: str) -> list[str]:
    """Prose numbers whose VALUE is NOT present in `source_md`. Order-preserving."""
    source_values = source_value_set(source_md)
    return [n for n in prose_numbers(report_text) if not number_present(n, source_values)]
