"""HUB-owned throttled HTTP client.

Net-new (CC-BY-NC repo). Reimplements the structural pacing pattern documented for the
academic-research-skills clients (monotonic-clock min-interval, polite-pool
raises the rate, 429 -> 2s backoff x 3). Network + clock are injected so the
client is unit-testable without sockets and HUB can share one instance per
source (§5.4: never N clients racing the same endpoint).
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from collections.abc import Callable, Mapping
from typing import Any

_BACKOFF_SECONDS = 2.0
_MAX_RETRIES = 3
_ANONYMOUS_MIN_INTERVAL = 1.0
_POLITE_MIN_INTERVAL = 0.1


class HttpUnavailable(Exception):
    """Source degraded — caller treats this source as missing for this query
    (LS-5: one source down != whole pipeline down)."""


class _Clock:
    monotonic = staticmethod(time.monotonic)
    sleep = staticmethod(time.sleep)


def _default_http_get(
    url: str, timeout: float, headers: Mapping[str, str] | None = None
) -> dict[str, Any]:
    all_headers = {"User-Agent": "paper-rolling/0.1", **(headers or {})}
    req = urllib.request.Request(url, headers=all_headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (host-pinned by caller)
        body = resp.read()
    return json.loads(body.decode("utf-8"))


class ThrottledClient:
    """Serial, paced GET client. One instance per source, shared by the HUB.

    Args:
        http_get: callable (url, timeout) -> parsed JSON dict; raises
            http_error_cls (with `.code`) on HTTP status errors.
        clock: object exposing monotonic() and sleep(); defaults to real time.
        http_error_cls: the exception type carrying a `.code` int attribute.
        min_interval: anonymous pacing floor in seconds.
        polite_interval: pacing floor when polite=True.
        polite: True when a polite-pool credential lifts the rate.
        timeout: per-request timeout in seconds.
    """

    def __init__(
        self,
        http_get: Callable[[str, float, Mapping[str, str] | None], dict[str, Any]] | None = None,
        clock: Any | None = None,
        http_error_cls: type[Exception] = urllib.error.HTTPError,
        min_interval: float = _ANONYMOUS_MIN_INTERVAL,
        polite_interval: float = _POLITE_MIN_INTERVAL,
        polite: bool = False,
        timeout: float = 30.0,
    ) -> None:
        self._http_get = http_get or _default_http_get
        self._clock = clock or _Clock()
        self._http_error_cls = http_error_cls
        self._min_interval = polite_interval if polite else min_interval
        self._timeout = timeout
        self._last_request_at: float | None = None

    def _throttle(self) -> None:
        if self._last_request_at is None:
            return
        # time.monotonic (not time.time): NTP / manual clock adjustments can
        # make wall-clock go backward, producing a negative elapsed and either
        # a huge sleep or none. Monotonic is immune.
        elapsed = self._clock.monotonic() - self._last_request_at
        if elapsed < self._min_interval:
            self._clock.sleep(self._min_interval - elapsed)

    def get_json(
        self,
        url: str,
        query: Mapping[str, str] | None = None,
        *,
        headers: Mapping[str, str] | None = None,
    ) -> dict[str, Any]:
        """GET url (optionally appending urlencoded query) and parse JSON.

        `headers` are extra per-request headers (e.g. an Authorization bearer
        for HF Papers) merged on top of the default User-Agent.

        Returns {} on 404. Raises HttpUnavailable on 5xx, network errors, or
        exhausted 429 retries.
        """
        full_url = url
        if query:
            from urllib.parse import urlencode

            sep = "&" if "?" in url else "?"
            full_url = f"{url}{sep}{urlencode(dict(query))}"

        self._throttle()
        self._last_request_at = self._clock.monotonic()

        for attempt in range(_MAX_RETRIES + 1):
            try:
                return self._http_get(full_url, self._timeout, headers)
            except self._http_error_cls as e:
                code = getattr(e, "code", None)
                if code == 404:
                    return {}
                if code == 429 and attempt < _MAX_RETRIES:
                    self._clock.sleep(_BACKOFF_SECONDS)
                    # Re-anchor so the next _throttle() paces against wake time,
                    # not entry time (else it under-sleeps and re-trips 429).
                    self._last_request_at = self._clock.monotonic()
                    continue
                raise HttpUnavailable(f"HTTP {code}") from e
            except (urllib.error.URLError, TimeoutError, OSError) as e:
                raise HttpUnavailable(f"network error: {e}") from e

        raise HttpUnavailable("rate limit exhausted after retries")
