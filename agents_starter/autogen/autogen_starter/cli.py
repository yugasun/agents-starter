#!/usr/bin/env python
import asyncio
import click

from . import examples


@click.group()
def cli():
    """Examples runner."""
    pass


@cli.command("run")
@click.argument("example_name", default="quickstart")
def run_example(example_name):
    """Run a specific example by name.

    Example:
        $ arun run quickstart
    """
    click.echo(f"Running example: {example_name}")

    run_func = getattr(examples, example_name, None)
    if run_func and callable(run_func):
        click.echo(f"Found example function: {run_func.__name__}")
        # Properly handle async function
        if asyncio.iscoroutinefunction(run_func):
            asyncio.run(run_func())
        else:
            run_func()
    else:
        click.echo(f"Example function '{example_name}' not found.")
        click.echo("Available examples:")
        for name in dir(examples):
            if not name.startswith("_") and callable(getattr(examples, name)):
                click.echo(f"  - {name}")


@cli.command("list")
def list_examples():
    """List all available examples."""
    click.echo("Available examples:")
    for name in dir(examples):
        if not name.startswith("_") and callable(getattr(examples, name)):
            click.echo(f"  - {name}")


def run():
    """Entry point function."""
    cli()


if __name__ == "__main__":
    run()
