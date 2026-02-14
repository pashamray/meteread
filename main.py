import typer
from meter import WaterMeter, ElectricityMeter, GasMeter
from processor import NoneProcessor
from reader import DelayReader, ZeroReader, RandomReader, DSMRv5Reader

app = typer.Typer()

@app.command()
def read(name: str):
    meters = {
        'water': WaterMeter(
            name='cold water',
            reader=DelayReader(
                reader=RandomReader(),
                delay=1.0
            ),
            processor=NoneProcessor()
        ),
        'electricity': ElectricityMeter(
            name='electricity meter',
            reader=DSMRv5Reader(
                device='/dev/ttyUSB0'
            ),
            processor=NoneProcessor()
        ),
        'gas': GasMeter(
            name='gas meter',
            reader=DelayReader(
                reader=ZeroReader(),
                delay=1.0
            ),
            processor=NoneProcessor()
        ),
    }
    meter = meters.get(name)

    while True:
        for value in meter():
            print(f"meter: {meter.name}, value: {value['value']} {value['unit']}")

@app.command()
def config():
    raise NotImplementedError

if __name__ == "__main__":
    app()