"""Puzzle 1: The Tokenizer's Challenge -- teach tokenization/BPE."""

from puzzles.base import Puzzle
from game.state import GameState
from game.display import Display


class TokenizerPuzzle(Puzzle):
    puzzle_id = "tokenizer"

    def can_start(self, state: GameState) -> bool:
        return "raw_prompt_fragment" in state.inventory

    def start(self, state: GameState, display: Display) -> str:
        state.puzzle_states["tokenizer"] = "in_progress"
        state.flags["tokenizer_started"] = True
        return (
            "You place the raw prompt fragment on the workbench. The word "
            "'unbelievable' glows on the chopping block.\n\n"
            "The Tokenizer Gnome grins. 'Now then! Split this into tokens "
            "the way I would. Choose the correct tokenization:'\n\n"
            "  A) 'u' 'n' 'b' 'e' 'l' 'i' 'e' 'v' 'a' 'b' 'l' 'e'\n"
            "     (character-level -- one letter per token)\n\n"
            "  B) 'un' 'believ' 'able'\n"
            "     (subword tokenization -- meaningful pieces)\n\n"
            "  C) 'unbelievable'\n"
            "     (whole word -- one token for the entire word)\n\n"
            "  D) 'un' 'believe' 'able'\n"
            "     (morphological -- by English morphemes)\n\n"
            "Type 'choose' followed by A, B, C, or D."
        )

    def handle_input(self, raw: str, state: GameState,
                      display: Display) -> str | None:
        if state.puzzle_states.get("tokenizer") != "in_progress":
            return None

        raw = raw.strip().lower()

        # Handle "choose X" or bare "X"
        choice = None
        if raw.startswith("choose "):
            choice = raw[7:].strip()
        elif raw in ("a", "b", "c", "d"):
            choice = raw

        if choice is None:
            return None

        if choice == "b":
            state.puzzle_states["tokenizer"] = "solved"
            state.flags["tokenizer_puzzle_solved"] = True
            # Consume the prompt fragment
            if "raw_prompt_fragment" in state.inventory:
                state.inventory.remove("raw_prompt_fragment")

            return (
                "The Gnome's eyes widen. 'CORRECT! Subword tokenization! "
                "Not characters, not whole words, but meaningful subword "
                "pieces. The BPE algorithm finds the most efficient split.'\n\n"
                "He demonstrates with another word: 'ChatGPT' becomes "
                "'Chat' + 'G' + 'PT'. 'See? Proper nouns get unusual "
                "splits because they're rare in the training data. Common "
                "words like \"the\" stay whole, but longer words get "
                "chopped into reusable pieces.'\n\n"
                "The Gnome hands you his spare cleaver. 'Take this token "
                "cleaver. You've earned it.'\n\n"
                "The path south to Embedding Space is now open."
            )
        elif choice == "a":
            return (
                "The Gnome shakes his head. 'Character-level?! Far too "
                "many tokens! A sentence would be hundreds of tokens long. "
                "Modern LLMs use SUBWORD tokenization -- pieces bigger "
                "than characters but sometimes smaller than words. Try "
                "again!'"
            )
        elif choice == "c":
            return (
                "The Gnome scoffs. 'One token for the whole word? My "
                "vocabulary would need millions of entries! And what about "
                "new words I've never seen? No, I use SUBWORD pieces that "
                "can combine to form any word. Try again!'"
            )
        elif choice == "d":
            return (
                "The Gnome tilts his head. 'Close! But I don't follow "
                "English morphology rules. I use statistical patterns -- "
                "Byte-Pair Encoding -- which finds the most common "
                "substrings in the training data. \"believ\" is more "
                "statistically common as a chunk than \"believe\" in my "
                "tokenizer. Try again!'"
            )
        else:
            return "The Gnome taps his foot. 'A, B, C, or D. Choose wisely!'"

    def is_solved(self, state: GameState) -> bool:
        return state.puzzle_states.get("tokenizer") == "solved"

    def get_hint(self, state: GameState) -> str:
        if "raw_prompt_fragment" not in state.inventory:
            return (
                "The Gnome wants to test you, but you need something to "
                "tokenize. Have you found a raw prompt fragment in the "
                "Input Buffer?"
            )
        if not state.flags.get("tokenizer_started"):
            return (
                "Try using the raw prompt fragment on the workbench. "
                "Type 'use raw_prompt_fragment on workbench'."
            )
        return (
            "Think about how LLMs actually split text. It's not by "
            "individual characters (too many tokens), not by whole words "
            "(vocabulary too large), but by something in between..."
        )
