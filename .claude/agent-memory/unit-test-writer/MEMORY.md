# Meteread Project - Testing Memory

## Project Setup
- **Language**: Python 3.14, managed with `uv`
- **Testing framework**: pytest >= 8 (in `[dependency-groups] dev`)
- **Run tests**: `uv run pytest tests/ -v`
- **Root `conftest.py`**: empty file needed so pytest adds project root to sys.path

## Package Structure
- `reader/`, `processor/`, `meter/` are top-level packages (not under `src/`)
- Imports use bare package names: `from reader import AbstractReader`

## Key Testing Patterns
- `DSMRv5SerialReader` requires hardware -- never import in tests
- `time.sleep` in DelayReader: patch target is `reader.DelayReader.sleep`
- `random.random` in RandomReader: patch target is `reader.RandomReader.random.random`
- All processors return `None` (falsy), so `AbstractMeter.__call__` while-loop exits after one iteration
- Use `MagicMock` with `__next__` for mocking readers in meter tests
