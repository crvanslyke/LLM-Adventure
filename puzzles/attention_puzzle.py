"""Puzzle 3: Assembling the Attention Mechanism -- teach Q/K/V attention."""

from puzzles.base import Puzzle
from game.state import GameState
from game.display import Display


class AttentionPuzzle(Puzzle):
    puzzle_id = "attention"

    def can_start(self, state: GameState) -> bool:
        return all(
            item in state.inventory
            for item in ("query_crystal", "key_crystal", "value_crystal")
        )

    def start(self, state: GameState, display: Display) -> str:
        state.puzzle_states["attention"] = "in_progress"
        state.flags["attention_step"] = 0
        return (
            "The three pedestals glow, sensing the crystals in your "
            "inventory. Place each crystal on its matching pedestal.\n\n"
            "Type 'place query_crystal on pedestal' (or 'place key_crystal "
            "on pedestal', 'place value_crystal on pedestal')."
        )

    def _crystals_placed(self, state: GameState) -> int:
        count = 0
        if state.flags.get("placed_query"): count += 1
        if state.flags.get("placed_key"): count += 1
        if state.flags.get("placed_value"): count += 1
        return count

    def handle_input(self, raw: str, state: GameState,
                      display: Display) -> str | None:
        if state.puzzle_states.get("attention") != "in_progress":
            return None

        raw = raw.strip().lower()

        # Handle crystal placement
        if "place" in raw or "put" in raw or "use" in raw:
            if "query" in raw and "query_crystal" in state.inventory:
                state.flags["placed_query"] = True
                state.inventory.remove("query_crystal")
                placed = self._crystals_placed(state)
                if placed == 3:
                    return self._all_placed(state)
                return (
                    "You place the Query Crystal on the Q pedestal. It "
                    "glows with questions: 'What am I looking for?'\n\n"
                    f"Crystals placed: {placed}/3."
                )
            elif "key" in raw and "key_crystal" in state.inventory:
                state.flags["placed_key"] = True
                state.inventory.remove("key_crystal")
                placed = self._crystals_placed(state)
                if placed == 3:
                    return self._all_placed(state)
                return (
                    "You place the Key Crystal on the K pedestal. It hums: "
                    "'Here is what I contain.'\n\n"
                    f"Crystals placed: {placed}/3."
                )
            elif "value" in raw and "value_crystal" in state.inventory:
                state.flags["placed_value"] = True
                state.inventory.remove("value_crystal")
                placed = self._crystals_placed(state)
                if placed == 3:
                    return self._all_placed(state)
                return (
                    "You place the Value Crystal on the V pedestal. It "
                    "glows: 'Take what you need.'\n\n"
                    f"Crystals placed: {placed}/3."
                )

        # Handle bonus question FIRST (before main question check)
        if state.flags.get("attention_bonus_active"):
            choice = raw
            if raw.startswith("choose "):
                choice = raw[7:].strip()

            if choice == "skip":
                return self._solve(state, bonus=False)
            elif choice == "c" or choice == "both":
                state.flags["attention_bonus_correct"] = True
                return self._solve(state, bonus=True)
            elif choice in ("a", "b"):
                return (
                    "You're partially right, but there's a more complete "
                    "answer. Think about whether BOTH reasons contribute. "
                    "Or type 'skip' to move on."
                )
            return None

        # Handle the main comprehension question
        if state.flags.get("attention_question_active"):
            choice = raw
            if raw.startswith("choose "):
                choice = raw[7:].strip()

            if choice in ("c", "cat"):
                state.flags["attention_main_correct"] = True
                state.flags["attention_bonus_active"] = True
                return (
                    "CORRECT! The word 'it' most strongly attends to 'cat' "
                    "because 'it' is a pronoun that refers back to the cat. "
                    "The attention mechanism learns to connect pronouns with "
                    "their referents -- this is one of its most important "
                    "capabilities.\n\n"
                    "The beams between 'it' and 'cat' blaze brightly.\n\n"
                    "BONUS QUESTION (for extra points):\n"
                    "  Why might 'mat' ALSO receive some attention from 'it'?\n\n"
                    "  A) 'it' could refer to the mat (the mat was old)\n"
                    "  B) 'mat' is close by in the sentence\n"
                    "  C) Both A and B\n\n"
                    "Type 'choose A', 'choose B', or 'choose C' "
                    "(or 'skip' to skip the bonus)."
                )
            elif choice in ("a", "the"):
                return (
                    "Not quite. 'The' is a common function word -- it "
                    "doesn't carry the meaning that 'it' is looking for. "
                    "Think about what 'it' REFERS to in the sentence."
                )
            elif choice in ("b", "mat"):
                return (
                    "Possible, but there's a stronger connection. In "
                    "'because it was tired,' what was tired? Usually "
                    "tiredness applies to a living thing. Try again!"
                )
            elif choice in ("d", "because"):
                return (
                    "'Because' explains the reason, but 'it' is looking "
                    "for its REFERENT -- the thing it stands for. What "
                    "was tired?"
                )

        return None

    def _all_placed(self, state: GameState) -> str:
        state.flags["attention_question_active"] = True
        return (
            "All three crystals resonate! Beams of light erupt from the "
            "pedestals, converging above them. A holographic sentence "
            "appears:\n\n"
            "  'The cat sat on the mat because it was tired.'\n\n"
            "The Attention Mechanism speaks:\n"
            "  'In this sentence, what does the word \"it\" most likely "
            "attend to?'\n\n"
            "  A) 'the'\n"
            "  B) 'mat'\n"
            "  C) 'cat'\n"
            "  D) 'because'\n\n"
            "Type 'choose' followed by A, B, C, or D."
        )

    def _solve(self, state: GameState, bonus: bool) -> str:
        state.puzzle_states["attention"] = "solved"
        state.flags["attention_puzzle_solved"] = True
        state.flags["attention_question_active"] = False
        state.flags["attention_bonus_active"] = False

        bonus_text = ""
        if bonus:
            bonus_text = (
                "\n\nBONUS CORRECT! Attention is probabilistic -- it "
                "doesn't just pick one answer. 'It' could theoretically "
                "refer to 'mat' (ambiguity), AND nearby tokens get some "
                "attention simply due to proximity. The attention mechanism "
                "assigns probabilities, not certainties."
            )

        return (
            "The crystals merge into a single Attention Matrix -- a "
            "shimmering grid that shows the attention patterns between "
            "all tokens in any sentence. The door to the south swings "
            "open." + bonus_text + "\n\n"
            "The path to the Training Grounds is now open!"
        )

    def is_solved(self, state: GameState) -> bool:
        return state.puzzle_states.get("attention") == "solved"

    def get_hint(self, state: GameState) -> str:
        if not self.can_start(state):
            missing = []
            if "query_crystal" not in state.inventory:
                missing.append("Query Crystal (west of the Attention Nexus)")
            if "key_crystal" not in state.inventory:
                missing.append("Key Crystal (northeast of the Attention Nexus)")
            if "value_crystal" not in state.inventory:
                missing.append("Value Crystal (east of the Attention Nexus)")
            return (
                "You need all three crystals: " + ", ".join(missing) + ". "
                "Explore the chambers off the Attention Nexus."
            )
        if self._crystals_placed(state) < 3:
            return "Place each crystal on its pedestal: 'place query_crystal on pedestal'"
        return (
            "In 'The cat sat on the mat because it was tired,' what does "
            "'it' refer to? What was tired?"
        )
