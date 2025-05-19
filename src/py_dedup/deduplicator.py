""
Core deduplication functionality.

This module provides the main Deduplicator class that handles message deduplication
using a configurable cache backend and hashing strategy.
"""
import time
from typing import Any, Optional, Union

from .cache.base import BaseCache
from .exceptions import CacheError, ConfigurationError, SerializationError
from .hasher import HashAlgorithm, MessageHasher


class Deduplicator:
    """
    A deduplicator that prevents processing of duplicate messages within a time window.

    This class provides a simple interface for checking if a message has been seen
    within a configurable time window (TTL). It uses a cache backend to store message
    hashes and a hashing strategy to generate consistent hashes from messages.
    """

    def __init__(
        self,
        ttl_seconds: int,
        cache_backend: Optional[BaseCache] = None,
        hash_algorithm: HashAlgorithm = HashAlgorithm.SHA256,
        key_prefix: str = "dedup:",
    ) -> None:
        """
        Initialize the deduplicator.

        Args:
            ttl_seconds: Time to live for deduplication entries in seconds.
            cache_backend: The cache backend to use. If None, a new MemoryCache is used.
            hash_algorithm: The hash algorithm to use for message hashing.
            key_prefix: Prefix to use for cache keys.

        Raises:
            ConfigurationError: If ttl_seconds is not a positive integer.
        """
        if not isinstance(ttl_seconds, int) or ttl_seconds <= 0:
            raise ConfigurationError("ttl_seconds must be a positive integer")

        self.ttl_seconds = ttl_seconds
        self.cache = cache_backend or self._create_default_cache()
        self.hasher = MessageHasher(algorithm=hash_algorithm)
        self.key_prefix = key_prefix

    def is_duplicate(
        self,
        message: Any,
        format: str = "json",
        custom_key: Optional[str] = None,
        **kwargs: Any,
    ) -> bool:
        """
        Check if a message is a duplicate and update the cache if it's not.

        Args:
            message: The message to check.
            format: The format of the message ('json' or 'protobuf').
            custom_key: Optional custom key to use instead of hashing the message.
            **kwargs: Additional arguments to pass to the hasher.

        Returns:
            bool: True if the message is a duplicate, False otherwise.

        Raises:
            SerializationError: If the message cannot be hashed.
            CacheError: If there is an error accessing the cache.
        """
        try:
            # Generate a cache key
            if custom_key is not None:
                cache_key = f"{self.key_prefix}{custom_key}"
            else:
                # Hash the message to create a consistent key
                message_hash = self.hasher.hash_message(message, format=format, **kwargs)
                cache_key = f"{self.key_prefix}{message_hash}"

            # Check if the key exists in the cache
            is_duplicate = self.cache.get(cache_key)

            # If not a duplicate, add it to the cache
            if not is_duplicate:
                self.cache.set(cache_key, self.ttl_seconds)

            return is_duplicate

        except Exception as e:
            if isinstance(e, (SerializationError, CacheError)):
                raise
            # Wrap unexpected errors
            raise CacheError(f"Unexpected error during deduplication: {e}") from e

    def _create_default_cache(self) -> BaseCache:
        """Create a default in-memory cache."""
        from .cache.memory import MemoryCache  # Avoid circular import

        return MemoryCache()

    def clear(self) -> None:
        """Clear all entries from the cache."""
        self.cache.clear()

    def __enter__(self):
        """Support for context manager protocol."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Clean up resources when exiting the context."""
        self.clear()
