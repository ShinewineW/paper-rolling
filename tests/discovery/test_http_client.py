"""ThrottledClient: monotonic pacing, polite-pool min-interval, 429 backoff."""

from __future__ import annotations

import pytest
from scripts.discovery.http_client import HttpUnavailable, ThrottledClient


class FakeClock:
    def __init__(self):
        self.now = 1000.0
        self.slept = []

    def monotonic(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.now += seconds


class FakeHTTPError(Exception):
    def __init__(self, code: int):
        super().__init__(f"HTTP {code}")
        self.code = code


class FakeHttp:
    """Records URLs; returns queued responses. A response is either a dict
    (200 JSON / text wrapper) or an int status code to raise as HTTPError."""

    def __init__(self, responses):
        self.responses = list(responses)
        self.urls = []

    def __call__(self, url: str, timeout: float, headers=None):
        self.urls.append(url)
        self.last_headers = headers
        resp = self.responses.pop(0)
        if isinstance(resp, int):
            raise FakeHTTPError(resp)
        return resp


def make_client(http, clock, **kw):
    return ThrottledClient(http_get=http, clock=clock, http_error_cls=FakeHTTPError, **kw)


def test_first_request_does_not_sleep():
    clock = FakeClock()
    http = FakeHttp([{"ok": 1}])
    client = make_client(http, clock)
    assert client.get_json("https://api.example.com/x") == {"ok": 1}
    assert clock.slept == []


def test_anonymous_paces_at_one_per_second():
    clock = FakeClock()
    http = FakeHttp([{"a": 1}, {"b": 2}])
    client = make_client(http, clock, min_interval=1.0)
    client.get_json("https://api.example.com/1")
    client.get_json("https://api.example.com/2")
    # second call had ~0 elapsed since the first, so it sleeps the full interval
    assert clock.slept == [1.0]


def test_polite_pool_raises_rate_to_short_interval():
    clock = FakeClock()
    http = FakeHttp([{"a": 1}, {"b": 2}])
    client = make_client(http, clock, min_interval=1.0, polite_interval=0.1, polite=True)
    client.get_json("https://api.example.com/1")
    client.get_json("https://api.example.com/2")
    assert clock.slept == [0.1]


def test_429_backs_off_2s_then_succeeds():
    clock = FakeClock()
    http = FakeHttp([429, {"ok": 1}])
    client = make_client(http, clock)
    assert client.get_json("https://api.example.com/x") == {"ok": 1}
    # one 2s backoff before the retry that succeeded
    assert 2.0 in clock.slept


def test_429_exhausts_after_three_retries():
    clock = FakeClock()
    http = FakeHttp([429, 429, 429, 429])
    client = make_client(http, clock)
    with pytest.raises(HttpUnavailable):
        client.get_json("https://api.example.com/x")
    assert clock.slept.count(2.0) == 3


def test_404_returns_empty_dict():
    clock = FakeClock()
    http = FakeHttp([404])
    client = make_client(http, clock)
    assert client.get_json("https://api.example.com/missing") == {}


def test_5xx_raises_unavailable_no_retry():
    clock = FakeClock()
    http = FakeHttp([503])
    client = make_client(http, clock)
    with pytest.raises(HttpUnavailable):
        client.get_json("https://api.example.com/x")


def test_get_json_forwards_per_request_headers():
    # Regression (Codex Round-8): the shared production client MUST accept and
    # forward per-request headers (e.g. the HF Papers Authorization bearer that
    # hf_papers.py passes). Previously get_json had no `headers` param, so the
    # real ThrottledClient raised TypeError on the HF discovery path.
    clock = FakeClock()
    http = FakeHttp([{"ok": True}])
    client = make_client(http, clock)
    out = client.get_json(
        "https://huggingface.co/api/papers/search",
        {"q": "topic"},
        headers={"Authorization": "Bearer hf_xxx"},
    )
    assert out == {"ok": True}
    assert http.last_headers == {"Authorization": "Bearer hf_xxx"}
