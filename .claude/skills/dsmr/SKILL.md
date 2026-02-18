---
name: dsmr
description: Implement or modify DSMR-related functionality in this project — processors, readers, or debugging. Use when the task involves DSMR telegram data, the DSMRv5SerialReader, or adding electricity meter processing.
argument-hint: [task description]
allowed-tools: Read, Grep, Glob, Bash, Edit, Write
---

# DSMR Skill

You are helping with DSMR (Dutch Smart Meter Requirements) v5 functionality in the meteread project.

## Context

The project uses the `dsmr-parser` library. The `DSMRv5SerialReader` wraps `dsmr_parser.clients.SerialReader` and yields parsed `Telegram` objects via `read_as_object()`.

## V5 Telegram attributes (electricity)

Electricity fields are direct attributes on the `Telegram` object:

```python
telegram.EQUIPMENT_IDENTIFIER        # electricity meter serial number (str)
telegram.ELECTRICITY_USED_TARIFF_1   # cumulative consumption tariff 1 (kWh)
telegram.ELECTRICITY_USED_TARIFF_2   # cumulative consumption tariff 2 (kWh)
telegram.ELECTRICITY_DELIVERED_TARIFF_1  # cumulative return-to-grid tariff 1 (kWh)
telegram.ELECTRICITY_DELIVERED_TARIFF_2  # cumulative return-to-grid tariff 2 (kWh)
telegram.CURRENT_ELECTRICITY_USAGE   # current power consumption (kW)
telegram.CURRENT_ELECTRICITY_DELIVERY  # current power return to grid (kW)
```

Each is a `CosemObject` with `.value` and `.unit` properties.

## V5 Telegram attributes (gas and other sub-meters)

In V5, sub-meters (gas, water) are MBus devices. They are **not** direct telegram attributes — they are grouped under `telegram.MBUS_DEVICES`, a list of `MbusDevice` objects.

```python
for device in telegram.MBUS_DEVICES:
    device.MBUS_DEVICE_TYPE.value        # int: 3=gas, 7=water
    device.MBUS_EQUIPMENT_IDENTIFIER.value  # serial number (str)
    device.MBUS_METER_READING.value      # reading (Decimal)
    device.MBUS_METER_READING.unit       # unit string, e.g. 'm3'
    device.MBUS_METER_READING.datetime   # timestamp of reading
```

`MBUS_DEVICES` is only set if the telegram contains MBus lines. Use `hasattr(telegram, 'MBUS_DEVICES')` to guard.

> **Wrong names from older docs** — do NOT use: `MSN_ELECTRICITY`, `MSN_GAS`, `ELECTRICITY_CURRENTLY_DELIVERED`, `ELECTRICITY_CURRENTLY_RETURNED`, `GAS_METER_READING`, `HOURLY_GAS_METER_READING`. These do not exist on V5 telegrams.

## Readers

- `DSMRv5SerialReader(device)` — reads from a physical P1 port, yields `Telegram` objects indefinitely.
- `DSMRv5RawReader(raw)` — parses a raw telegram string once (checksum validation disabled), yields the same `Telegram` indefinitely. Use for testing without hardware.

```python
DSMRv5RawReader(
    raw=(
        '/ISk5\\2MT382-1000\r\n'
        '\r\n'
        '5-3:0.2.8(50)\r\n'
        '0-0:1.0.0(210101000000W)\r\n'
        '0-0:96.1.1(4530303334303034363639353537343136)\r\n'
        '1-0:1.8.1(001234.567*kWh)\r\n'
        '1-0:1.8.2(002345.678*kWh)\r\n'
        '1-0:2.8.1(000001.000*kWh)\r\n'
        '1-0:2.8.2(000002.000*kWh)\r\n'
        '0-0:96.14.0(0002)\r\n'
        '1-0:1.7.0(01.500*kW)\r\n'
        '1-0:2.7.0(00.000*kW)\r\n'
        '0-0:96.7.21(00000)\r\n'
        '0-0:96.7.9(00000)\r\n'
        '1-0:32.32.0(00000)\r\n'
        '1-0:52.32.0(00000)\r\n'
        '1-0:72.32.0(00000)\r\n'
        '1-0:32.36.0(00000)\r\n'
        '1-0:52.36.0(00000)\r\n'
        '1-0:72.36.0(00000)\r\n'
        '1-0:32.7.0(230.1*V)\r\n'
        '1-0:52.7.0(230.2*V)\r\n'
        '1-0:72.7.0(230.0*V)\r\n'
        '1-0:31.7.0(001*A)\r\n'
        '1-0:51.7.0(002*A)\r\n'
        '1-0:71.7.0(003*A)\r\n'
        '1-0:21.7.0(00.500*kW)\r\n'
        '1-0:41.7.0(00.500*kW)\r\n'
        '1-0:61.7.0(00.500*kW)\r\n'
        '1-0:22.7.0(00.000*kW)\r\n'
        '1-0:42.7.0(00.000*kW)\r\n'
        '1-0:62.7.0(00.000*kW)\r\n'
        '0-1:24.1.0(003)\r\n'
        '0-1:96.1.0(4730303233353631323930333635383137)\r\n'
        '0-1:24.2.1(210101120000W)(01234.567*m3)\r\n'
        '!0000\r\n'
    )
)
```

## Project wiring

Meters are defined in `main.py`:

```python
'electricity': GenericMeter(
    name='electricity meter',
    reader=DSMRv5SerialReader(device='/dev/ttyUSB0'),
    processor=DSMRElectricityProcessor()
),
'gas': GenericMeter(
    name='gas meter',
    reader=DSMRv5SerialReader(device='/dev/ttyUSB0'),
    processor=DSMRGasProcessor()
),
'raw': GenericMeter(
    name='raw meter',
    reader=DSMRv5RawReader(raw=...),
    processor=DSMRElectricityProcessor()
),
```

Both electricity and gas are read from the same P1 port — they come from the same telegram. Gas and water are sub-meters accessed via `MBUS_DEVICES`.

## Task: $ARGUMENTS

## Steps

1. Read the relevant source files before making changes.
2. If adding a processor: subclass `AbstractProcessor`, implement `__call__(self, data) -> None`, add it to `processor/__init__.py`, and wire it in `main.py`.
3. If modifying a reader: subclass `AbstractReader`, implement `__next__`, add it to `reader/__init__.py`.
4. Keep processors focused — one responsibility per class.
5. After changes, run `uv run pytest` to verify nothing is broken.

## Notes

- `TelegramParser` accepts `apply_checksum_validation=False` — use this when parsing raw strings that lack a valid CRC.
- The power failure log line (`1-0:99.97.0`) can cause `ParseError` with certain formats; the parser logs a warning and continues — this is not fatal.
- `MBUS_DEVICES` is absent from the telegram if no sub-meter lines are present. Always guard with `hasattr`.
