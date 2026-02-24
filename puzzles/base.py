"""Abstract base class for all puzzles."""

from abc import ABC, abstractmethod
from game.state import GameState
from game.display import Display


class Puzzle(ABC):
    """Base class for puzzle implementations."""

    puzzle_id: str = ""

    @abstractmethod
    def can_start(self, state: GameState) -> bool:
        """Check if prerequisites are met to begin the puzzle."""
        ...

    @abstractmethod
    def start(self, state: GameState, display: Display) -> str:
        """Start the puzzle and return initial prompt text."""
        ...

    @abstractmethod
    def handle_input(self, raw: str, state: GameState,
                      display: Display) -> str | None:
        """Process puzzle-specific input. Returns output text or None
        if the input wasn't puzzle-related."""
        ...

    @abstractmethod
    def is_solved(self, state: GameState) -> bool:
        """Check if the puzzle has been solved."""
        ...

    def get_hint(self, state: GameState) -> str:
        """Return a context-sensitive hint."""
        return "Look around carefully and examine everything."
