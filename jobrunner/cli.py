import typer
from pathlib import Path
from jobrunner.parser import parse_pipeline
from jobrunner.database import create_tables, create_job, create_steps

app = typer.Typer(help="Jobrunner CLI")

cli = typer.Typer()
app.add_typer(cli)



@cli.command()
def init():
    """
    Initialize Jobrunner environment
    """

    base = Path(".jobrunner")
    logs = base / "logs"
    db = base / "jobs.db"

    base.mkdir(exist_ok=True)
    logs.mkdir(exist_ok=True)

    if not db.exists():
        db.touch()
        typer.echo("Database created")

    # NEW LINE
    create_tables()

    typer.echo("Jobrunner initialized")

@cli.command()
def run(pipeline_file: str):
    """
    Run a pipeline from YAML definition
    """

    pipeline = parse_pipeline(pipeline_file)

    job_id = create_job(pipeline["name"])
    create_steps(job_id, pipeline["steps"])

    typer.echo(f"Job created: {job_id}")