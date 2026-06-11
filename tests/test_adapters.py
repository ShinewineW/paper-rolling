"""Default infra adapters (build_http / build_run_cli / build_discover).

Deterministic wiring tests — no network (stub/monkeypatch only), per the
project's test-isolation rule. A live end-to-end discovery smoke is run manually,
not committed here.
"""

from __future__ import annotations

import sys

import scripts.adapters as adapters
from scripts.adapters import _PacedTextClient, build_discover, build_http, build_run_cli


class _FakeResp:
    def __init__(self, status_code: int, content: bytes) -> None:
        self.status_code = status_code
        self.content = content


def test_build_http_returns_status_and_bytes(monkeypatch):
    captured = {}

    def fake_get(url, timeout, headers):
        captured["url"] = url
        captured["timeout"] = timeout
        return _FakeResp(200, b"<html>ok</html>")

    monkeypatch.setattr(adapters.requests, "get", fake_get)
    status, body = build_http(timeout=7.0)("https://example.org/p")
    assert status == 200
    assert body == b"<html>ok</html>"
    assert captured["url"] == "https://example.org/p"
    assert captured["timeout"] == 7.0


def test_build_http_network_error_is_clean_failure(monkeypatch):
    def boom(*a, **k):
        raise adapters.requests.RequestException("down")

    monkeypatch.setattr(adapters.requests, "get", boom)
    status, body = build_http()("https://example.org")
    assert status == 0
    assert body == b""


def test_build_run_cli_success():
    result = build_run_cli()([sys.executable, "-c", "print('hi')"], ".")
    assert result.returncode == 0
    assert "hi" in result.stdout


def test_build_run_cli_nonzero_does_not_raise():
    result = build_run_cli()([sys.executable, "-c", "import sys; sys.exit(3)"], ".")
    assert result.returncode == 3


def test_build_discover_wires_five_sources_and_config(monkeypatch):
    seen = {}

    def fake_discover(campaign_config, sources, llm):
        seen["config"] = campaign_config
        seen["sources"] = sources
        seen["llm"] = llm
        return [{"title": "x"}]

    monkeypatch.setattr(adapters, "_discover", fake_discover)

    def fake_llm(prompt):
        return ["q1", "q2"]

    discover = build_discover(
        fake_llm,
        is_ad_domain=False,
        from_year=2025,
        overfetch_factor=2,
        force_include=[{"arxiv_id": "2401.00001", "title": "Forced"}],
    )
    out = discover("world models", 5)

    assert out == [{"title": "x"}]
    assert set(seen["sources"]) == {"openalex", "s2", "arxiv", "dblp", "hf_papers"}
    cfg = seen["config"]
    assert cfg["topic"] == "world models"
    assert cfg["top_k"] == 5
    assert cfg["is_ad_domain"] is False
    assert cfg["from_year"] == 2025
    assert cfg["from_date"] == "2025-01-01"
    assert cfg["overfetch_factor"] == 2
    assert cfg["force_include"] == [{"arxiv_id": "2401.00001", "title": "Forced"}]
    assert cfg["auto_discover"] is True  # default (自发查找) forwarded
    assert seen["llm"] is fake_llm


def test_build_discover_forwards_auto_discover_false(monkeypatch):
    """指定列表 mode: auto_discover=False must reach the orchestrator's campaign_config
    (a silent default-to-True would turn list mode into auto-discovery — wrong papers)."""
    seen = {}
    monkeypatch.setattr(adapters, "_discover", lambda c, s, _llm: seen.update(c) or [])
    build_discover(lambda _p: [], auto_discover=False)("t", 3)
    assert seen["auto_discover"] is False


def test_build_discover_defaults_from_year_to_two_years_back(monkeypatch):
    seen = {}
    monkeypatch.setattr(adapters, "_discover", lambda c, s, _llm: seen.update(c) or [])
    build_discover(lambda _p: [])("t", 3)
    assert seen["from_year"] == seen["current_year"] - 2
    assert seen["from_date"] == f"{seen['from_year']}-01-01"


def test_paced_text_client_get_text_decodes_and_urlencodes(monkeypatch):
    captured = {}

    class _FakeResp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b"<feed>ok</feed>"

    def fake_urlopen(req, timeout):
        captured["url"] = req.full_url
        return _FakeResp()

    monkeypatch.setattr(adapters.urllib.request, "urlopen", fake_urlopen)
    client = _PacedTextClient(min_interval=0.0)  # no real sleep in test
    text = client.get_text("http://export.arxiv.org/api/query", {"search_query": "all:x"})
    assert text == "<feed>ok</feed>"
    assert "search_query=all%3Ax" in captured["url"]
