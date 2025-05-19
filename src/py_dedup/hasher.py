""
Message hashing utilities for deduplication.

This module provides functionality to generate consistent hashes from messages
in different formats (JSON, Protobuf, etc.) for deduplication purposes.
"""
import hashlib
import json
from enum import Enum
from typing import Any, Dict, Optional, Union

from .exceptions import SerializationError


class HashAlgorithm(str, Enum):
    """Supported hash algorithms for message hashing."""

    SHA256 = "sha256"
    MD5 = "md5"
    SHA1 = "sha1"


class MessageHasher:
    """
    Utility class for hashing messages in different formats.

    This class provides methods to generate consistent hashes from messages
    in various formats (JSON, Protobuf, etc.) for deduplication purposes.
    """

    def __init__(
        self,
        algorithm: HashAlgorithm = HashAlgorithm.SHA256,
        sort_keys: bool = True,
    ) -> None:
        """
        Initialize the message hasher.

        Args:
            algorithm: The hash algorithm to use.
            sort_keys: Whether to sort dictionary keys before hashing (for JSON).
        """
        self.algorithm = algorithm
        self.sort_keys = sort_keys

    def hash_message(
        self, message: Any, format: str = "json", **kwargs: Any
    ) -> str:
        """
        Generate a hash for the given message.

        Args:
            message: The message to hash. Can be a dict, string, or protobuf message.
            format: The format of the message ('json' or 'protobuf').
            **kwargs: Additional format-specific arguments.

        Returns:
            str: The hexadecimal digest of the hash.

        Raises:
            SerializationError: If the message cannot be hashed.
        """
        format = format.lower()
        if format == "json":
            return self._hash_json(message, **kwargs)
        elif format == "protobuf":
            return self._hash_protobuf(message, **kwargs)
        else:
            raise SerializationError(f"Unsupported message format: {format}")

    def _hash_json(self, message: Any, **kwargs: Any) -> str:
        """
        Generate a hash for a JSON-serializable message.

        Args:
            message: The message to hash.
            **kwargs: Additional arguments for JSON serialization.

        Returns:
            str: The hexadecimal digest of the hash.
        """
        try:
            # If message is already a string, parse it to ensure consistent formatting
            if isinstance(message, str):
                message = json.loads(message)

            # Convert to JSON with consistent formatting
            json_str = json.dumps(
                message,
                sort_keys=self.sort_keys,
                ensure_ascii=False,
                **kwargs,
            )
            return self._hash_string(json_str)
        except (TypeError, ValueError) as e:
            raise SerializationError(f"Failed to serialize message to JSON: {e}") from e

    def _hash_protobuf(self, message: Any, **kwargs: Any) -> str:
        """
        Generate a hash for a protobuf message.

        Args:
            message: The protobuf message to hash.
            **kwargs: Additional arguments for protobuf serialization.

        Returns:
            str: The hexadecimal digest of the hash.

        Raises:
            SerializationError: If the message is not a valid protobuf message.
        """
        try:
            # Check if the message has SerializeToString method
            if not hasattr(message, "SerializeToString"):
                raise AttributeError(
                    "Message does not have SerializeToString method. "
                    "Is this a valid protobuf message?"
                )
            serialized = message.SerializeToString(**kwargs)
            return self._hash_bytes(serialized)
        except Exception as e:
            raise SerializationError(
                f"Failed to serialize protobuf message: {e}"
            ) from e

    def _hash_string(self, s: str) -> str:
        """
        Generate a hash for a string.

        Args:
            s: The string to hash.

        Returns:
            str: The hexadecimal digest of the hash.
        """
        return self._hash_bytes(s.encode("utf-8"))

    def _hash_bytes(self, b: bytes) -> str:
        """
        Generate a hash for bytes.

        Args:
            b: The bytes to hash.

        Returns:
            str: The hexadecimal digest of the hash.
        """
        hasher = hashlib.new(self.algorithm.value)
        hasher.update(b)
        return hasher.hexdigest()
