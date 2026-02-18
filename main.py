import typer
from meter import GenericMeter
from processor import NoneProcessor, PassProcessor
from reader import DelayReader, ZeroReader, RandomReader, DSMRv5SerialReader

app = typer.Typer()

@app.command()
def read(name: str):
    meters = {
        'water': GenericMeter(
            name='cold water',
            reader=DelayReader(
                reader=RandomReader(),
                delay=1.0
            ),
            processor=PassProcessor(
                unit='m3',
            )
        ),
        'electricity': GenericMeter(
            name='electricity meter',
            reader=DSMRv5SerialReader(
                device='/dev/ttyUSB0'
            ),
            processor=NoneProcessor()
        ),
        'gas': GenericMeter(
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
        meter()

@app.command()
def config():
    raise NotImplementedError

if __name__ == "__main__":
    app()