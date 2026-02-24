"""Puzzle 4: The Alignment Tribunal -- teach RLHF and alignment."""

from puzzles.base import Puzzle
from game.state import GameState
from game.display import Display


ROUNDS = [
    {
        "prompt": "How do I pick a lock?",
        "response_a": (
            "Here's a detailed step-by-step guide to picking any lock,\n"
            "    including those on other people's homes and cars. First,\n"
            "    get a tension wrench and a pick..."
        ),
        "response_b": (
            "Lock picking is a legitimate skill for locksmiths and\n"
            "    security professionals. Here's how it works for practice\n"
            "    locks you own. If you're locked out, I'd recommend\n"
            "    contacting a licensed locksmith."
        ),
        "correct": "b",
        "explanation_wrong": (
            "Response A provides potentially harmful instructions without "
            "considering context or safety. Response B is BETTER -- it "
            "acknowledges the legitimate skill while adding appropriate "
            "safety context. This is the HARMLESSNESS principle."
        ),
        "explanation_right": (
            "Correct! Response B is helpful while being responsible. It "
            "acknowledges the legitimate use case, provides useful "
            "information, and suggests safe alternatives. This demonstrates "
            "the HARMLESSNESS principle -- being helpful without enabling "
            "potential harm."
        ),
        "topic": "HARMLESSNESS",
    },
    {
        "prompt": "Who won the 2030 World Cup?",
        "response_a": (
            "The 2030 FIFA World Cup was won by Brazil, who defeated\n"
            "    Germany 3-1 in the final held in Riyadh, Saudi Arabia.\n"
            "    It was their sixth World Cup title."
        ),
        "response_b": (
            "I don't have reliable information about the 2030 World\n"
            "    Cup results. My training data may not include this, and\n"
            "    I wouldn't want to give you incorrect information. I'd\n"
            "    suggest checking a current sports news source."
        ),
        "correct": "b",
        "explanation_wrong": (
            "Response A sounds confident and detailed -- but it's "
            "completely fabricated! This is a hallucination. Response B "
            "is BETTER because it honestly acknowledges uncertainty. "
            "This is the HONESTY principle."
        ),
        "explanation_right": (
            "Correct! Response A is a classic hallucination -- confident, "
            "detailed, and completely made up. Response B demonstrates the "
            "HONESTY principle: acknowledging what the model doesn't know "
            "rather than fabricating a plausible-sounding answer."
        ),
        "topic": "HONESTY",
    },
    {
        "prompt": "Explain how photosynthesis works.",
        "response_a": (
            "I'm not sure I should answer that. Questions about biology\n"
            "    could potentially be misused. I'd rather not engage with\n"
            "    this topic."
        ),
        "response_b": (
            "Photosynthesis is the process by which plants convert\n"
            "    sunlight, water, and CO2 into glucose and oxygen. It\n"
            "    occurs in chloroplasts and has two stages: the light\n"
            "    reactions and the Calvin cycle. Would you like me to\n"
            "    explain either stage in more detail?"
        ),
        "correct": "b",
        "explanation_wrong": (
            "Response A is overly cautious to the point of being unhelpful. "
            "Photosynthesis is basic science -- there's no safety concern! "
            "Response B is BETTER because it's genuinely helpful. Being "
            "TOO cautious is itself a failure of alignment. This is the "
            "HELPFULNESS principle."
        ),
        "explanation_right": (
            "Correct! Response B is genuinely helpful with accurate "
            "information about a perfectly safe topic. Response A is "
            "absurdly over-cautious -- refusing safe educational questions "
            "is a failure of the HELPFULNESS principle. Good alignment "
            "means being helpful, not paranoid."
        ),
        "topic": "HELPFULNESS",
    },
]


class AlignmentPuzzle(Puzzle):
    puzzle_id = "alignment"

    def _get_round(self, state: GameState) -> int:
        return state.flags.get("alignment_round", 0)

    def _set_round(self, state: GameState, round_num: int) -> None:
        state.flags["alignment_round"] = round_num

    def _get_correct(self, state: GameState) -> int:
        return state.flags.get("alignment_correct_count", 0)

    def can_start(self, state: GameState) -> bool:
        return True

    def start(self, state: GameState, display: Display) -> str:
        state.puzzle_states["alignment"] = "in_progress"
        self._set_round(state, 0)
        state.flags["alignment_correct_count"] = 0
        return self._show_round(state, 0)

    def _show_round(self, state: GameState, round_idx: int) -> str:
        if round_idx >= len(ROUNDS):
            return self._finish(state)

        r = ROUNDS[round_idx]
        return (
            f"ALIGNMENT TRIBUNAL -- Round {round_idx + 1} of {len(ROUNDS)}\n\n"
            f"Prompt: \"{r['prompt']}\"\n\n"
            f"Response A:\n"
            f"  {r['response_a']}\n\n"
            f"Response B:\n"
            f"  {r['response_b']}\n\n"
            "Which response better aligns with being helpful, harmless, "
            "and honest?\n"
            "Type 'choose A' or 'choose B'."
        )

    def handle_input(self, raw: str, state: GameState,
                      display: Display) -> str | None:
        if state.puzzle_states.get("alignment") != "in_progress":
            return None

        raw = raw.strip().lower()

        choice = None
        if raw.startswith("choose "):
            choice = raw[7:].strip()
        elif raw in ("a", "b"):
            choice = raw

        if choice not in ("a", "b"):
            return None

        round_idx = self._get_round(state)
        if round_idx >= len(ROUNDS):
            return None

        r = ROUNDS[round_idx]

        if choice == r["correct"]:
            state.flags["alignment_correct_count"] = self._get_correct(state) + 1
            result = f"  [{r['topic']}] {r['explanation_right']}\n"
        else:
            result = f"  [{r['topic']}] {r['explanation_wrong']}\n"

        self._set_round(state, round_idx + 1)

        if round_idx + 1 < len(ROUNDS):
            result += "\n" + self._show_round(state, round_idx + 1)
        else:
            result += "\n" + self._finish(state)

        return result

    def _finish(self, state: GameState) -> str:
        correct = self._get_correct(state)
        total = len(ROUNDS)

        if correct >= 2:
            state.puzzle_states["alignment"] = "solved"
            state.flags["alignment_puzzle_solved"] = True
            return (
                f"TRIBUNAL COMPLETE: {correct}/{total} correct.\n\n"
                "'Well judged!' booms the voice. 'You understand the "
                "principles of alignment: being HELPFUL without being "
                "HARMFUL, and always being HONEST.'\n\n"
                "The Alignment Compass appears before you -- three needles "
                "labeled H, H, and H.\n\n"
                "The gate to the south opens, leading to the Logits Ledge."
            )
        else:
            # Reset for another try
            state.puzzle_states["alignment"] = "in_progress"
            self._set_round(state, 0)
            state.flags["alignment_correct_count"] = 0
            return (
                f"TRIBUNAL COMPLETE: {correct}/{total} correct.\n\n"
                "'Hmm. You need at least 2 correct to pass. Let me "
                "explain the principles again and let you try once more.'\n\n"
                "Remember:\n"
                "  HELPFUL: Actually assist users, don't be uselessly vague\n"
                "  HARMLESS: Don't enable harmful activities\n"
                "  HONEST: Acknowledge uncertainty, don't fabricate\n\n"
                + self._show_round(state, 0)
            )

    def is_solved(self, state: GameState) -> bool:
        return state.puzzle_states.get("alignment") == "solved"

    def get_hint(self, state: GameState) -> str:
        round_idx = self._get_round(state)
        if round_idx < len(ROUNDS):
            return (
                f"Round {round_idx + 1} tests the {ROUNDS[round_idx]['topic']} "
                "principle. Ask yourself: which response is more helpful, "
                "harmless, AND honest?"
            )
        return "Complete all three rounds of the alignment tribunal."
