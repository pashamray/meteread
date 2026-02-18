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

For testing without hardware, use the raw meter variants backed by a hardcoded DSMR v5 telegram:

```bash
uv run python main.py read raw_electricity
uv run python main.py read raw_gas
```

## Architecture

Three composable layers wired together in `main.py`:

**Reader** (`reader/`) — implements Python's `Iterator` protocol via `AbstractReader`. `__next__` returns the raw data for one reading. `DelayReader` decorates any reader with a sleep between reads. `DSMRv5SerialReader` reads from a DSMR v5 smart meter over serial. `DSMRv5RawReader` parses a raw telegram string and yields it repeatedly — useful for testing without hardware.

**Processor** (`processor/`) — a callable (`AbstractProcessor.__call__(data) -> None`) that receives each raw reading and does something with it (print, store, etc.). `ChainProcessor` composes multiple processors so they all receive the same data in sequence.

**Meter** (`meter/`) — `AbstractMeter.__call__` drives the loop: `while self.processor(next(self.reader)): pass`. Since processors return `None` (falsy), this exits after one read. The outer `while True` in `main.py` calls `meter()` repeatedly for continuous reading.

## Project Structure

```
meteread/
├── main.py
├── pyproject.toml
├── meter/
│   ├── AbstractMeter.py
│   └── GenericMeter.py
├── processor/
│   ├── AbstractProcessor.py
│   ├── ChainProcessor.py
│   ├── DSMRElectricityProcessor.py
│   ├── DSMRGasProcessor.py
│   ├── NoneProcessor.py
│   └── PassProcessor.py
├── reader/
│   ├── AbstractReader.py
│   ├── DelayReader.py
│   ├── DSMRv5RawReader.py
│   ├── DSMRv5SerialReader.py
│   ├── RandomReader.py
│   └── ZeroReader.py
└── tests/
    ├── conftest.py
    ├── test_meters.py
    ├── test_processors.py
    └── test_readers.py
```

## DSMR

Electricity and gas are both read from the same DSMR v5 P1 port. Gas is a sub-meter on the MBus channel — `DSMRGasProcessor` finds it by device type (3 = gas) in `telegram.MBUS_DEVICES`.

`DSMRElectricityProcessor` prints:
```
electricity sn=<id> t1=<kWh> t2=<kWh> now=<kW> returned=<kW>
```

`DSMRGasProcessor` prints:
```
gas sn=<id> reading=<value> <unit>
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
        print(data)
```

To run multiple processors on the same reading, use `ChainProcessor`:

```python
from processor import ChainProcessor, DSMRElectricityProcessor, DSMRGasProcessor

ChainProcessor(DSMRElectricityProcessor(), DSMRGasProcessor())
```

## Dependencies

- **dsmr-parser** — DSMR v5 protocol parsing for Dutch smart meters
- **typer** — CLI framework
- Python 3.13+
