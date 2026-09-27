"""Reusable helpers for Django cache operations.

This module provides a small abstraction around Django's cache
framework so application services do not need to interact with
the cache backend directly.

The configured cache backend may be LocMemCache during development
and Redis in production without requiring changes to the service
layer.
"""

from __future__ import annotations

from typing import Any

from django.core.cache import cache

def get_cache(
key: str,
default: Any = None,
) -> Any:
    """Retrieve a value from the configured cache backend.

    Args:
        key: Unique cache key.
        default: Value returned when the key does not exist.

    Returns:
        Cached value if present; otherwise the default value.
    """
    return cache.get(
        key,
        default=default,
    )
def set_cache(
key: str,
value: Any,
timeout: int,
) -> None:
    """Store a value in the configured cache backend.

    Args:
        key: Unique cache key.
        value: Value to store.
        timeout: Cache lifetime in seconds.
    """
    cache.set(
        key,
        value,
        timeout=timeout,
    )
def delete_cache(
key: str,
) -> None:
    """Remove a value from the configured cache backend.

    Args:
        key: Cache key to invalidate.
    """
    cache.delete(key)