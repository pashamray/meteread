import typer

app = typer.Typer()

@app.command()
def read(name: str):
    print(f"Reading {name}")

@app.command()
def config():
    raise NotImplementedError

if __name__ == "__main__":
    app()