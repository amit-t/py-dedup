""
Base cache interface for the deduplication system.

This module defines the abstract base class that all cache backends must implement.
"""
from abc import ABC, abstractmethod
from typing import Any, Optional


class BaseCache(ABC):
    """Abstract base class for all cache backends."""

    @abstractmethod
    def get(self, key: str) -> bool:
        """
        Check if a key exists in the cache.

        Args:
            key: The key to check.

        Returns:
            bool: True if the key exists, False otherwise.
        """
        raise NotImplementedError

    @abstractmethod
    def set(self, key: str, ttl_seconds: int) -> None:
        """
        Add a key to the cache with a TTL.

        Args:
            key: The key to add.
            ttl_seconds: Time to live in seconds.
        """
        raise NotImplementedError

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Remove a key from the cache.

        Args:
            key: The key to remove.
        """
        raise NotImplementedError

    @abstractmethod
    def clear(self) -> None:
        """Clear all keys from the cache."""
        raise NotImplementedError
