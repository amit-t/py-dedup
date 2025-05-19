"""Cache backends for the deduplication system.

This package provides various cache implementations that can be used with the
Deduplicator class.
"""

from .base import BaseCache
from .memory import MemoryCache

__all__ = ["BaseCache", "MemoryCache"]
