"""Score tracking and rank calculation."""

from game.state import GameState
from game.display import Display

RANKS = [
    (0, "Uninitialized Tensor"),
    (21, "Partially Trained Model"),
    (41, "Fine-Tuned Apprentice"),
    (61, "Attention Head"),
    (81, "Transformer Adept"),
    (96, "Foundation Model Master"),
]

# Score values
SCORE_ROOM_VISIT = 2
SCORE_PUZZLE_SOLVE = 8
SCORE_BONUS = 3
SCORE_JOURNAL_COMPLETE = 5
SCORE_FINAL_QUESTION = 5


def get_rank(score: int) -> str:
    rank = RANKS[0][1]
    for threshold, title in RANKS:
        if score >= threshold:
            rank = title
    return rank


def award_points(state: GameState, points: int, reason: str,
                  display: Display) -> None:
    old = state.score
    state.score = min(state.score + points, state.max_score)
    gained = state.score - old
    if gained > 0:
        display.print_raw(
            display.score_text(f"  [+{gained} points: {reason}]")
        )


def display_score(state: GameState, display: Display) -> None:
    rank = get_rank(state.score)
    display.print_raw(display.separator())
    display.print(f"Score: {state.score}/{state.max_score} points")
    display.print(f"Rank: {rank}")
    display.print(f"Turns: {state.turns}")
    rooms = len(state.rooms_visited)
    display.print(f"Rooms explored: {rooms}/18")
    puzzles = sum(1 for v in state.puzzle_states.values() if v == "solved")
    display.print(f"Puzzles solved: {puzzles}/6")
    journal = len(state.journal_entries)
    display.print(f"Journal entries: {journal}/11")
