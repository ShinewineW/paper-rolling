# tests/test_scaffold.py
"""Scaffold contract tests: pyproject deps, directory tree, LICENSE, gitignore,
campaign template. Asserts the repo skeleton other chunks build on is present
and well-formed.
"""

import tomllib

import scripts.paths as paths

ROOT = paths.repo_root()


# --- pyproject / uv ---------------------------------------------------------


def test_pyproject_declares_runtime_and_dev_deps():
    pp = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = pp["project"]
    assert project["name"] == "paper-rolling"
    assert project["license"]["text"] == "CC-BY-NC-4.0"  # Revision 2026-06-06 (was Apache-2.0)
    assert project["requires-python"] == ">=3.11"

    runtime = " ".join(project["dependencies"]).lower()
    for dep in ("requests", "pyyaml", "rapidfuzz", "lxml"):
        assert dep in runtime, f"missing runtime dep: {dep}"

    dev = pp["dependency-groups"]["dev"]
    dev_joined = " ".join(dev).lower()
    for dep in ("pytest", "ruff"):
        assert dep in dev_joined, f"missing dev dep: {dep}"


def test_pyproject_configures_ruff_and_pytest():
    pp = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    # ruff line length + target version present.
    assert pp["tool"]["ruff"]["line-length"] == 100
    # pytest testpaths points at tests/.
    assert "tests" in pp["tool"]["pytest"]["ini_options"]["testpaths"]


# --- LICENSE / README -------------------------------------------------------


def test_license_is_cc_by_nc_4_0_full_text():  # Revision 2026-06-06 (was Apache-2.0)
    text = (ROOT / "LICENSE").read_text(encoding="utf-8")
    assert "Creative Commons" in text
    assert "Attribution-NonCommercial 4.0 International" in text
    # Spot-check a clause unique to the full legalcode (not just the deed).
    assert "Section 2 -- Scope." in text


def test_readme_states_license_usage_and_growth_tradeoff():
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "CC-BY-NC" in text
    # Usage: cd into the workspace then invoke the skill.
    assert "cd ~/Coding/paper-rolling" in text
    assert "/paper-landscape" in text
    # LS-6: local PDFs/images + tracked figures grow unboundedly, accepted on purpose.
    assert "LS-6" in text
    assert "accept" in text.lower() and "growth" in text.lower()


def test_notice_attributes_vendored_ars_modules():  # Round 1 F2
    # CC-BY-NC requires attribution for the vendored academic-research-skills code.
    text = (ROOT / "NOTICE").read_text(encoding="utf-8")
    assert "academic-research-skills" in text
    assert "CC-BY-NC" in text or "Attribution-NonCommercial" in text
    # Only the two genuine verbatim drop-ins are MVP-vendored (Round 6 scope fix).
    for mod in ("_text_similarity", "verification_cache"):
        assert mod in text
    # NET-NEW + DEFERRED modules must NOT be attributed as vendored (Round 8).
    for forbidden in (
        "crosscheck",
        "contamination_signals",
        "check_v3_7_3",
        "uncited_assertion_detector",
        "_claim_audit_constants",
        "claim_audit_pipeline",
    ):
        assert forbidden not in text


# --- directory tree ---------------------------------------------------------


def test_required_directories_exist():
    for d in (
        "corpus",
        "_ledger",
        "person_vault",
        "ai_package",
        "landscapes",
        "_failed",
        "config",
        ".claude/skills/paper-landscape/scripts",
        ".claude/skills/paper-landscape/sub-skills",
        ".claude/skills/paper-landscape/references",
        "tests",
    ):
        assert (ROOT / d).is_dir(), f"missing dir: {d}"


def test_empty_dirs_have_gitkeep_so_they_survive_clone():
    for d in ("corpus", "_ledger", "person_vault", "ai_package", "landscapes", "_failed"):
        assert (ROOT / d / ".gitkeep").is_file(), f"missing .gitkeep in {d}"


# --- .gitignore -------------------------------------------------------------


def test_gitignore_tracks_products_and_ignores_inputs():
    gi = (ROOT / ".gitignore").read_text(encoding="utf-8")
    # Inputs ignored (regenerable):
    for pat in (
        "corpus/**/*.pdf",
        "corpus/**/images/",
        "corpus/**/content_list.json",
        ".cache/",
        ".env",
        ".venv/",
    ):
        assert pat in gi, f"expected ignore pattern: {pat}"
    # Products NOT blanket-ignored: there is no bare line that ignores all of
    # person_vault/ or ai_package/ or _ledger/ or landscapes/ or config/.
    lines = {ln.strip() for ln in gi.splitlines()}
    for product in ("person_vault/", "ai_package/", "_ledger/", "landscapes/", "config/", "*.md"):
        assert product not in lines, f"product must not be ignored: {product}"


# --- campaign.yaml + .env.example ------------------------------------------


def test_campaign_yaml_template_has_all_locked_fields():
    import yaml

    # The repo ships a TEMPLATE (.example), not a live config — a fresh clone has
    # no live config/campaign.yaml so the Hard Gate fires (load_campaign -> None).
    cfg = yaml.safe_load((ROOT / "config" / "campaign.yaml.example").read_text(encoding="utf-8"))
    # Hard-Gate-confirmed fields the runtime CampaignConfig actually reads
    # (中枢-D1 / 吸收-D4): topic, n_per_tick, is_ad_domain — must match campaign.py.
    assert "topic" in cfg
    assert isinstance(cfg["n_per_tick"], int) and cfg["n_per_tick"] > 0
    assert isinstance(cfg["is_ad_domain"], bool)
    # 中枢-D5a: preprint policy default is strict.
    assert cfg["preprint_policy"] == "strict"
    # D-发现-2: polite-pool email present (canonical value from the spec).
    assert cfg["openalex_mailto"] == "ahhssxlcwjz@163.com"
    # D-发现-3: top-tier venue allowlist seeded.
    venues = cfg["venue_allowlist"]
    for v in ("NeurIPS", "ICML", "ICLR", "CVPR", "ICCV", "ECCV", "ICRA", "CoRL", "RSS"):
        assert v in venues, f"venue missing: {v}"
    # D-发现-5: institution whitelist seeded.
    insts = cfg["institution_whitelist"]
    for inst in ("Google", "Meta", "NVIDIA", "Waymo"):
        assert any(inst in name for name in insts), f"institution missing: {inst}"


def test_env_example_documents_hf_token_from_env():
    text = (ROOT / ".env.example").read_text(encoding="utf-8")
    assert "HF_TOKEN" in text
    # .env.example documents the read-only HF_TOKEN read from .env (D-发现-4).
    assert "read-only" in text.lower()


# --- SKILL.md skeleton ------------------------------------------------------

SKILL_PATH = ROOT / ".claude" / "skills" / "paper-landscape" / "SKILL.md"


def test_skill_md_has_frontmatter_name_and_description():
    text = SKILL_PATH.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    fm_end = text.index("\n---", 3)
    fm = text[4:fm_end]
    assert "name: paper-landscape" in fm
    assert "description:" in fm


def test_skill_md_documents_campaign_gate_and_loop():
    text = SKILL_PATH.read_text(encoding="utf-8")
    # 中枢-D1 / 吸收-D4: one-time campaign Hard Gate confirming topic + count.
    assert "Hard Gate" in text
    assert "campaign" in text.lower()
    assert "config/campaign.yaml" in text
    # 吸收-D3: daily /loop autonomous cadence, no re-gate.
    assert "/loop" in text
    # 中枢-D2: no mid-pipeline questions after the gate.
    assert "AskUserQuestion" in text
    # MUST discipline is explicit.
    assert "MUST" in text
