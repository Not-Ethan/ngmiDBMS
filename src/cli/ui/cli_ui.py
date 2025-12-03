from rich.console import Console
from rich.text import Text
from rich.panel import Panel

console = Console()

class UI:
    @staticmethod
    def banner():
        banner_text = Text("""
███╗   ██╗  ██████╗  ███╗   ███╗ ██╗
████╗  ██║ ██╔═══██╗ ████╗ ████║ ██║
██╔██╗ ██║ ██║       ██╔████╔██║ ██║
██║╚██╗██║ ██║ ████║ ██║╚██╔╝██║ ██║
██║ ╚████║ ██║   ██║ ██║ ╚═╝ ██║ ██║
██║  ╚███║ ██║   ██║ ██║     ██║ ██║
██║   ╚██║ ╚██████╔╝ ██║     ██║ ██║
╚═╝    ╚═╝  ╚═════╝  ╚═╝     ╚═╝ ╚═╝
""", style="bold magenta")

        subtitle = Text("ngmiDBMS — Not Gonna Make It Database System", style="bold white")

        console.print(banner_text)
        console.print(subtitle)
        console.print("\n")

    @staticmethod
    def success(msg: str):
        console.print(f"[bold green]✔ {msg}[/]")

    @staticmethod
    def error(msg: str):
        console.print(f"[bold red]✘ {msg}[/]")

    @staticmethod
    def info(msg: str):
        console.print(f"[bold cyan]➤ {msg}[/]")

    @staticmethod
    def section(title: str):
        console.print(Panel.fit(title, border_style="magenta", style="white bold"), "")

    @staticmethod
    def prompt(label: str) -> str:
        from rich.prompt import Prompt
        return Prompt.ask(f"[bold magenta]{label}[/]")

    @staticmethod
    def panel(title: str, body: str):
        console.print(Panel(body, title=title, border_style="magenta"))


    @staticmethod
    def warning(msg: str):
        console.print(f"[bold yellow]⚠ {msg}[/]")

    @staticmethod
    def status_panel(title: str, items: dict):
        """Display system status in a formatted panel"""
        content = ""
        for key, (status, style) in items.items():
            content += f"[bold white]{key}:[/] [{style}]{status}[/]\n"
        
        console.print(Panel(content.strip(), title=title, border_style="cyan"))

    @staticmethod
    def connection_retry(attempt: int, max_attempts: int):
        console.print(f"[yellow]Retrying connection... ({attempt}/{max_attempts})[/]")

