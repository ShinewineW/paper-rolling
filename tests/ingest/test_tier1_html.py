import pytest
from scripts.ingest.tier1_html import Tier1Unavailable, run_tier1


def test_tier1_success_converts_and_downloads_figures(tmp_path, fake_http, fake_cli):
    aid, ver = "2401.00001", "v1"
    html = (
        b"<html><body><p>Body <math><mi>x</mi></math></p>"
        b'<figure><img src="fig1.png"/></figure></body></html>'
    )
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, html)
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}/fig1.png", 200, b"\x89PNG")

    def pandoc(argv, cwd):
        # emulate pandoc: find -o target (bare filename), write GFM into cwd.
        out = argv[argv.index("-o") + 1]
        (tmp_path / out).write_text("Body $$x$$\n\n![](images/fig1.png)\n")

    fake_cli.program(returncode=0, side_effect=pandoc)

    out = run_tier1(aid, ver, tmp_path, http=fake_http, run_cli=fake_cli, pandoc_version="3.1.2")

    assert "$$x$$" in out.md_text
    assert out.images == ["fig1.png"]
    assert out.html_had_math is True
    assert (tmp_path / "images" / "fig1.png").read_bytes() == b"\x89PNG"
    argv = fake_cli.calls[0].argv
    assert "--from" in argv and argv[argv.index("--from") + 1] == "html"
    assert "--to" in argv and argv[argv.index("--to") + 1] == "gfm"


def test_tier1_missing_html_raises_unavailable(tmp_path, fake_http, fake_cli):
    aid, ver = "2401.00002", "v1"
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 404, b"")
    with pytest.raises(Tier1Unavailable) as ei:
        run_tier1(aid, ver, tmp_path, http=fake_http, run_cli=fake_cli, pandoc_version="3")
    assert "html_missing" in str(ei.value)


def test_tier1_latexml_error_marker_raises_unavailable(tmp_path, fake_http, fake_cli):
    aid, ver = "2401.00003", "v1"
    bad = b'<html><body><span class="ltx_ERROR">Undefined macro</span></body></html>'
    fake_http.add(f"https://arxiv.org/html/{aid}{ver}", 200, bad)
    with pytest.raises(Tier1Unavailable) as ei:
        run_tier1(aid, ver, tmp_path, http=fake_http, run_cli=fake_cli, pandoc_version="3")
    assert "latexml_error" in str(ei.value)
