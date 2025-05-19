"""Custom exceptions for the py-dedup library."""

from typing import Optional


class DeduplicationError(Exception):
    """Base exception for all deduplication-related errors."""

    def __init__(self, message: str, original_exception: Optional[Exception] = None):
        self.message = message
        self.original_exception = original_exception
        super().__init__(self.message)


class CacheError(DeduplicationError):
    """Raised when there is an error with the cache backend."""

    pass


class SerializationError(DeduplicationError):
    """Raised when there is an error serializing/deserializing data."""

    pass


class ConfigurationError(DeduplicationError):
    """Raised when there is a configuration error."""

    pass
