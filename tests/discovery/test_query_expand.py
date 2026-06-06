"""LLM query expansion + OpenAlex topic anchoring (D-发现-6)."""

from __future__ import annotations

from scripts.discovery.query_expand import expand_queries, resolve_topic_id


def fake_llm(prompt: str) -> list[str]:
    # Deterministic stand-in for the LLM expansion call.
    assert "end-to-end driving" in prompt
    return ["end-to-end driving", "BEVFormer", "trajectory planning", "  ", "BEVFormer"]


def test_expand_dedups_and_strips_blanks_and_includes_seed():
    out = expand_queries("end-to-end driving", llm=fake_llm)
    assert "end-to-end driving" in out
    assert "BEVFormer" in out
    assert "trajectory planning" in out
    assert "" not in out
    assert "  " not in out
    # dedup: BEVFormer appears once
    assert out.count("BEVFormer") == 1


def test_second_round_uses_ai_keywords():
    out = expand_queries(
        "end-to-end driving", llm=fake_llm, ai_keywords=["diffusion policy", "BEVFormer"]
    )
    assert "diffusion policy" in out
    assert out.count("BEVFormer") == 1  # still deduped against round 1


class StubClient:
    def __init__(self, payload):
        self.payload = payload
        self.calls = []

    def get_json(self, url, query=None):
        self.calls.append((url, dict(query or {})))
        return self.payload


def test_resolve_topic_id_returns_best_match_id():
    payload = {
        "results": [{"id": "https://openalex.org/T10044", "display_name": "Autonomous Driving"}]
    }
    client = StubClient(payload)
    tid = resolve_topic_id("autonomous driving", client)
    assert tid == "T10044"
    url, q = client.calls[0]
    assert "/topics" in url
    assert q["search"] == "autonomous driving"


def test_resolve_topic_id_none_on_empty():
    client = StubClient({"results": []})
    assert resolve_topic_id("nonsense", client) is None
