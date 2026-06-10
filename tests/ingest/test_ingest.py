import json

import pytest
from conftest import write_mineru_output
from scripts.ingest.contract import sha256_bytes
from scripts.ingest.ingest import IngestFailed, _paper_id, ingest, quarantine


def test_paper_id_doi_only_candidate_is_not_none(tmp_path):
    """Codex R21: a non-arXiv (DOI-only) candidate must NOT build a `None_...`
    corpus id — it gets a stable doi-hash identity."""
    doi_only = {"arxiv_id": None, "doi": "10.1109/CVPR.2022.01164", "title": "Venue Paper"}
    pid = _paper_id(doi_only)
    assert not pid.startswith("None")
    assert pid.startswith("doi-")
    assert pid.endswith("_VenuePaper")
    # arXiv candidates keep the version-aware id.
    arxiv = {"arxiv_id": "2403.12345", "arxiv_version": "v2", "doi": None, "title": "ArxivPaper"}
    assert _paper_id(arxiv) == "2403.12345v2_ArxivPaper"


def test_ingest_derives_arxiv_pdf_url_when_oa_pdf_url_missing(
    tmp_path, fake_http, fake_cli, candidate
):
    """Codex R21: an HF-discovered arXiv candidate may carry oa_pdf_url=None; when
    Tier-1 is unavailable, Tier-2 must DERIVE the arXiv PDF URL rather than fail."""
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    candidate = {**candidate, "oa_pdf_url": None}  # HF-style: no OA pdf url
    derived = f"https://arxiv.org/pdf/{aid}{ver}"
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 404, b"")  # Tier-1 unavailable
    fake_http.add(derived, 200, b"%PDF body")  # derived arXiv PDF URL

    def mineru(argv, cwd):
        from pathlib import Path

        out = argv[argv.index("-o") + 1]
        write_mineru_output(
            Path(cwd, out),
            md="# T\n$$a$$\n",
            images=["x.png"],
            content_list='[{"type":"equation"}]',
        )

    fake_cli.program(returncode=0, side_effect=mineru)

    res = ingest(candidate, tmp_path, http=fake_http, run_cli=fake_cli, now=_now)

    assert res.tier == 2
    assert derived in fake_http.requested  # the derived arXiv PDF URL was fetched


FIXED_NOW = "2026-06-05T12:00:00+00:00"


def _now():
    return FIXED_NOW


def _write_ready_corpus(tmp_path, candidate, *, md, converter="mineru", with_content_list=True):
    """Pre-populate a committed, ready corpus entry (MD + consistent contract)."""
    from scripts.ingest.contract import MdContract, write_contract

    pid = _paper_id(candidate)
    paper_dir = tmp_path / "corpus" / pid
    paper_dir.mkdir(parents=True)
    (paper_dir / f"{pid}.md").write_text(md, encoding="utf-8")
    if with_content_list:
        (paper_dir / "content_list.json").write_text('[{"type":"equation"}]', encoding="utf-8")
    write_contract(
        MdContract(
            source_pdf_sha256="deadbeef",
            converter=converter,
            converter_version="2.0.0",
            md_sha256=sha256_bytes(md.encode("utf-8")),
            image_count=0,
            equation_block_count=md.count("$$") // 2,
        ),
        paper_dir / ".md_contract.json",
    )
    return paper_dir, pid


def test_ingest_reuses_ready_corpus_and_skips_reconvert(tmp_path, fake_http, fake_cli, candidate):
    """A committed, ready corpus entry is reused verbatim — ingest must NOT download
    or run the converter, so an off-box (pod) MinerU MD survives a re-emit instead of
    being overwritten by a fresh local conversion."""
    paper_dir, pid = _write_ready_corpus(tmp_path, candidate, md="# Reused\n$$a$$\n")

    res = ingest(candidate, tmp_path, http=fake_http, run_cli=fake_cli, now=_now)

    assert res.tier == 2
    assert res.md_path == paper_dir / f"{pid}.md"
    assert res.content_list_path == paper_dir / "content_list.json"
    assert fake_http.requested == []  # nothing fetched
    assert fake_cli.calls == []  # converter never invoked


def test_ingest_reconverts_when_committed_md_drifted(tmp_path, fake_http, fake_cli, candidate):
    """If the committed MD no longer matches its contract (corrupted/truncated), the
    reuse guard must distrust it and fall through to a fresh conversion attempt."""
    from scripts.ingest.contract import MdContract, write_contract

    pid = _paper_id(candidate)
    paper_dir = tmp_path / "corpus" / pid
    paper_dir.mkdir(parents=True)
    (paper_dir / f"{pid}.md").write_text("# drifted body\n", encoding="utf-8")
    write_contract(
        MdContract(
            source_pdf_sha256=None,
            converter="mineru",
            converter_version="2.0.0",
            md_sha256="0" * 64,  # deliberately wrong → drift
            image_count=0,
            equation_block_count=0,
        ),
        paper_dir / ".md_contract.json",
    )
    # all routes 404 → a genuine conversion attempt fails loudly, proving no reuse.
    with pytest.raises(IngestFailed):
        ingest(candidate, tmp_path, http=fake_http, run_cli=fake_cli, now=_now)
    assert fake_http.requested  # it DID try to fetch — i.e. did not reuse


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


def _eq_gate_runner(calls, pandoc_md):
    """A run_cli that emits `pandoc_md` for pandoc and a MinerU fallback."""
    from pathlib import Path

    from conftest import FakeCliResult

    def runner(argv, cwd):
        if argv[0] == "pandoc":
            calls["pandoc"] += 1
            out = argv[argv.index("-o") + 1]
            Path(cwd, out).write_text(pandoc_md)
            return FakeCliResult(returncode=0)
        out = argv[argv.index("-o") + 1]
        write_mineru_output(Path(cwd, out), md="$$z = 1$$\n", images=[], content_list="[]")
        return FakeCliResult(returncode=0)

    return runner


def test_ingest_equation_gate_demotes_when_math_dropped(tmp_path, fake_http, fake_cli, candidate):
    """Source had DISPLAY equations but pandoc produced 0 $$ -> gate demotes."""
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    html = b'<html><body><math display="block"><mi>z</mi></math>'
    html += b'<math display="block"><mi>w</mi></math></body></html>'  # 2 display eqs
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, html)
    fake_http.add(candidate["oa_pdf_url"], 200, b"%PDF body")
    calls = {"pandoc": 0}

    res = ingest(
        candidate,
        tmp_path,
        http=fake_http,
        run_cli=_eq_gate_runner(calls, "Body with no display math at all.\n"),
        now=_now,
    )

    assert calls["pandoc"] == 1  # Tier-1 ran
    assert res.tier == 2  # demoted: 0/2 display equations survived


def test_ingest_equation_gate_demotes_on_partial_loss(tmp_path, fake_http, fake_cli, candidate):
    """ROADMAP A1: even PARTIAL display-equation loss (< 50% survive) demotes."""
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    html = b"<html><body>" + b'<math display="block"><mi>a</mi></math>' * 4 + b"</body></html>"
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, html)
    fake_http.add(candidate["oa_pdf_url"], 200, b"%PDF body")
    calls = {"pandoc": 0}

    # Source has 4 display equations; pandoc emits only 1 (25% < 50%) -> demote.
    res = ingest(
        candidate, tmp_path, http=fake_http, run_cli=_eq_gate_runner(calls, "$$a$$\n"), now=_now
    )
    assert res.tier == 2


def test_ingest_equation_gate_keeps_when_most_survive(tmp_path, fake_http, fake_cli, candidate):
    """≥ 50% display equations surviving is trustworthy — keep Tier-1."""
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    html = b"<html><body>" + b'<math display="block"><mi>a</mi></math>' * 4 + b"</body></html>"
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, html)
    calls = {"pandoc": 0}

    # Source 4 display eqs; pandoc emits 3 (75% ≥ 50%) -> keep Tier-1.
    res = ingest(
        candidate,
        tmp_path,
        http=fake_http,
        run_cli=_eq_gate_runner(calls, "$$a$$\n$$b$$\n$$c$$\n"),
        now=_now,
    )
    assert res.tier == 1


def test_ingest_does_not_demote_inline_only_math(tmp_path, fake_http, fake_cli, candidate):
    """ROADMAP A1 fix: inline-only math (no display equations) legitimately emits
    0 $$ — it must NOT be demoted (the old all-or-nothing gate wrongly did)."""
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    html = b"<html><body><p>inline <math><mi>z</mi></math> only</p></body></html>"
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, html)
    calls = {"pandoc": 0}

    res = ingest(
        candidate,
        tmp_path,
        http=fake_http,
        run_cli=_eq_gate_runner(calls, "Body with inline math, no display equations.\n"),
        now=_now,
    )
    assert res.tier == 1  # not demoted — inline-only math has no display equations


def test_ingest_table_gate_demotes_when_tables_dropped(tmp_path, fake_http, fake_cli, candidate):
    """ROADMAP A2: source had data tables but pandoc dropped them (< 50% survive)."""
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    html = b"<html><body>" + b"<table><tr><td>x</td></tr></table>" * 2 + b"</body></html>"
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, html)
    fake_http.add(candidate["oa_pdf_url"], 200, b"%PDF body")
    calls = {"pandoc": 0}

    res = ingest(
        candidate,
        tmp_path,
        http=fake_http,
        run_cli=_eq_gate_runner(calls, "Body — tables all dropped.\n"),
        now=_now,
    )
    assert res.tier == 2  # 0/2 tables survived -> demoted to MinerU


def test_ingest_table_gate_keeps_when_tables_survive(tmp_path, fake_http, fake_cli, candidate):
    aid, ver = candidate["arxiv_id"], candidate["arxiv_version"]
    html = b"<html><body>" + b"<table><tr><td>x</td></tr></table>" * 2 + b"</body></html>"
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, html)
    calls = {"pandoc": 0}
    md = "| A |\n| --- |\n| 1 |\n\n| B |\n| --- |\n| 2 |\n"  # 2 GFM tables survive

    res = ingest(candidate, tmp_path, http=fake_http, run_cli=_eq_gate_runner(calls, md), now=_now)
    assert res.tier == 1  # 2/2 tables survived -> Tier-1 kept


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
