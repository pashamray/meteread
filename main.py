import typer
from meter import WaterMeter, ElectricityMeter, GasMeter

app = typer.Typer()

@app.command()
def read(name: str):
    meters = {
        'water': WaterMeter('water meter 1'),
        'electricity': ElectricityMeter('electricity meter 1'),
        'gas': GasMeter('gas meter 1'),
    }
    meter = meters.get(name)

    for value in meter:
        print(f"meter: {meter.name}, value: {value} {meter.unit}")

@app.command()
def config():
    raise NotImplementedError

if __name__ == "__main__":
    app()