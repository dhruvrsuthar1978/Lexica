"""Rate limiting extension points."""

import asyncio
from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Deque, Dict, Protocol

from app.core.exceptions import AppError, ErrorType


class RateLimiter(Protocol):
    """Protocol for rate limiting implementations."""

    async def check(self, key: str) -> None:
        """Raise RateLimitExceededError if the key exceeds policy."""


class RateLimitExceededError(AppError):
    """Request was rejected by a rate limiter."""

    def __init__(self, message: str = "Too many requests") -> None:
        super().__init__(
            message,
            error_type=ErrorType.RATE_LIMITED,
            status_code=429,
        )


class InMemoryRateLimiter:
    """Simple in-memory sliding-window rate limiter."""

    def __init__(self, requests: int, window_seconds: int) -> None:
        self._requests = requests
        self._window = timedelta(seconds=window_seconds)
        self._history: Dict[str, Deque[datetime]] = {}
        self._lock = asyncio.Lock()

    async def check(self, key: str) -> None:
        now = datetime.now(timezone.utc)
        async with self._lock:
            entries = self._history.setdefault(key, deque())
            cutoff = now - self._window
            while entries and entries[0] < cutoff:
                entries.popleft()
            if len(entries) >= self._requests:
                raise RateLimitExceededError(
                    f"Too many requests for key {key}. Limit is {self._requests} per {int(self._window.total_seconds())} seconds."
                )
            entries.append(now)


class NoopRateLimiter:
    """Default rate limiter that permits all requests."""

    async def check(self, key: str) -> None:
        """Permit the request."""
