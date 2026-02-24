"""Single source of truth for all mutable game state."""

from dataclasses import dataclass, field


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
