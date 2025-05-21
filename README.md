# py-dedup

[![Python Version](https://img.shields.io/pypi/pyversions/py-dedup)](https://pypi.org/project/py-dedup/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A lightweight Python library that provides time-bound deduplication for messages read from a queue/stream. It prevents reprocessing of duplicate messages arriving within a defined sliding time window.

## Features

- **Time-based Deduplication**: Prevent processing of duplicate messages within a configurable time window
- **Multiple Payload Formats**: Supports JSON and Protobuf payloads via consistent hashing
- **Pluggable Cache Backends**: Built-in in-memory cache with support for Redis as a distributed cache backend
- **Simple API**: Easy-to-use interface for checking message duplication

## Installation

```bash
pip install py-dedup
```

For Redis backend support:

```bash
pip install "py-dedup[redis]"
```

## Quick Start

```python
from py_dedup import Deduplicator
from py_dedup.cache.memory import MemoryCache

# Initialize with a 60-second deduplication window
cache = MemoryCache()
deduper = Deduplicator(ttl_seconds=60, cache_backend=cache)

# Check if a message is a duplicate
message = {"id": "123", "data": "example"}
if not deduper.is_duplicate(message, format="json"):
    # Process the message
    print("Processing new message")
else:
    print("Duplicate message, skipping")
```

## Documentation

Full documentation is available at [https://github.com/amit-t/py-dedup](https://github.com/yourusername/py-dedup).

## Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on how to submit pull requests, report issues, or suggest improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
