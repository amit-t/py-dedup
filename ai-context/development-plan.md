# Python Deduplication Library Development Plan

## Repo Name
`py-dedup`

## Objective
Create a lightweight Python library that provides time-bound deduplication for messages read from a queue/stream. It prevents reprocessing of duplicate messages arriving within a defined sliding time window. Supports JSON and Protobuf payloads via consistent hashing.

---

## Phase 0: Bootstrap Setup

### Files
- `.gitignore`
- `pyproject.toml` (use `poetry` or `hatch`)
- `README.md`
- `LICENSE`
- `src/lib/__init__.py`
- `tests/test_basic.py`

### Steps
- Initialize Git repo
- Set up Python project using `poetry init`
- Configure test framework (`pytest`)

---

## Phase 1: Core Library Structure

### File Structure
```
src/lib/
  __init__.py
  cache.py
  hasher.py
  models.py
  deduplicator.py
```

### Modules
- `cache.py`: In-memory TTL cache implementation (using `collections.OrderedDict` or `cachetools.TTLCache`)
- `hasher.py`: Implements consistent hashing for JSON/Protobuf
- `models.py`: Typed message abstraction (dataclasses)
- `deduplicator.py`: Central deduplication logic using sliding window

### Steps
- Implement a time-based cache
- Hash messages to create a unique key
- Store keys in cache with TTL
- On new message, check if key is in cache
- If not, process and store; else ignore

---

## Phase 2: Message Hashing Engine

### `hasher.py`
- Support for:
  - Canonical JSON hashing using `json.dumps(sort_keys=True)`
  - Protobuf hashing via `message.SerializeToString()` + `hashlib.sha256`

### Steps
- Add a switch to select hash method
- Ensure consistent output regardless of field ordering

---

## Phase 3: Deduplication Interface

### `deduplicator.py`
Expose main public interface:
```python
class Deduplicator:
    def __init__(self, ttl_seconds: int, cache_backend: BaseCache):
        def is_duplicate(self, message: Any, format: str = "json") -> bool
```

### Steps
- Encapsulate cache and hasher
- Accept external cache backend (in-memory or Redis)
- Add format detection and routing
- Return True if message is duplicate; False if new and inserted

---

## Phase 4: Pluggable Cache Backend Support

### Backends
- In-memory (default)
- Redis (user provides Redis cluster endpoint during init)

### Structure
```
src/lib/cache/
  base.py
  memory.py
  redis.py
```

### Interface
```python
class BaseCache:
    def get(self, key: str) -> bool: ...
    def set(self, key: str, ttl: int) -> None: ...
```

### Steps
- Define `BaseCache` protocol
- Implement `MemoryCache` and `RedisCache`
- Redis config passed during `Deduplicator` init:
```python
deduper = Deduplicator(ttl_seconds=60, cache_backend=RedisCache(redis_url="redis://localhost:6379"))
```

---

## Phase 5: Testing Suite

### Structure
```
tests/
  test_deduplicator.py
  test_cache.py
  test_hasher.py
```

### Steps
- Unit tests for each component
- Mock time using `freezegun`
- Parametrize hash tests with json/protobuf

---

## Phase 6: Packaging & Publishing

### Steps
- Finalize `pyproject.toml`
- Add usage examples to README
- Version the release
- Publish to PyPI using `poetry publish`

---

## Sample Usage
```python
from lib import Deduplicator
from lib.cache.redis import RedisCache

cache = RedisCache(redis_url="redis://localhost:6379")
deduper = Deduplicator(ttl_seconds=60, cache_backend=cache)

if not deduper.is_duplicate(message, format="json"):
    process(message)
```

---

## TODO Notes for Windsurf Agent
- Auto-generate code stubs for each module
- Write CLI tool for manual message hash debugging
- Auto-document interfaces using `pdoc`

---

## Optional Extensions
- Sliding window metrics dashboard
- Pluggable deduplication key extraction strategy
- Type hints for message schemas
