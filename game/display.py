"""Text output formatting with optional ANSI color."""

import textwrap

WIDTH = 78

# ANSI color codes
COLORS = {
    "bold": "\033[1m",
    "dim": "\033[2m",
    "room": "\033[1;37m",      # bold white
    "item": "\033[33m",        # yellow
    "npc": "\033[36m",         # cyan
    "puzzle": "\033[32m",      # green
    "error": "\033[31m",       # red
    "journal": "\033[35m",     # magenta
    "score": "\033[34m",       # blue
    "reset": "\033[0m",
}


class Display:
    def __init__(self, use_color: bool = True) -> None:
        self.use_color = use_color

    def color(self, text: str, style: str) -> str:
        if not self.use_color or style not in COLORS:
            return text
        return f"{COLORS[style]}{text}{COLORS['reset']}"

    def wrap(self, text: str) -> str:
        paragraphs = text.split("\n\n")
        wrapped = []
        for para in paragraphs:
            lines = para.strip().split("\n")
            for line in lines:
                stripped = line.strip()
                if not stripped:
                    continue
                # Preserve lines that look like menu options or indented content
                if stripped.startswith(("  ", "> ", "A)", "B)", "C)", "D)",
                                       "1)", "2)", "3)", "4)", "5)")):
                    wrapped.append(stripped)
                else:
                    wrapped.append(textwrap.fill(stripped, width=WIDTH))
            wrapped.append("")
        return "\n".join(wrapped).rstrip()

    def header(self, text: str) -> str:
        line = "=" * WIDTH
        colored = self.color(text, "room")
        return f"\n{line}\n  {colored}\n{line}"

    def separator(self) -> str:
        return "-" * WIDTH

    def room_name(self, name: str) -> str:
        return self.color(name, "room")

    def item_name(self, name: str) -> str:
        return self.color(name, "item")

    def npc_speech(self, text: str) -> str:
        return self.color(text, "npc")

    def puzzle_text(self, text: str) -> str:
        return self.color(text, "puzzle")

    def error_text(self, text: str) -> str:
        return self.color(text, "error")

    def journal_text(self, text: str) -> str:
        return self.color(text, "journal")

    def score_text(self, text: str) -> str:
        return self.color(text, "score")

    def print(self, text: str, style: str | None = None) -> None:
        wrapped = self.wrap(text)
        if style:
            wrapped = self.color(wrapped, style)
        print(wrapped)

    def print_raw(self, text: str, style: str | None = None) -> None:
        """Print without wrapping."""
        if style:
            text = self.color(text, style)
        print(text)
