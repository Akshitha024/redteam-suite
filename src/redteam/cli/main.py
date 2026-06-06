"""Typer CLI for redteam-suite."""

from __future__ import annotations

import json
from pathlib import Path

import typer
from rich.console import Console

from redteam.runner import run

app = typer.Typer(no_args_is_help=True, help="Defensive red-team prompt suite.")
console = Console()


@app.command()
def info() -> None:
    console.print("redteam-suite: see `redteam bench --help`.")


@app.command()
def bench(out_dir: Path = typer.Option(Path("runs/latest"))) -> None:
    res = run(out_dir)
    console.print_json(json.dumps({"aggregate": res["aggregate"]}, default=str))


if __name__ == "__main__":
    app()
