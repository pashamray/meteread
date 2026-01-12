import typer
from meter import WaterMeter, ElectricityMeter, GasMeter
from processor import DelayProcessor, ZeroProcessor, RandomProcessor, DSMRv5ReadProcessor

app = typer.Typer()

@app.command()
def read(name: str):
    meters = {
        'water': WaterMeter(
            name='cold water',
            processor=DelayProcessor(
                processor=RandomProcessor(),
                delay=1.0
            )
        ),
        'electricity': ElectricityMeter(
            name='electricity meter',
            processor=DSMRv5ReadProcessor(
                device='/dev/ttyUSB0'
            )
        ),
        'gas': GasMeter(
            name='gas meter',
            processor=DelayProcessor(
                processor=ZeroProcessor(),
                delay=1.0
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