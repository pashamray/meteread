# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run tests
uv run pytest

# Docs (live preview at http://localhost:8000)
uv run zensical serve

# Docs (build static site to site/)
uv run zensical build

# Run a single test file
uv run pytest tests/test_processors.py

# Run a meter reading (continuous loop — requires hardware or use 'raw')
uv run python main.py read electricity
uv run python main.py read gas
uv run python main.py read electricity_and_gas

# Test without hardware (replays a hardcoded DSMR v5 telegram)
uv run python main.py read raw

# Run the full stack with Docker (meteread + InfluxDB 3)
docker compose up -d
```

No linter is configured.

## Architecture

Four composable layers wired together in `main.py`:

**Reader** (`reader/`) — implements Python's `Iterator` protocol via `AbstractReader`. `__next__` returns a parsed DSMR telegram. `DelayReader` wraps any reader and sleeps between reads. `DSMRv5SerialReader` reads from a DSMR v5 P1 port over serial. `DSMRv5RawReader` parses a raw telegram string and yields it repeatedly (useful for testing without hardware).

**Processor** (`processor/`) — a callable (`AbstractProcessor.__call__(data) -> None`) that receives each telegram and does something with it. `ChainProcessor` fans one telegram out to multiple processors in sequence. DSMR processors accept an optional `storage` argument. All implementations return `None`.

**Storage** (`storage/`) — optional persistence backend passed into processors. `AbstractStorage.write(measurement, tags, fields, timestamp)` is the interface. `InfluxDBStorage` writes to InfluxDB 3; `CsvStorage` appends to a CSV file.

**Meter** (`meter/`) — `AbstractMeter.__call__` drives the loop: `while self.processor(next(self.reader)): pass`. Because processors return `None` (falsy), this exits after one read. The outer `while True` in `main.py` calls `meter()` repeatedly for continuous reading.

## Key patterns

- `load_dotenv()` is called before `app()` in `main.py`; configuration (e.g. `INFLUXDB_URL`) is read via `os.getenv`.
- The `raw` meter in `main.py` is the reference entry: it shows how `DelayReader`, `DSMRv5RawReader`, `ChainProcessor`, and `InfluxDBStorage` are composed together.
- Test fixtures live in `tests/conftest.py` and expose `raw_telegram_v5` (string) and `telegram` (parsed object) shared across all test files.
- Gas is a sub-meter on the MBus channel; `DSMRGasProcessor` identifies it by device type 3 in `telegram.MBUS_DEVICES`.
