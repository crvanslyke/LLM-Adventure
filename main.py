#!/usr/bin/env python3
"""LLM Adventure: A text-based adventure game about Large Language Models."""

import sys
from game.engine import GameEngine


def main() -> None:
    debug = "--debug" in sys.argv
    no_color = "--no-color" in sys.argv
    engine = GameEngine(debug=debug, use_color=not no_color)
    engine.run()


if __name__ == "__main__":
    main()
