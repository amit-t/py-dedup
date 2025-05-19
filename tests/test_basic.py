""Basic tests for the py-dedup library."""
import json
import time
import unittest
from typing import Any, Dict

from py_dedup import Deduplicator, MemoryCache


class TestDeduplicator(unittest.TestCase):
    """Test cases for the Deduplicator class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.cache = MemoryCache()
        self.ttl_seconds = 1  # 1 second TTL for testing
        self.deduper = Deduplicator(
            ttl_seconds=self.ttl_seconds, cache_backend=self.cache
        )

    def test_duplicate_detection(self) -> None:
        ""Test that duplicate messages are detected."""
        message = {"id": "123", "data": "test"}
        
        # First time should not be a duplicate
        self.assertFalse(self.deduper.is_duplicate(message))
        
        # Second time should be a duplicate
        self.assertTrue(self.deduper.is_duplicate(message))

    def test_ttl_expiration(self) -> None:
        ""Test that deduplication expires after TTL."""
        message = {"id": "456", "data": "test-ttl"}
        
        # First time should not be a duplicate
        self.assertFalse(self.deduper.is_duplicate(message))
        
        # Should be a duplicate immediately after
        self.assertTrue(self.deduper.is_duplicate(message))
        
        # Wait for TTL to expire
        time.sleep(self.ttl_seconds + 0.1)  # Add a small buffer
        
        # Should not be a duplicate after TTL
        self.assertFalse(self.deduper.is_duplicate(message))

    def test_different_messages(self) -> None:
        ""Test that different messages are not marked as duplicates."""
        message1 = {"id": "1", "data": "test1"}
        message2 = {"id": "2", "data": "test2"}
        
        # First message should not be a duplicate
        self.assertFalse(self.deduper.is_duplicate(message1))
        
        # Second message should also not be a duplicate
        self.assertFalse(self.deduper.is_duplicate(message2))
        
        # Both should be duplicates now
        self.assertTrue(self.deduper.is_duplicate(message1))
        self.assertTrue(self.deduper.is_duplicate(message2))

    def test_custom_key(self) -> None:
        ""Test deduplication with custom keys."""
        message1 = {"id": "1", "data": "test1"}
        message2 = {"id": "2", "data": "test2"}
        
        # Use the same custom key for different messages
        custom_key = "my-custom-key"
        
        # First time with custom key should not be a duplicate
        self.assertFalse(self.deduper.is_duplicate(message1, custom_key=custom_key))
        
        # Different message but same custom key should be a duplicate
        self.assertTrue(self.deduper.is_duplicate(message2, custom_key=custom_key))

    def test_clear_cache(self) -> None:
        ""Test that clearing the cache works."""
        message = {"id": "789", "data": "test-clear"}
        
        # Add to cache
        self.assertFalse(self.deduper.is_duplicate(message))
        self.assertTrue(self.deduper.is_duplicate(message))
        
        # Clear cache
        self.deduper.clear()
        
        # Should not be a duplicate after clear
        self.assertFalse(self.deduper.is_duplicate(message))

    def test_json_serialization(self) -> None:
        ""Test that JSON serialization works as expected."""
        message = {"id": "json-1", "data": [1, 2, 3], "nested": {"a": 1, "b": 2}}
        
        # Should handle dict directly
        self.assertFalse(self.deduper.is_duplicate(message))
        self.assertTrue(self.deduper.is_duplicate(message))
        
        # Should handle JSON string
        json_str = json.dumps(message)
        self.assertTrue(self.deduper.is_duplicate(json_str))
        
        # Different order of keys should still be considered the same
        different_order = json.dumps({"nested": {"b": 2, "a": 1}, "id": "json-1", "data": [1, 2, 3]})
        self.assertTrue(self.deduper.is_duplicate(different_order))


if __name__ == "__main__":
    unittest.main()
