"""
py-dedup - A lightweight Python library for time-bound message deduplication.

This library provides a simple interface for preventing duplicate message processing
within a configurable time window, with support for multiple cache backends.
"""

from typing import Any, Optional, Union

from .cache.base import BaseCache
from .cache.memory import MemoryCache
from .deduplicator import Deduplicator
from .exceptions import DeduplicationError
from .hasher import HashAlgorithm, MessageHasher

__version__ = "0.1.0"

__all__ = [
    "Deduplicator",
    "BaseCache",
    "MemoryCache",
    "MessageHasher",
    "HashAlgorithm",
    "DeduplicationError",
]
