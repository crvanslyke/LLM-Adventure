"""Puzzle 5: Tuning the Generator -- teach temperature/sampling."""

from puzzles.base import Puzzle
from game.state import GameState
from game.display import Display


# Pre-written outputs for different temperature ranges
OUTPUTS = {
    "too_low": [
        "The the the the the the the the the the...",
        "The researcher walked to the the the the the...",
        "I think the most important thing is the most important thing is the...",
    ],
    "low": [
        "The researcher carefully documented the results of the experiment.",
        "The data showed a clear trend toward increased efficiency.",
        "In conclusion, the evidence strongly supports the hypothesis.",
    ],
    "good": [
        "The researcher ventured deeper into the neural network, discovering patterns that shimmered like constellations in a digital sky.",
        "Inside the model, language flowed like a river -- sometimes calm and predictable, sometimes turbulent with unexpected metaphors.",
        "Every token carried a story, every attention head held a different perspective, and together they wove tapestries of meaning.",
    ],
    "high": [
        "Purple quantum elephants democracy fish pancake the MAGNIFICENT!",
        "Wobbling fractal Tuesday sings to the inverted probability of cheese!",
        "Kaleidoscope neurons hiccup forgotten alphabets through translucent math!",
    ],
}


class SamplingPuzzle(Puzzle):
    puzzle_id = "sampling"

    def can_start(self, state: GameState) -> bool:
        return True

    def start(self, state: GameState, display: Display) -> str:
        state.puzzle_states["sampling"] = "in_progress"
        state.flags["sampling_temperature"] = 1.0
        state.flags["sampling_top_k"] = 50
        state.flags["sampling_top_p"] = 0.9
        state.flags["sampling_pull_count"] = 0
        return (
            "The Sampling Chamber activates! Three dials glow:\n\n"
            "  TEMPERATURE: 1.0    (set temperature <0.0-2.0>)\n"
            "  TOP-K:       50     (set top_k <1-100>)\n"
            "  TOP-P:       0.9    (set top_p <0.0-1.0>)\n\n"
            "Adjust the dials and 'pull lever' to generate text.\n"
            "The door needs 'coherent but creative' output to open."
        )

    def handle_input(self, raw: str, state: GameState,
                      display: Display) -> str | None:
        if state.puzzle_states.get("sampling") != "in_progress":
            return None

        raw = raw.strip().lower()

        # Handle "set" commands
        if raw.startswith("set "):
            parts = raw.split()
            if len(parts) >= 3:
                dial = parts[1]
                try:
                    value = float(parts[2])
                except ValueError:
                    return "Please provide a numeric value."

                if dial == "temperature":
                    value = max(0.0, min(2.0, value))
                    state.flags["sampling_temperature"] = value
                    flavor = self._temp_flavor(value)
                    return f"Temperature set to {value} ({flavor})."
                elif dial in ("top_k", "topk", "top-k", "k"):
                    value = max(1, min(100, int(value)))
                    state.flags["sampling_top_k"] = value
                    return f"Top-K set to {int(value)}."
                elif dial in ("top_p", "topp", "top-p", "p"):
                    value = max(0.0, min(1.0, value))
                    state.flags["sampling_top_p"] = value
                    return f"Top-P set to {value}."

            return "Usage: set temperature <value>, set top_k <value>, or set top_p <value>"

        # Handle "pull lever"
        if "pull" in raw and ("lever" in raw or raw == "pull"):
            temp = state.flags.get("sampling_temperature", 1.0)
            pull_count = state.flags.get("sampling_pull_count", 0)
            state.flags["sampling_pull_count"] = pull_count + 1

            # Determine output category
            import random
            if temp < 0.2:
                category = "too_low"
                verdict = "TOO REPETITIVE"
            elif temp < 0.5:
                category = "low"
                verdict = "COHERENT BUT BORING"
            elif temp <= 0.9:
                category = "good"
                verdict = None  # Winner!
            elif temp <= 1.3:
                # Borderline -- could go either way
                category = "high" if temp > 1.1 else "good"
                verdict = "TOO CHAOTIC" if category == "high" else None
            else:
                category = "high"
                verdict = "TOO CHAOTIC"

            idx = pull_count % len(OUTPUTS[category])
            output = OUTPUTS[category][idx]

            if verdict is None:
                # SUCCESS!
                state.puzzle_states["sampling"] = "solved"
                state.flags["sampling_puzzle_solved"] = True
                return (
                    f"Generated: \"{output}\"\n\n"
                    "The door chimes: COHERENT AND CREATIVE!\n\n"
                    "The door swings open with a satisfying click. The "
                    "Temperature Dial detaches from the wall and floats "
                    "into your hands -- a souvenir from the Sampling "
                    "Chamber.\n\n"
                    f"Your winning settings: Temperature={temp}\n\n"
                    "The path south to the Output Stream is now open!"
                )
            else:
                return (
                    f"Generated: \"{output}\"\n\n"
                    f"The door buzzer sounds: {verdict}.\n\n"
                    "Adjust the temperature and try again. Remember: too "
                    "low = repetitive, too high = chaotic. Find the sweet "
                    "spot between creativity and coherence."
                )

        return None

    def _temp_flavor(self, temp: float) -> str:
        if temp < 0.2:
            return "nearly deterministic -- will always pick the top token"
        elif temp < 0.5:
            return "conservative -- predictable and safe"
        elif temp <= 0.9:
            return "balanced -- coherent with some creativity"
        elif temp <= 1.3:
            return "warm -- more creative, less predictable"
        else:
            return "very hot -- highly random, expect chaos"

    def is_solved(self, state: GameState) -> bool:
        return state.puzzle_states.get("sampling") == "solved"

    def get_hint(self, state: GameState) -> str:
        temp = state.flags.get("sampling_temperature", 1.0)
        if temp < 0.5:
            return "Temperature is too low -- output will be repetitive. Try raising it to around 0.7."
        elif temp > 0.9:
            return "Temperature is too high -- output will be chaotic. Try lowering it to around 0.7."
        else:
            return "The temperature looks good. Try pulling the lever!"
