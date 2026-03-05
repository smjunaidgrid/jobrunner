import typer
from pathlib import Path

app = typer.Typer(help="Jobrunner CLI")

cli = typer.Typer()
app.add_typer(cli)

@cli.command()
def init():
    """
    Initialized Jobrunner environment
    """

    base = Path(".jobrunner")
    logs = base / "logs"
    db = base / "jobs.db"

    base.mkdir(exist_ok=True)
    logs.mkdir(exist_ok=True)

    if not db.exists():
        db.touch()
        typer.echo("Database created")

    typer.echo("Jobrunner initialized")