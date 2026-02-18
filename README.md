# Meteread

A Python utility for reading utility meter values (water, electricity, gas) with a composable reader/processor architecture.

## Installation

```bash
git clone https://github.com/pashamray/meteread.git
cd meteread
uv sync
```

## Usage

```bash
uv run python main.py read water
uv run python main.py read electricity
uv run python main.py read gas
```

## Architecture

Three composable layers wired together in `main.py`:

**Reader** (`reader/`) — implements Python's `Iterator` protocol via `AbstractReader`. `__next__` returns the raw data for one reading. `DelayReader` decorates any reader with a sleep between reads. `DSMRv5SerialReader` reads from a DSMR v5 smart meter over serial.

**Processor** (`processor/`) — a callable (`AbstractProcessor.__call__(data) -> None`) that receives each raw reading. Stores metadata like `sn` (serial number) and `unit`.

**Meter** (`meter/`) — `AbstractMeter.__call__` drives the loop: `while self.processor(next(self.reader)): pass`. Since processors return `None` (falsy), this exits after one read. The outer `while True` in `main.py` calls `meter()` repeatedly for continuous reading.

## Project Structure

```
meteread/
├── main.py
├── pyproject.toml
├── conftest.py
├── meter/
│   ├── AbstractMeter.py
│   └── GenericMeter.py
├── processor/
│   ├── AbstractProcessor.py
│   ├── NoneProcessor.py
│   └── PassProcessor.py
├── reader/
│   ├── AbstractReader.py
│   ├── DelayReader.py
│   ├── DSMRv5SerialReader.py
│   ├── RandomReader.py
│   └── ZeroReader.py
└── tests/
    ├── test_readers.py
    ├── test_processors.py
    └── test_meters.py
```

## Testing

```bash
uv run pytest
```

## Extending

To add a new meter type: add a key to the `meters` dict in `main.py`, composing a reader and processor.

To add a new reader, subclass `AbstractReader` and implement `__next__`:

```python
from reader import AbstractReader

class MyReader(AbstractReader):
    def __next__(self):
        return 42.0
```

To add a new processor, subclass `AbstractProcessor` and implement `__call__`:

```python
from processor import AbstractProcessor

class MyProcessor(AbstractProcessor):
    def __call__(self, data) -> None:
        print(f"{data} {self.unit}")
```

## Dependencies

- **dsmr-parser** — DSMR v5 protocol parsing for Dutch smart meters
- **typer** — CLI framework
- Python 3.13+
