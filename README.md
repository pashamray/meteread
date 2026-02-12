# Meteread

A Python utility for reading meter values from various types of utility meters including water, electricity, and gas meters with configurable data readers.

## Overview

Meteread is a command-line application that provides meter readings from different utility meters. It features a modular architecture with separate meter types and data readers, allowing for flexible configuration of how meter data is read and processed. The project uses an object-oriented design with abstract base classes for both meters and readers.

### Screenshot
![screenshot](doc/screenshot.png)

## Features

- **Multiple Meter Types**: Support for water, electricity, and gas meters
- **Modular Reader Architecture**: Configurable data readers for different reading behaviors
- **DSMR Support**: Real electricity meter reading via DSMR protocol
- **Delay and Random Readers**: Simulated readings with configurable delays
- **Iterator Pattern**: Each meter implements Python's iterator protocol for continuous reading
- **Command Line Interface**: Easy-to-use CLI built with Typer
- **Extensible Design**: Abstract base classes allow for easy addition of new meter types and readers

## Meter Types

- **Water Meter**: Measures water consumption in cubic meters (m³)
- **Electricity Meter**: Measures electrical consumption (kw/h)
- **Gas Meter**: Measures gas consumption in cubic meters (m³)

## Reader Types

- **RandomReader**: Generates random values for testing and simulation
- **ZeroReader**: Returns zero values (useful for testing)
- **DelayReader**: Wraps another reader and adds configurable delays
- **DSMRv5Reader**: Reads real electricity data from DSMR-compatible smart meters

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/pashamray/meteread.git
    cd meteread
    ```

2. Install using uv (recommended):
    ```bash
    uv install
    ```

   Or using pip:
    ```bash
    pip install -e .
    ```

## Usage

Run the application using Python:

```bash
python main.py read <meter_type>
```

### Available Commands

#### Read Meter Values
```bash
python main.py read water       # Read water meter (random values with 1s delay)
python main.py read electricity # Read electricity meter (DSMR from /dev/ttyUSB0)
python main.py read gas         # Read gas meter (zero values with 1s delay)
```

Example output:
```
meter: cold water, value: 3.45 m³
meter: cold water, value: 2.78 m³
meter: cold water, value: 4.12 m³
...
```

#### Configuration (Coming Soon)
```bash
python main.py config
```
*Note: Configuration command is not yet implemented*

## Project Structure

```
meteread/
├── main.py                    # Main application entry point
├── README.md                  # This file
├── pyproject.toml            # Project configuration and dependencies
├── uv.lock                   # Lock file for uv package manager
├── meter/                    # Meter module
│   ├── __init__.py           # Module initialization
│   ├── AbstractMeter.py      # Abstract base class for all meters
│   ├── ElectricityMeter.py   # Electricity meter implementation
│   ├── GasMeter.py           # Gas meter implementation
│   └── WaterMeter.py         # Water meter implementation
└── reader/                   # Reader module
    ├── __init__.py           # Module initialization
    ├── AbstractReader.py     # Abstract base class for all readers
    ├── DelayReader.py        # Adds delays to reader output
    ├── DSMRv5Reader.py       # DSMR protocol reader for smart meters
    ├── RandomReader.py       # Random value generator reader
    └── ZeroReader.py         # Zero value reader
```

## Architecture

The project follows a clean architecture pattern with two main abstractions:

### Meters
- **AbstractMeter**: Base class implementing the Iterator protocol
- **Concrete Meters**: Specific implementations for each utility type (Water, Electricity, Gas)

### Readers
- **AbstractReader**: Base class for data reading strategies
- **Concrete Readers**: Different implementations for various data sources and behaviors

Each meter is configured with a reader that determines how the data is generated or read. This allows for flexible combinations like:
- Water meter with random data and delays for simulation
- Electricity meter with real DSMR data from smart meters
- Gas meter with zero values for testing

## Dependencies

- **typer**: Command-line interface framework
- **dsmr-parser**: DSMR protocol parsing for Dutch smart meters
- **Python 3.13+**: Required Python version

## Development

### Adding New Meter Types

1. Create a new class inheriting from `AbstractMeter`
2. Implement the required properties (`name`, `unit`)
3. Configure with the appropriate reader in `main.py`

### Adding New Readers

1. Create a new class inheriting from `AbstractReader`
2. Implement the `__next__()` method to return float values
3. Add any required initialization parameters

### Example: Custom Reader

```python
from reader.AbstractReader import AbstractReader

class CustomReader(AbstractReader):
    def __init__(self, custom_param):
        self.custom_param = custom_param

    def __next__(self) -> float:
        # Your custom logic here
        return 1.0 # sample value
```

## License

See LICENSE file for details.

