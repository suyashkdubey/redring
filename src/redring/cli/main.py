import typer
from redring.engine.engine import Engine
from redring.renderers.cli import CLIRenderer
from redring.core.logging import configure_logging
import redring.scanners #This registers the modules so dont remove this line!

logger = configure_logging()

app = typer.Typer(
    name="RedRing",
    help="AI-powered diagnostic engine for developer environments."
)

@app.command()
def diagnose(stack:str = typer.Argument(
    ...,
    help="Technology stack to diagnose (python, docker, git, etc.)"
    )):
    """
    Diagnose issues for a specific technology stack.
    """
    logger.info("Diagnose command started | stack=%s", stack)
    try:
        engine = Engine()
        result = engine.run(stack)
        logger.debug("Engine returned %d scan results", len(result))
        renderer = CLIRenderer()
        logger.debug("Rendering scan results")
        renderer.render(result)
        logger.debug("Rendering completed")
        logger.info("Diagnose command completed | stack=%s", stack)
    except Exception:
        logger.exception("Diagnose command failed | stack=%s", stack)
        typer.echo("❌ Redring encountered an unexpected error.")
        typer.echo("Check the log file for details.")

@app.command()
def version():
    print("v0.2.0-alpha.2")

if __name__ == "__main__":
    app()