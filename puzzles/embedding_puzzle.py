"""Puzzle 2: The Embedding Navigator -- teach word embeddings."""

from puzzles.base import Puzzle
from game.state import GameState
from game.display import Display


class EmbeddingPuzzle(Puzzle):
    puzzle_id = "embedding"

    def _get_step(self, state: GameState) -> int:
        return state.flags.get("embedding_step", 0)

    def _set_step(self, state: GameState, step: int) -> None:
        state.flags["embedding_step"] = step

    def can_start(self, state: GameState) -> bool:
        return True

    def start(self, state: GameState, display: Display) -> str:
        state.puzzle_states["embedding"] = "in_progress"
        self._set_step(state, 1)
        return (
            "The navigation console hums to life.\n\n"
            "EMBEDDING NAVIGATION SYSTEM v2.0\n"
            "To chart a course through embedding space, demonstrate your\n"
            "understanding of semantic relationships.\n\n"
            "Challenge 1 of 3:\n"
            "  The classic analogy: 'king' is to 'queen' as 'man' is to ___?\n\n"
            "  Type your answer (a single word)."
        )

    def handle_input(self, raw: str, state: GameState,
                      display: Display) -> str | None:
        if state.puzzle_states.get("embedding") != "in_progress":
            return None

        raw = raw.strip().lower()

        # Allow "choose X" or bare answer
        if raw.startswith("choose "):
            raw = raw[7:].strip()

        step = self._get_step(state)

        if step == 1:
            if raw == "woman":
                self._set_step(state, 2)
                return (
                    "CORRECT! In embedding space, the vector relationship\n"
                    "king - man + woman ≈ queen. This famous result shows\n"
                    "that embeddings capture meaningful semantic relationships.\n\n"
                    "Challenge 2 of 3:\n"
                    "  Which word is CLOSEST to 'python' in a programming\n"
                    "  context?\n\n"
                    "  A) snake    B) java    C) elephant    D) river\n\n"
                    "  Type 'choose' followed by A, B, C, or D."
                )
            else:
                return (
                    "Not quite. Think about the relationship: 'king' is the\n"
                    "male version of 'queen'. So 'man' is the male version\n"
                    "of...? (Type a single word.)"
                )

        elif step == 2:
            choice = raw
            if choice == "b" or choice == "java":
                self._set_step(state, 3)
                return (
                    "CORRECT! In the programming context, 'python' and 'java'\n"
                    "are nearest neighbors -- both are programming languages.\n"
                    "'Snake' would be close in a zoological context, which\n"
                    "shows that embeddings can capture multiple meanings.\n\n"
                    "Challenge 3 of 3:\n"
                    "  Which word is the ODD ONE OUT? (Furthest away in\n"
                    "  embedding space from the others.)\n\n"
                    "  'happy', 'joyful', 'elated', 'refrigerator', 'cheerful'\n\n"
                    "  Type the odd word."
                )
            elif choice in ("a", "snake"):
                return (
                    "Close, but think about CONTEXT. In programming-related\n"
                    "text, which word appears in similar contexts to 'python'?\n"
                    "The key insight: embeddings cluster words that appear in\n"
                    "similar contexts. Try again!"
                )
            elif choice in ("c", "elephant", "d", "river"):
                return (
                    "Not quite. Think about what words appear in similar\n"
                    "contexts to 'python' when discussing programming.\n"
                    "Another programming language would be closest. Try again!"
                )
            else:
                return "Please choose A, B, C, or D."

        elif step == 3:
            if raw == "refrigerator":
                state.puzzle_states["embedding"] = "solved"
                state.flags["embedding_puzzle_solved"] = True
                return (
                    "CORRECT! 'Refrigerator' is the clear outlier. The other\n"
                    "four words -- happy, joyful, elated, cheerful -- all\n"
                    "cluster tightly in the 'positive emotions' region of\n"
                    "embedding space. 'Refrigerator' lives way over in the\n"
                    "'kitchen appliances' neighborhood.\n\n"
                    "The Embedding Compass materializes on the console. It\n"
                    "spins through 768 dimensions before settling on a\n"
                    "heading.\n\n"
                    "The platform glides south toward the Attention Nexus.\n"
                    "The path south is now open."
                )
            else:
                return (
                    "Not quite. Four of those words are synonyms for the\n"
                    "same emotion. One of them is... not like the others.\n"
                    "Which word has nothing to do with feelings?"
                )

        return None

    def is_solved(self, state: GameState) -> bool:
        return state.puzzle_states.get("embedding") == "solved"

    def get_hint(self, state: GameState) -> str:
        step = self._get_step(state)
        if step == 0:
            return "Use the navigation console to begin the embedding challenge."
        elif step == 1:
            return "King is to queen as man is to ___? Think gender pairs."
        elif step == 2:
            return "In programming contexts, which language is most similar to Python?"
        else:
            return "Four words mean the same thing. One is a kitchen appliance."
