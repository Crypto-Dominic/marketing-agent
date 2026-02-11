"""Interactive CLI for the marketing agent."""

import sys
from pathlib import Path

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.theme import Theme

from .agent import MarketingAgent

theme = Theme({"brand": "bold cyan", "user": "bold green", "info": "dim"})
console = Console(theme=theme)


WELCOME = """\
# Brand Marketing Agent

Your **Senior Marketing Manager** is ready.

## Capabilities
- **Content creation** — blog posts, ad copy, emails, landing pages
- **Campaign planning** — objectives, channels, timeline, KPIs
- **Social media** — platform-specific calendars and draft posts
- **Analytics** — measurement frameworks and reporting structures
- **Brand governance** — every output aligned to your brand guidelines

## Commands
- Type your request in natural language
- `/reset` — clear conversation and start fresh
- `/config` — show current brand config path
- `/quit` — exit the agent

---
"""


def main():
    config_path = None
    if len(sys.argv) > 1:
        config_path = Path(sys.argv[1])

    console.print(Panel(Markdown(WELCOME), border_style="cyan", title="[brand]Marketing Agent[/brand]"))

    try:
        agent = MarketingAgent(config_path=config_path)
    except FileNotFoundError as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)

    brand_name = agent.config.get("brand", {}).get("name", "your brand")
    console.print(f"[info]Loaded brand config for[/info] [brand]{brand_name}[/brand]\n")

    while True:
        try:
            user_input = console.input("[user]You>[/user] ").strip()
        except (EOFError, KeyboardInterrupt):
            console.print("\n[info]Goodbye.[/info]")
            break

        if not user_input:
            continue

        if user_input.lower() in ("/quit", "/exit", "quit", "exit"):
            console.print("[info]Goodbye.[/info]")
            break

        if user_input.lower() == "/reset":
            agent.reset()
            console.print("[info]Conversation cleared.[/info]\n")
            continue

        if user_input.lower() == "/config":
            console.print(f"[info]Config path:[/info] {agent.config}")
            continue

        with console.status("[brand]Thinking...[/brand]", spinner="dots"):
            try:
                response = agent.chat(user_input)
            except Exception as e:
                console.print(f"[red]Error:[/red] {e}")
                continue

        console.print()
        console.print(Panel(Markdown(response), border_style="cyan", title="[brand]Marketing Agent[/brand]"))
        console.print()


if __name__ == "__main__":
    main()
