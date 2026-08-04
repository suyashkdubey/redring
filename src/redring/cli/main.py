import typer
from redring.engine.engine import Engine
from redring.renderers.cli import CLIRenderer
import redring.scanners 

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
    engine = Engine()
    result = engine.run(stack)
    renderer = CLIRenderer()
    rendered_text = renderer.render(result)
    print(rendered_text)

@app.command()
def version():
    print("v0.1.0")

if __name__ == "__main__":
    app()