import logging
import typer

#from engineer.ai.step import CodeStep

app = typer.Typer()

@app.command()
def create(
    project_title: str = typer.Argument("example", help="project title"),
    project_workspace: str = typer.Argument("projects", help="project workspace"),
    model: str = typer.Argument("gpt-4", help="model id string"),
    temperature: float = 0.1,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

@app.command()
def understand(
    github_url: str = typer.Argument("https://github.com/yantao0527/demo-engineer.git", help="Github project URL"),
    temp_workspace: str = typer.Argument("/tmp/projects", help="Workspace that github clone to"),
    model: str = typer.Argument("gpt-4", help="model id name"),
    temperature: float = 0.1,
    verbose: bool = typer.Option(False, "--verbose", "-v"),
):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO)

if __name__ == "__main__":
    app()

