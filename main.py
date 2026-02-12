import typer
from meter import WaterMeter, ElectricityMeter, GasMeter
from reader import DelayReader, ZeroReader, RandomReader, DSMRv5Reader

app = typer.Typer()

@app.command()
def read(name: str):
    meters = {
        'water': WaterMeter(
            name='cold water',
            sn='undefined',
            reader=DelayReader(
                reader=RandomReader(),
                delay=1.0
            )
        ),
        'electricity': ElectricityMeter(
            name='electricity meter',
            sn='undefined',
            reader=DSMRv5Reader(
                device='/dev/ttyUSB0'
            )
        ),
        'gas': GasMeter(
            name='gas meter',
            sn='undefined',
            reader=DelayReader(
                reader=ZeroReader(),
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