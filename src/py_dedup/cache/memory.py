""
In-memory cache implementation for deduplication.

This module provides a simple in-memory cache using an ordered dictionary
with TTL (time-to-live) support.
"""
import time
from collections import OrderedDict
from typing import Optional

from ..exceptions import CacheError
from .base import BaseCache


class MemoryCache(BaseCache):
    """
    In-memory cache implementation using an ordered dictionary with TTL support.

    This implementation is thread-safe for single operations but not for bulk operations.
    """

    def __init__(self) -> None:
        """Initialize the in-memory cache."""
        self._cache: OrderedDict[str, float] = OrderedDict()

    def get(self, key: str) -> bool:
        """
        Check if a key exists in the cache and has not expired.

        Args:
            key: The key to check.

        Returns:
            bool: True if the key exists and has not expired, False otherwise.
        """
        expire_time = self._cache.get(key)
        if expire_time is None:
            return False

        if expire_time < time.monotonic():
            # Key has expired, remove it
            self.delete(key)
            return False

        return True

    def set(self, key: str, ttl_seconds: int) -> None:
        """
        Add a key to the cache with a TTL.

        Args:
            key: The key to add.
            ttl_seconds: Time to live in seconds.

        Raises:
            CacheError: If TTL is not a positive number.
        """
        if ttl_seconds <= 0:
            raise CacheError("TTL must be a positive number")

        self._cache[key] = time.monotonic() + ttl_seconds
        # Move the key to the end to maintain LRU order
        self._cache.move_to_end(key)

    def delete(self, key: str) -> None:
        """
        Remove a key from the cache.

        Args:
            key: The key to remove.
        """
        self._cache.pop(key, None)

    def clear(self) -> None:
        """Clear all keys from the cache."""
        self._cache.clear()

    def _clean_expired(self) -> None:
        """Remove all expired keys from the cache."""
        current_time = time.monotonic()
        # Create a list of keys to delete to avoid modifying the dict during iteration
        expired_keys = [k for k, v in self._cache.items() if v < current_time]
        for key in expired_keys:
            self.delete(key)

    def __contains__(self, key: str) -> bool:
        """Check if a key exists in the cache and has not expired."""
        return self.get(key)
