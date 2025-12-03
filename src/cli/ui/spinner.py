from rich.console import Console
from rich.spinner import Spinner
from contextlib import contextmanager

console = Console()

@contextmanager
def loading(text="Loading...", spinner="dots"):
    with console.status(f"[bold cyan]{text}[/]", spinner=spinner, spinner_style="magenta"):
        yield
