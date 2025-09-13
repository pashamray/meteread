# Meteread

A Python utility for reading meter values from various types of utility meters including water, electricity, and gas meters.

## Overview

Meteread is a command-line application that provides meter readings from different utility meters. It provides a simple interface to read meter values and displays them with appropriate units. The project uses an object-oriented design with an abstract base class and specific implementations for each meter type.

## Features

- **Multiple Meter Types**: Support for water, electricity, and gas meters
- **Real-time Reading**: Reads meter values with realistic intervals
- **Iterator Pattern**: Each meter implements Python's iterator protocol for continuous reading
- **Command Line Interface**: Easy-to-use CLI built with Typer
- **Extensible Design**: Abstract base class allows for easy addition of new meter types

## Meter Types

- **Water Meter**: Measures water consumption in cubic meters (m³)
- **Electricity Meter**: Measures electrical consumption in kilowatts (kW)
- **Gas Meter**: Measures gas consumption in cubic meters (m³)

## Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd meteread
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the application using Python:

```bash
python main.py read <meter_type>
```

### Available Commands

#### Read Meter Values
```bash
python main.py read water       # Read water meter
python main.py read electricity # Read electricity meter
python main.py read gas         # Read gas meter
```

Example output:
```
...
meter: water meter 1, value: 3.45 m3
meter: water meter 1, value: 2.78 m3
meter: water meter 1, value: 4.12 m3
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
├── main.py                 # Main application entry point
├── README.md              # This file
├── requirements.txt       # Project dependencies
└── meter/                 # Meter module
    ├── __init__.py        # Module initialization
    ├── abstractmeter.py   # Abstract base class for all meters
    ├── electricitymeter.py # Electricity meter implementation
    ├── gasmeter.py        # Gas meter implementation
    └── watermeter.py      # Water meter implementation
```

## Architecture

The project follows a clean architecture pattern:

- **AbstractMeter**: Base class implementing the Iterator protocol
- **Concrete Meters**: Specific implementations for each utility type
- **CLI Interface**: Typer-based command-line interface in `main.py`

Each meter generates random values between 0-5 with appropriate units and includes a 1-second delay to provide real-world reading behavior.

## Development

### Adding New Meter Types

To add a new meter type:

1. Create a new class inheriting from `AbstractMeter`
2. Implement the `__next__()` method
3. Add the meter to the meters dictionary in `main.py`

Example:
```python
from meter.abstractmeter import AbstractMeter

class SolarMeter(AbstractMeter):
    def __init__(self, name: str, sn: str | None = None):
        super().__init__(name, 'kWh', sn)
    
    def __next__(self) -> float:
        # Implementation here
        raise StopIteration
```

## Requirements

- Python 3.9+
- typer