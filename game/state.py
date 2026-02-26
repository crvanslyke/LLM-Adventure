"""Single source of truth for all mutable game state."""

import json
from dataclasses import dataclass, field
from pathlib import Path

SAVE_DIR = Path.home() / ".llm_adventure"
SAVE_FILE = SAVE_DIR / "savegame.json"


@dataclass
class GameState:
    current_room: str = "lobby"
    inventory: list[str] = field(default_factory=list)
    score: int = 0
    max_score: int = 100
    turns: int = 0
    puzzle_states: dict[str, str] = field(default_factory=dict)
    # puzzle_id -> "unsolved" | "in_progress" | "solved"
    journal_entries: list[str] = field(default_factory=list)
    flags: dict[str, bool] = field(default_factory=dict)
    rooms_visited: set[str] = field(default_factory=set)
    items_in_rooms: dict[str, list[str]] = field(default_factory=dict)
    game_over: bool = False
    hint_counts: dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize state to a JSON-compatible dict."""
        return {
            "current_room": self.current_room,
            "inventory": self.inventory,
            "score": self.score,
            "max_score": self.max_score,
            "turns": self.turns,
            "puzzle_states": self.puzzle_states,
            "journal_entries": self.journal_entries,
            "flags": self.flags,
            "rooms_visited": sorted(self.rooms_visited),
            "items_in_rooms": self.items_in_rooms,
            "game_over": self.game_over,
            "hint_counts": self.hint_counts,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "GameState":
        """Deserialize state from a dict."""
        state = cls()
        state.current_room = data.get("current_room", "lobby")
        state.inventory = data.get("inventory", [])
        state.score = data.get("score", 0)
        state.max_score = data.get("max_score", 100)
        state.turns = data.get("turns", 0)
        state.puzzle_states = data.get("puzzle_states", {})
        state.journal_entries = data.get("journal_entries", [])
        state.flags = data.get("flags", {})
        state.rooms_visited = set(data.get("rooms_visited", []))
        state.items_in_rooms = data.get("items_in_rooms", {})
        state.game_over = data.get("game_over", False)
        state.hint_counts = data.get("hint_counts", {})
        return state

    def save(self, path: Path | None = None) -> Path:
        """Save game state to a JSON file."""
        path = path or SAVE_FILE
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(self.to_dict(), indent=2))
        return path

    @classmethod
    def load(cls, path: Path | None = None) -> "GameState":
        """Load game state from a JSON file."""
        path = path or SAVE_FILE
        data = json.loads(path.read_text())
        return cls.from_dict(data)
