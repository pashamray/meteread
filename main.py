import typer
from meter import WaterMeter, ElectricityMeter, GasMeter
from processor import DelayProcessor, ZeroProcessor, RandomProcessor, DSMRv5Processor

app = typer.Typer()

@app.command()
def read(name: str):
    meters = {
        'water': WaterMeter(
            name='water meter 1',
            processor=DelayProcessor(
                processor=RandomProcessor(),
                delay=5.0
            )
        ),
        'electricity': ElectricityMeter(
            name='electricity meter 1',
            processor=DSMRv5Processor(
                device='/dev/ttyUSB0'
            )
        ),
        'gas': GasMeter(
            name='gas meter 1',
            processor=DelayProcessor(
                processor=ZeroProcessor(),
                delay=5.0
            )
        ),
    }
    meter = meters.get(name)

    for value in meter:
        print(f"meter: {meter.name}, value: {value} {meter.unit}")

@app.command()
def config():
    raise NotImplementedError

if __name__ == "__main__":
    app()