# .claude/skills/paper-landscape/scripts/llm/seams.py
"""Production construction of the SIX LLM seams (the runtime's seam factory).

`run_campaign(...)` injects LLM-backed seams; this module builds the REAL ones on
top of the provider layer: resolve_analysis / skeptic_votes / rigor_scores /
entailment_judge / expand_llm / write_report. Each seam picks its transport via
config/llm.yaml (LLMConfig.resolve -> StrictProvider), so it is provider-routed
with NO fallback: a failing/misconfigured provider raises EngineAbort (loud) and
aborts the tick, never silently degrading to the Claude Code subscription.

Ground-truth isolation is preserved: each seam is an independent provider call, so
audit votes are uncorrelated with the generator. Use ``build_seams()`` to get the
dict the driver passes to run_campaign.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from scripts.audit.rigor_rubric import DIMENSION_KEYS
from scripts.audit.types import ClaimRecord, SkepticVote
from scripts.llm.analyzer import REQUIRED_ARA_KEYS as _REQUIRED_ARA_KEYS
from scripts.llm.analyzer import analyze_chunked
from scripts.llm.config import LLMConfig, load_llm_config
from scripts.llm.jsonparse import extract_json as _extract_json
from scripts.llm.providers import StrictProvider
from scripts.llm.writer import curate_figures, write_human_sections
from scripts.output.figures import extract_figures, is_architecture_caption

# Per-seam provider routing (config/llm.yaml; required, no default provider). Loaded once.
# Transport (claude -p / opencode / any OpenAI-compatible API) is chosen PER SEAM
# here, so the analyzer can stay on Claude while the writer/audit run on a cheaper
# backend — without the engine knowing or caring.
_LLM_CONFIG: LLMConfig | None = None


def _cfg() -> LLMConfig:
    global _LLM_CONFIG
    if _LLM_CONFIG is None:
        _LLM_CONFIG = load_llm_config(Path("."))
    return _LLM_CONFIG


# Optional per-seam provider override (A/B a seam on another backend without
# editing config/llm.yaml). Maps seam name -> a provider name defined in config.
_SEAM_OVERRIDE: dict[str, str] = {}


def _provider_for(seam: str):
    """The runtime provider for a seam, wrapped by StrictProvider: a transport
    failure raises EngineAbort (loud, aborts the tick). NO fallback — a failing
    provider is surfaced, never silently swapped for another backend."""
    cfg = _cfg()
    name = _SEAM_OVERRIDE.get(seam)
    if name:
        return StrictProvider(cfg.providers[name])
    return cfg.resolve(seam)


# A full-paper MD can be very large; cap what we feed a single seam so the nested
# agent stays well inside its context window. Cosmos tech reports are long.
# (The analyzer's own cap lives in scripts/llm/analyzer.py; this one bounds the
# skeptic/rigor inputs.)
_MD_CHAR_CAP = 200_000


def _log(msg: str) -> None:
    print(f"[seam] {msg}", file=sys.stderr, flush=True)


def _ask_json(
    prompt: str,
    *,
    seam: str,
    tier: str = "strong",
    retries: int = 2,
    timeout: float = 900.0,
    effort: str = "high",
):
    """Call the seam's ROUTED provider and parse a JSON value, retrying with a
    tightening nudge.

    Transport is chosen per seam by config/llm.yaml (claude -p / opencode / any
    OpenAI-compatible API); this layer only handles JSON extraction + a re-ask
    nudge. The provider handles its own transient/rate-limit/timeout retry.
    """
    provider = _provider_for(seam)
    last: Exception | None = None
    nudge = (
        "\n\nIMPORTANT: your reply must be ONLY a single JSON value — no prose, "
        "no explanation, no markdown code fence."
    )
    for attempt in range(retries + 1):
        raw = provider.complete(
            prompt + (nudge if attempt else ""), tier=tier, effort=effort, timeout=timeout
        )
        try:
            return _extract_json(raw)
        except (ValueError, json.JSONDecodeError) as exc:
            last = exc
            _log(f"[{seam}/{provider.name}] JSON parse retry {attempt + 1}/{retries}: {exc}")
    raise RuntimeError(
        f"seam {seam!r} failed to return parseable JSON after {retries} retries: {last}"
    )


# --------------------------------------------------------------------------- #
# Seam 1: resolve_analysis — the analyzer (ARA bundle)                          #
# --------------------------------------------------------------------------- #


def resolve_analysis(md_path: Path, candidate: dict, *, prior_failure: str | None = None) -> dict:
    """Analyzer seam: frozen paper MD -> ARA bundle, via CHUNKED PARALLEL extraction.

    Instead of one monolithic long-output call (slow + fragile — it stalled 4/4 on
    opencode), the bundle is split into 5 chunks run CONCURRENTLY (scripts/llm/
    analyzer.py), each emitting only its own keys. Routed to the `analyzer`
    provider (config/llm.yaml; explicitly routed). Cross-referenced keys (claims /
    experiments / evidence / related_work) share one chunk so C#/E# ids resolve.
    """
    provider = _provider_for("analyzer")
    mode = _cfg().mode_for("analyzer")
    if mode == "agent_team":
        raise RuntimeError(
            "analyzer mode=agent_team is not runnable by the synchronous engine; "
            "use the agent-driven runner (the runtime agent dispatches the Workflow)."
        )
    aid = candidate.get("arxiv_id", "")
    _log(f"analyzer[{provider.name}]: {aid} chunked-parallel mode={mode}")
    bundle = analyze_chunked(
        Path(md_path),
        candidate,
        provider,
        grounded=(mode == "grounded"),
        timeout=1500.0,
        log=_log,
        prior_failure=prior_failure,
    )

    missing = [k for k in _REQUIRED_ARA_KEYS if k not in bundle]
    if missing:
        raise RuntimeError(f"analyzer (chunked) missing required keys: {missing}")

    # Coerce headline numerics to float (frontmatter + landscape table need floats).
    for k in ("headline_value", "params_million"):
        try:
            bundle[k] = float(bundle[k])
        except (TypeError, ValueError):
            _log(f"analyzer: {k}={bundle.get(k)!r} not float-coercible -> 0.0")
            bundle[k] = 0.0
    bundle.pop("_comment", None)
    return bundle


# --------------------------------------------------------------------------- #
# Seam 2: skeptic_votes — G2 ground-truth-isolated number skeptic               #
# --------------------------------------------------------------------------- #


def skeptic_votes(
    numbers: tuple[str, ...], source_md: str, claim_context: str
) -> tuple[SkepticVote, ...]:
    """G2 skeptic seam: for each number, is it present/derivable in the source MD?

    Ground-truth isolation: sees ONLY the candidate numbers + source MD + a short
    context label. Fails closed — any number the model omits defaults to
    found_in_source=False.
    """
    if not numbers:
        return ()
    src = source_md if len(source_md) <= _MD_CHAR_CAP else source_md[:_MD_CHAR_CAP]
    _log(f"skeptic: {len(numbers)} numbers ({claim_context})")
    prompt = (
        "You are a SKEPTIC verifying numbers against a source document. For EACH "
        "candidate number, decide whether it appears in the SOURCE MARKDOWN below "
        "— verbatim, or as a trivial transform (a percentage of a stated fraction, "
        "a sum of stated parts, a unit restatement). Judge ONLY presence, not "
        "whether the claim is correct or important.\n\n"
        "Return a JSON array with exactly one object per candidate number, in the "
        'same order: [{"number": "<echo the exact candidate string>", '
        '"found_in_source": true|false, "note": "<<=1 line>"}].\n\n'
        f"CANDIDATE NUMBERS ({len(numbers)}): {json.dumps(list(numbers))}\n\n"
        "=== SOURCE MARKDOWN ===\n"
        f"{src}\n=== END SOURCE MARKDOWN ==="
    )
    try:
        rows = _ask_json(prompt, seam="skeptic", tier="fast", timeout=600.0, effort="medium")
    except RuntimeError as exc:
        _log(f"skeptic: seam error, failing closed: {exc}")
        return tuple(
            SkepticVote(number=n, found_in_source=False, note="seam error") for n in numbers
        )

    by_num = {}
    if isinstance(rows, list):
        for r in rows:
            if isinstance(r, dict) and "number" in r:
                by_num[str(r["number"])] = bool(r.get("found_in_source", False))
    # Fail-closed: one vote per input number; default False if the model omitted it.
    return tuple(SkepticVote(number=n, found_in_source=by_num.get(n, False)) for n in numbers)


# --------------------------------------------------------------------------- #
# Seam 3: rigor_scores — G3 6-dimension rigor reviewer (private rubric)         #
# --------------------------------------------------------------------------- #

_RIGOR_RUBRIC = """\
Score each of SIX dimensions on an integer 1-5 scale (5 best). Read the WHOLE
bundle; these are semantic checks, not keyword matching.

- D1_evidence_relevance: does cited evidence support each claim IN SUBSTANCE?
  Type-aware (causal->ablation, generalization->heterogeneous, improvement->
  baseline, descriptive->sampling, scoping->bounds). 5=type-appropriate for every
  claim; 1=most cite irrelevant experiments.
- D2_falsifiability: are falsification criteria actionable, non-trivial, scope-
  matched, independently testable? 5=specific+actionable for every claim;
  1=meaningless criteria.
- D3_scope_calibration: claims assert exactly what evidence supports; assumptions
  explicit; generalization boundaries stated. 5=precise scope+explicit limits;
  1=pervasive over/under-claiming.
- D4_argument_coherence: coherent arc observations->gaps->insight->solution->
  claims->evidence; every gap addressed. 5=clear arc, all gaps addressed;
  1=layers tell different stories.
- D5_exploration_integrity: exploration_tree faithful — concrete dead-ends, real
  decision rationale, genuine (not post-hoc) negatives. 5=rich tree+genuine
  negatives; 1=tree contradicts claims / pure post-hoc.
- D6_methodological_rigor: baseline adequacy, ablation coverage, statistical
  reporting, metric-claim alignment, reproducibility. 5=comprehensive baselines+
  ablations+rigor; 1=none.
"""


def rigor_scores(ara_bundle: dict[str, str]) -> dict:
    """G3 rigor seam: ARA text bundle -> 6-dim scores + advisory findings.

    The rubric is held privately here (never in any generator prompt). Returns
    {"dimensions": {dim: {score,strengths,weaknesses,suggestions}}, "findings":[]}.
    """
    _log(f"rigor: bundle of {len(ara_bundle)} files")
    joined = "\n\n".join(f"=== {name} ===\n{text}" for name, text in ara_bundle.items())
    if len(joined) > _MD_CHAR_CAP:
        joined = joined[:_MD_CHAR_CAP] + "\n[...TRUNCATED...]"
    keys_json = json.dumps(list(DIMENSION_KEYS))
    prompt = (
        "You are the ARA 6-dimension RIGOR REVIEWER (the terminal seal). Apply the "
        "private rubric below to the research-artifact bundle and score all six "
        "dimensions.\n\n"
        f"{_RIGOR_RUBRIC}\n"
        "Return ONE JSON object:\n"
        '{"dimensions": {' + keys_json[1:-1] + ": each -> "
        '{"score": <int 1-5>, "strengths": [str], "weaknesses": [str], '
        '"suggestions": [str]}}, "findings": [{"dimension": str, "severity": '
        '"critical|major|minor|suggestion", "observation": str}]}\n'
        f"You MUST include all six keys: {keys_json}.\n\n"
        "=== ARTIFACT BUNDLE ===\n"
        f"{joined}\n=== END BUNDLE ==="
    )
    out = _ask_json(prompt, seam="rigor", tier="strong", timeout=1500.0)
    dims = out.get("dimensions") if isinstance(out, dict) else None
    if not isinstance(dims, dict) or any(k not in dims for k in DIMENSION_KEYS):
        present = list(dims) if isinstance(dims, dict) else None
        raise RuntimeError(f"rigor: dimensions missing keys; got {present}")
    # Coerce scores to int in [1,5] so compute_grade never crashes.
    for k in DIMENSION_KEYS:
        d = dims[k]
        try:
            s = int(round(float(d["score"])))
        except (TypeError, ValueError, KeyError):
            s = 1
        d["score"] = max(1, min(5, s))
        d.setdefault("strengths", [])
        d.setdefault("weaknesses", [])
        d.setdefault("suggestions", [])
    out.setdefault("findings", [])
    return out


# --------------------------------------------------------------------------- #
# Seam 4: entailment_judge — G3 type-aware claim<->experiment entailment        #
# --------------------------------------------------------------------------- #

_REQUIRED_DESIGN = {
    "causal": "an isolating ablation",
    "generalization": "heterogeneous test conditions",
    "improvement": "a baseline comparison",
    "descriptive": "representative sampling",
    "scoping": "declared bounds",
}


def entailment_judge(claim: ClaimRecord, experiment_text: str) -> tuple[bool, str]:
    """G3 entailment seam: does the linked experiment entail the claim, given its
    type's required experiment design? Returns (entailed, reason)."""
    ctype = claim.claim_type.value
    required = _REQUIRED_DESIGN.get(ctype, "a relevant experiment")
    _log(f"entailment: {claim.claim_id} ({ctype})")
    prompt = (
        "You are a type-aware ENTAILMENT JUDGE. Decide whether the EXPERIMENT "
        "below substantively supports the CLAIM. The claim's type dictates the "
        f"experiment design it REQUIRES to be entailed: a {ctype!r} claim requires "
        f"{required}. The experiment must exhibit that design before it entails.\n\n"
        f"CLAIM ({ctype}): {claim.statement}\n\n"
        f"EXPERIMENT TEXT:\n{experiment_text}\n\n"
        'Return ONE JSON object: {"entailed": true|false, "reason": "<one line>"}.'
    )
    try:
        out = _ask_json(prompt, seam="entailment", tier="fast", timeout=300.0, effort="medium")
    except RuntimeError as exc:
        return False, f"entailment seam error: {exc}"
    if isinstance(out, dict):
        return bool(out.get("entailed", False)), str(out.get("reason", ""))
    return False, "entailment seam returned non-object"


# --------------------------------------------------------------------------- #
# Seam 5: expand_llm — discovery query expansion                               #
# --------------------------------------------------------------------------- #


def expand_llm(prompt: str) -> list[str]:
    """Query-expansion seam: prompt -> list of query strings (discovery layer)."""
    _log("query-expand")
    full = prompt + '\n\nReturn ONLY a JSON array of short query strings, e.g. ["q1","q2"].'
    try:
        out = _ask_json(full, seam="expand", tier="fast", timeout=180.0, effort="medium")
    except RuntimeError as exc:
        _log(f"query-expand error, returning empty: {exc}")
        return []
    if isinstance(out, list):
        return [str(x) for x in out if isinstance(x, (str, int, float))]
    return []


# --------------------------------------------------------------------------- #
# Seam 6: write_report — human-chain section writer (vivid Chinese prose)       #
# --------------------------------------------------------------------------- #


def write_report(
    ara_dir: Path,
    *,
    md_path: Path | None = None,
    outdir: Path | None = None,
    prior_failure: str | None = None,
) -> dict:
    """Human-chain writer seam: gated ARA (+ source MD) -> report material.

    Routed to the ``writer`` provider in config/llm.yaml (explicitly routed;
    typically a cheaper backend like deepseek/qwen). Returns:
        {"sections": {section_id: markdown},
         "figures":  [{"ref","caption","zh"}, ...]}  # ORIGINAL paper figures + 中文导览
    branch1 stitches + grounds + lint-gates the sections and embeds EVERY figure
    (the paper-guided-tour requirement). ``md_path`` enables the figure inventory.
    """
    provider = _provider_for("writer")
    _log(f"write_report: writer provider = {provider.name}")
    sections = write_human_sections(
        Path(ara_dir), provider, outdir=outdir, log=_log, prior_failure=prior_failure
    )
    figs = extract_figures(Path(md_path)) if md_path else []
    if figs:
        _log(f"write_report: curating {len(figs)} original figures (selective)")
    curated = curate_figures(figs, provider) if figs else {}
    figures: list[dict] = []
    for f in figs:
        c = curated.get(f.ref, {})
        arch = is_architecture_caption(f.caption)
        role = c.get("role") or ("architecture" if arch else "other")
        # fallback when the LLM didn't rule on this figure: include architecture figs.
        include = bool(c["include"]) if "include" in c else arch
        figures.append(
            {
                "ref": f.ref,
                "caption": f.caption,
                "role": role,
                "include": include,
                "zh": c.get("zh", ""),
            }
        )
    # MANDATORY: the core method / model-structure figure(s) must be included.
    if not any(x["include"] and x["role"] == "architecture" for x in figures):
        forced = False
        for x in figures:
            if is_architecture_caption(x["caption"]):
                x["include"], x["role"], forced = True, "architecture", True
        if not forced and figures:  # no arch-like caption — papers lead with it
            figures[0]["include"], figures[0]["role"] = True, "architecture"
    return {"sections": sections, "figures": figures}


def build_seams() -> dict:
    """The six provider-routed, fallback-wrapped LLM seams for run_campaign.

    Each value is an independent Agent-tool-equivalent callable whose transport is
    chosen per config/llm.yaml. Pass these into run_campaign(...). (write_report is
    the human-chain writer seam consumed by branch1.)
    """
    return {
        "resolve_analysis": resolve_analysis,
        "skeptic_votes": skeptic_votes,
        "rigor_scores": rigor_scores,
        "entailment_judge": entailment_judge,
        "expand_llm": expand_llm,
        "write_report": write_report,
    }
