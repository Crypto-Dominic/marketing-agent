"""Interactive and non-interactive CLI for the marketing agent."""

import argparse
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


def _parse_args():
    parser = argparse.ArgumentParser(description="Brand Marketing Agent")
    parser.add_argument("--config", type=Path, help="Path to brand config YAML")
    parser.add_argument("--prompt", type=str, help="Run non-interactively with this prompt")
    parser.add_argument("--output", type=str, help="Save output to file (non-interactive mode)")
    return parser.parse_args()


def _run_non_interactive(args):
    """Run the agent with a single prompt and exit."""
    try:
        agent = MarketingAgent(config_path=args.config)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        response = agent.chat(args.prompt)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if args.output:
        Path(args.output).parent.mkdir(parents=True, exist_ok=True)
        Path(args.output).write_text(response)
        print(f"Output saved to {args.output}")
    else:
        print(response)


def main():
    args = _parse_args()

    if args.prompt:
        _run_non_interactive(args)
        return

    config_path = args.config

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
