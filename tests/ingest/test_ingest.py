import json

import pytest
from conftest import write_mineru_output
from scripts.ingest.contract import sha256_bytes
from scripts.ingest.ingest import IngestFailed, ingest, quarantine

FIXED_NOW = "2026-06-05T12:00:00+00:00"


def _now():
    return FIXED_NOW


def test_ingest_tier1_success_writes_md_and_contract(tmp_path, fake_http, fake_cli, candidate):
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    html = b'<html><body><p><math><mi>x</mi></math></p><img src="f.png"/></body></html>'
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, html)
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}/f.png", 200, b"\x89PNG")

    def pandoc(argv, cwd):
        from pathlib import Path

        out = argv[argv.index("-o") + 1]
        Path(cwd, out).write_text("Body $$x = y$$\n\n![](images/f.png)\n")

    fake_cli.program(returncode=0, side_effect=pandoc)

    res = ingest(candidate, tmp_path, http=fake_http, run_cli=fake_cli, now=_now)

    assert res.tier == 1
    assert res.md_path.exists()
    assert res.md_path.name == "1706.03762v5_AttentionIsAllYouNeed.md"
    contract = json.loads((res.md_path.parent / ".md_contract.json").read_text())
    assert contract["converter"] == "pandoc"
    assert contract["source_pdf_sha256"] is None  # Tier-1 never downloads PDF
    assert contract["equation_block_count"] == 1
    assert contract["image_count"] == 1


def test_ingest_demotes_to_tier2_when_html_missing(tmp_path, fake_http, fake_cli, candidate):
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 404, b"")
    fake_http.add(candidate["oa_pdf_url"], 200, b"%PDF body")

    def mineru(argv, cwd):
        from pathlib import Path

        out = argv[argv.index("-o") + 1]
        write_mineru_output(
            Path(cwd, out),
            md="# T\n$$a$$\n$$b$$\n",
            images=["x.png"],
            content_list='[{"type":"equation"}]',
        )

    fake_cli.program(returncode=0, side_effect=mineru)

    res = ingest(candidate, tmp_path, http=fake_http, run_cli=fake_cli, now=_now)

    assert res.tier == 2
    contract = json.loads((res.md_path.parent / ".md_contract.json").read_text())
    assert contract["converter"] == "mineru"
    assert contract["source_pdf_sha256"] == sha256_bytes(b"%PDF body")
    assert contract["equation_block_count"] == 2
    assert contract["image_count"] == 1


def test_ingest_equation_gate_demotes_when_math_dropped(tmp_path, fake_http, fake_cli, candidate):
    """HTML had math but pandoc produced 0 $$ blocks -> equation-count gate demotes."""
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    html = b"<html><body><p><math><mi>z</mi></math> text</p></body></html>"
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, html)
    fake_http.add(candidate["oa_pdf_url"], 200, b"%PDF body")

    calls = {"pandoc": 0}

    def runner(argv, cwd):
        from pathlib import Path

        from conftest import FakeCliResult

        if argv[0] == "pandoc":
            calls["pandoc"] += 1
            out = argv[argv.index("-o") + 1]
            Path(cwd, out).write_text("Body with no display math at all.\n")
            return FakeCliResult(returncode=0)
        # mineru
        out = argv[argv.index("-o") + 1]
        write_mineru_output(Path(cwd, out), md="$$z = 1$$\n", images=[], content_list="[]")
        return FakeCliResult(returncode=0)

    res = ingest(candidate, tmp_path, http=fake_http, run_cli=runner, now=_now)

    assert calls["pandoc"] == 1  # Tier-1 ran
    assert res.tier == 2  # but demoted because math was dropped
    contract = json.loads((res.md_path.parent / ".md_contract.json").read_text())
    assert contract["equation_block_count"] == 1


def test_ingest_both_tiers_fail_raises_ingestfailed(tmp_path, fake_http, fake_cli, candidate):
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 404, b"")
    # pdf_url not registered -> 404 -> Tier2Failed
    with pytest.raises(IngestFailed) as ei:
        ingest(candidate, tmp_path, http=fake_http, run_cli=fake_cli, now=_now)
    assert "1706.03762" in str(ei.value)


def test_quarantine_writes_failure_record(tmp_path, candidate):
    quarantine(
        candidate,
        tmp_path,
        reason="both tiers failed: html_missing; pdf_download 404",
        attempted_tiers=[1, 2],
        now=_now,
    )
    rec_path = tmp_path / "_failed" / "1706.03762v5_AttentionIsAllYouNeed.json"
    rec = json.loads(rec_path.read_text())
    assert rec["arxiv_id"] == "1706.03762"
    assert rec["title"] == "Attention Is All You Need"
    assert rec["source_url"] == candidate["oa_pdf_url"]
    assert rec["attempted_tiers"] == [1, 2]
    assert rec["failed_at"] == FIXED_NOW
    assert "html_missing" in rec["reason"]
