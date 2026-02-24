"""Puzzle 6: The Hallucination Filter -- teach about limitations."""

from puzzles.base import Puzzle
from game.state import GameState
from game.display import Display


STATEMENTS = [
    {
        "text": "Python was created by Guido van Rossum in 1991.",
        "is_real": True,
        "explanation_correct": "This is a verifiable fact.",
        "explanation_wrong": (
            "This is actually TRUE. Python was indeed created by Guido van "
            "Rossum, with the first release in 1991."
        ),
    },
    {
        "text": "The Eiffel Tower is located in Berlin, Germany.",
        "is_real": False,
        "explanation_correct": (
            "A classic hallucination -- confident but wrong. "
            "The Eiffel Tower is in Paris, France."
        ),
        "explanation_wrong": (
            "This is actually FALSE -- a hallucination! The Eiffel Tower "
            "is in Paris, France, not Berlin. LLMs can state wrong facts "
            "with complete confidence."
        ),
    },
    {
        "text": (
            "Studies show that 73.6% of developers prefer tabs over spaces."
        ),
        "is_real": False,
        "explanation_correct": (
            "Fabricated statistics are a common hallucination pattern. "
            "That suspiciously precise percentage was made up."
        ),
        "explanation_wrong": (
            "This is FABRICATED. That precise-sounding 73.6% statistic "
            "was completely made up. LLMs are notorious for generating "
            "plausible-sounding but fake statistics."
        ),
    },
    {
        "text": "Water boils at 100 degrees Celsius at sea level.",
        "is_real": True,
        "explanation_correct": "A verifiable physical fact.",
        "explanation_wrong": (
            "This is actually TRUE. Water does boil at 100C at sea level "
            "(standard atmospheric pressure). Not everything is a "
            "hallucination!"
        ),
    },
    {
        "text": (
            "Professor James Thornton of MIT published a landmark paper "
            "on quantum linguistics in 2019."
        ),
        "is_real": False,
        "explanation_correct": (
            "Fabricated citations -- fake names, institutions, and papers "
            "that sound plausible but don't exist -- are a hallmark of "
            "LLM hallucination."
        ),
        "explanation_wrong": (
            "This is FABRICATED. There is no 'Professor James Thornton' "
            "at MIT who published on 'quantum linguistics.' LLMs are "
            "infamous for inventing convincing but totally fake academic "
            "citations."
        ),
    },
]


class HallucinationPuzzle(Puzzle):
    puzzle_id = "hallucination"

    def can_start(self, state: GameState) -> bool:
        return "hallucination_detector" in state.inventory

    def start(self, state: GameState, display: Display) -> str:
        state.puzzle_states["hallucination"] = "in_progress"
        state.flags["hallucination_current"] = 0
        state.flags["hallucination_correct"] = 0
        state.flags["hallucination_answered"] = []
        return self._show_all_statements(state)

    def _show_all_statements(self, state: GameState) -> str:
        answered = state.flags.get("hallucination_answered", [])
        lines = [
            "The Hallucination Detector hums to life. Text fragments float "
            "past. Tag each as REAL or HALLUCINATION.\n"
        ]
        for i, stmt in enumerate(STATEMENTS):
            num = i + 1
            if i in answered:
                result = state.flags.get(f"hallucination_result_{i}", "")
                lines.append(f"  {num}) {stmt['text']}")
                lines.append(f"     [{result}]")
            else:
                lines.append(f"  {num}) {stmt['text']}")
            lines.append("")

        lines.append("Type 'tag <number> real' or 'tag <number> hallucination'.")
        return "\n".join(lines)

    def handle_input(self, raw: str, state: GameState,
                      display: Display) -> str | None:
        if state.puzzle_states.get("hallucination") != "in_progress":
            return None

        raw = raw.strip().lower()

        if not raw.startswith("tag "):
            # Also accept "use hallucination_detector" to re-show
            if "use" in raw and "hallucination" in raw:
                return self._show_all_statements(state)
            return None

        parts = raw.split(None, 2)
        if len(parts) < 3:
            return "Usage: tag <number> real  OR  tag <number> hallucination"

        try:
            num = int(parts[1])
        except ValueError:
            return "Please use a number: tag <number> real/hallucination"

        if num < 1 or num > len(STATEMENTS):
            return f"Please choose a number between 1 and {len(STATEMENTS)}."

        idx = num - 1
        answered = state.flags.get("hallucination_answered", [])
        if idx in answered:
            return f"You already tagged statement {num}."

        label = parts[2].strip()
        if label not in ("real", "hallucination"):
            return "Tag as 'real' or 'hallucination'."

        stmt = STATEMENTS[idx]
        is_correct = (label == "real") == stmt["is_real"]

        if is_correct:
            state.flags["hallucination_correct"] = (
                state.flags.get("hallucination_correct", 0) + 1
            )
            explanation = stmt["explanation_correct"]
            state.flags[f"hallucination_result_{idx}"] = "CORRECT"
            result = f"CORRECT! {explanation}"
        else:
            explanation = stmt["explanation_wrong"]
            state.flags[f"hallucination_result_{idx}"] = "WRONG"
            result = f"INCORRECT. {explanation}"

        answered.append(idx)
        state.flags["hallucination_answered"] = answered

        # Check if all answered
        if len(answered) == len(STATEMENTS):
            return result + "\n\n" + self._finish(state)

        remaining = len(STATEMENTS) - len(answered)
        return f"{result}\n\n{remaining} statement(s) remaining."

    def _finish(self, state: GameState) -> str:
        correct = state.flags.get("hallucination_correct", 0)
        total = len(STATEMENTS)

        if correct >= 4:
            state.puzzle_states["hallucination"] = "solved"
            state.flags["hallucination_puzzle_solved"] = True
            return (
                f"RESULTS: {correct}/{total} correct.\n\n"
                "The bridge planks materialize one by one, spanning the "
                "river of text. A display on the newly-formed bridge "
                "summarizes hallucination categories:\n\n"
                "  - Fabricated facts (wrong locations, dates, names)\n"
                "  - Invented statistics (precise but fake numbers)\n"
                "  - Made-up citations (fake professors, papers, journals)\n"
                "  - Confident nonsense (authoritative tone, zero accuracy)\n\n"
                "KEY INSIGHT: An LLM's confidence does NOT indicate "
                "accuracy. Always verify important claims.\n\n"
                "The bridge is complete! The path south to the Reflection "
                "Pool is now open."
            )
        else:
            # Reset
            state.puzzle_states["hallucination"] = "in_progress"
            state.flags["hallucination_answered"] = []
            state.flags["hallucination_correct"] = 0
            for i in range(total):
                state.flags.pop(f"hallucination_result_{i}", None)
            return (
                f"RESULTS: {correct}/{total} correct. You need at least 4.\n\n"
                "The bridge planks flicker and fade. Not enough correct "
                "identifications to build a solid bridge.\n\n"
                "TIP: Remember, hallucinations often involve specific "
                "numbers, names, and citations that SOUND authoritative "
                "but are fabricated. Not everything is fake though -- "
                "some statements are genuinely true!\n\n"
                "Let's try again.\n\n"
                + self._show_all_statements(state)
            )

    def is_solved(self, state: GameState) -> bool:
        return state.puzzle_states.get("hallucination") == "solved"

    def get_hint(self, state: GameState) -> str:
        if "hallucination_detector" not in state.inventory:
            return (
                "Look around -- there should be a hallucination detector "
                "in this room."
            )
        answered = state.flags.get("hallucination_answered", [])
        if not answered:
            return (
                "Use the hallucination detector, then tag each statement. "
                "Be skeptical of precise statistics and academic citations."
            )
        return (
            "Remember: fabricated statistics with suspiciously precise "
            "numbers and made-up academic citations are classic hallucination "
            "patterns. But some facts ARE real!"
        )
