# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv sync

# Run a meter reading (continuous loop)
uv run python main.py read water
uv run python main.py read electricity
uv run python main.py read gas
```

No test suite or linter is configured.

## Architecture

The system has three composable layers wired together in `main.py`:

**Reader** (`reader/`) — implements Python's `Iterator` protocol via `AbstractReader`. `__next__` returns the raw data for one reading. `DelayReader` is a decorator that wraps any other reader and adds a sleep between reads. `DSMRv5SerialReader` reads from a DSMR v5 smart meter over serial.

**Processor** (`processor/`) — a callable (`AbstractProcessor.__call__(data) -> None`) that receives each raw reading and does something with it (print, store, etc.). It stores metadata like `sn` (serial number) and `unit`. All current implementations return `None`.

**Meter** (`meter/`) — `AbstractMeter.__call__` drives the loop: `while self.processor(next(self.reader)): pass`. Because processors return `None` (falsy), this exits after one read. The outer `while True` in `main.py` repeatedly invokes the meter, creating a continuous reading loop.

To add a new meter type: add a new key to the `meters` dict in `main.py`, composing a reader and processor. To add a new reader, subclass `AbstractReader` and implement `__next__`. To add a new processor, subclass `AbstractProcessor` and implement `__call__`.
