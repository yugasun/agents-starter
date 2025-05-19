import asyncio
from typing import Optional
from agents import set_tracing_disabled
import typer

from .. import examples

app = typer.Typer()

set_tracing_disabled(True)  # Enable tracing for the CLI


# 获取命令航参数 --example/-e 来确定执行哪个函数
@app.command(
    help="Run the example function.",
)
def run_example(
    framework: Optional[str] = "autogen", example: Optional[str] = "quickstart"
):
    """
    Run the example function.
    """
    fw_examples = None
    run_func = None
    if framework and example:
        typer.echo(f"Example: {example}")
        fw_examples = getattr(examples, f"{framework}_examples", None)

        if fw_examples:
            run_func = getattr(fw_examples, example, None)
            if run_func:
                typer.echo(f"Found example function: {run_func.__name__}")
                asyncio.run(run_func())
            else:
                typer.echo(
                    f"Example function '{example}' not found in framework '{framework}'."
                )
        else:
            typer.echo(
                f"Framework '{framework}' not found. Available frameworks: {', '.join(examples.__all__)}"
            )

    else:
        typer.echo(
            "Please provide a framework and an example function to run. Use --help for more information."
        )


def run():
    app()


if __name__ == "__main__":
    run()
