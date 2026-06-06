import pytest
from conftest import write_mineru_output
from scripts.ingest.contract import sha256_bytes
from scripts.ingest.tier2_mineru import Tier2Failed, run_tier2


def test_tier2_success_collects_md_images_and_content_list(tmp_path, fake_http, fake_cli):
    pdf_bytes = b"%PDF-1.7 fake body"
    pdf_url = "https://arxiv.org/pdf/2401.0009v2"
    fake_http.add(pdf_url, 200, pdf_bytes)

    def mineru(argv, cwd):
        # MinerU writes into the -o output dir (joined under cwd).
        from pathlib import Path

        out = argv[argv.index("-o") + 1]
        write_mineru_output(
            Path(cwd, out),
            md="# Title\n$$E = mc^2$$\n",
            images=["a.png", "b.png"],
            content_list='[{"type":"equation","text":"E = mc^2"}]',
        )

    fake_cli.program(returncode=0, side_effect=mineru)

    res = run_tier2(pdf_url, tmp_path, http=fake_http, run_cli=fake_cli, mineru_version="2.0.0")

    assert "$$E = mc^2$$" in res.md_text
    assert sorted(res.images) == ["a.png", "b.png"]
    assert res.content_list_path.name == "content_list.json"
    assert res.source_pdf_sha256 == sha256_bytes(pdf_bytes)
    # CPU backend must be requested (摄取-D1 / spec §2.2 Apple-Silicon caveat).
    argv = fake_cli.calls[0].argv
    assert argv[0] == "mineru"
    assert "-b" in argv and argv[argv.index("-b") + 1] in {"pipeline", "cpu"}


def test_tier2_pdf_download_failure_raises(tmp_path, fake_http, fake_cli):
    with pytest.raises(Tier2Failed) as ei:
        run_tier2(
            "https://arxiv.org/pdf/missing",
            tmp_path,
            http=fake_http,
            run_cli=fake_cli,
            mineru_version="2",
        )
    assert "pdf_download" in str(ei.value)


def test_tier2_mineru_nonzero_exit_raises(tmp_path, fake_http, fake_cli):
    pdf_url = "https://arxiv.org/pdf/2401.0010v1"
    fake_http.add(pdf_url, 200, b"%PDF body")
    fake_cli.program(returncode=3, stderr="CUDA oom")
    with pytest.raises(Tier2Failed) as ei:
        run_tier2(pdf_url, tmp_path, http=fake_http, run_cli=fake_cli, mineru_version="2")
    assert "mineru_failed" in str(ei.value)
