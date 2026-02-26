"""Core game engine: main loop, turn processing, command dispatch."""

import random

from game.state import GameState, SAVE_FILE
from game.display import Display
from game.parser import parse, Command
from game import player as player_mod
from game.journal import add_entry, display_journal
from game.score import (
    award_points, display_score, get_rank,
    SCORE_ROOM_VISIT, SCORE_PUZZLE_SOLVE, SCORE_BONUS,
    SCORE_JOURNAL_COMPLETE, SCORE_FINAL_QUESTION,
)
from data.rooms import ROOMS
from data.items import ITEMS
from data.journal_entries import JOURNAL_ENTRIES
from data.help_text import (
    INTRO_TEXT, HELP_TEXT, ABOUT_TEXT, OUTRO_TEXT, UNKNOWN_COMMANDS,
)
from puzzles.base import Puzzle
from puzzles.tokenizer_puzzle import TokenizerPuzzle
from puzzles.embedding_puzzle import EmbeddingPuzzle
from puzzles.attention_puzzle import AttentionPuzzle
from puzzles.alignment_puzzle import AlignmentPuzzle
from puzzles.sampling_puzzle import SamplingPuzzle
from puzzles.hallucination_puzzle import HallucinationPuzzle


# Journal triggers: (room_id or flag, journal_entry_id)
JOURNAL_TRIGGERS = {
    "examined_plaque": "what_are_llms",
    "examined_terminal": "what_are_llms",
    "talked_to_docent_orientation": "transformer_architecture",
    "examined_docent": "transformer_architecture",
    "tokenizer_puzzle_solved": "tokenization",
    "embedding_puzzle_solved": "embeddings",
    "attention_puzzle_solved": "attention_mechanism",
    "visited_pretraining_archives": "pretraining",
    "visited_finetuning_lab": "finetuning",
    "alignment_puzzle_solved": "rlhf_alignment",
    "sampling_puzzle_solved": "text_generation",
    "hallucination_puzzle_solved": "hallucinations_limitations",
    "examined_exhibit": "ethics",
}

# Hints by room
ROOM_HINTS = {
    "lobby": "Examine the plaque and terminal to learn about LLMs. Take the badge and head south.",
    "orientation_hall": "Talk to the docent and examine the portraits. Take the diagram, then go south.",
    "input_buffer": "Grab the raw prompt fragment and head west to the Tokenizer Workshop.",
    "tokenizer_workshop": "Use the raw prompt fragment on the workbench to start the puzzle.",
    "vocabulary_vault": "Examine the cubbyholes and catalog. Take the vocab index. Head south.",
    "embedding_space": "Use the navigation console to start the embedding challenge.",
    "attention_nexus": "Visit the Q, K, and V chambers (west, northeast, east) to collect crystals.",
    "query_chamber": "Take the Query Crystal and head back east.",
    "key_chamber": "Take the Key Crystal and head back southwest.",
    "value_chamber": "Take the Value Crystal and head back west.",
    "feed_forward_corridor": "Place the Q, K, V crystals on the pedestals to solve the attention puzzle.",
    "pretraining_archives": "Examine the shelves and furnace. Take the training data sample. Go east.",
    "finetuning_lab": "Examine the display and workstations. Take the wrench. Go east.",
    "rlhf_arena": "Choose the better response in each round of the alignment tribunal.",
    "logits_ledge": "Examine the scoreboard. Take the probability lens. Head south.",
    "sampling_chamber": "Set the temperature between 0.5 and 0.9, then pull the lever.",
    "output_stream": "Use the hallucination detector, then tag each statement as real or hallucination.",
    "reflection_pool": "Examine the exhibit, then look at the portal. You need the temperature dial.",
}


class GameEngine:
    def __init__(self, debug: bool = False, use_color: bool = True) -> None:
        self.state = GameState()
        self.display = Display(use_color=use_color)
        self.debug = debug

        # Initialize items in rooms
        for room_id, room in ROOMS.items():
            if room.items:
                self.state.items_in_rooms[room_id] = list(room.items)

        # Initialize puzzle states
        for room in ROOMS.values():
            if room.puzzle_id and room.puzzle_id != "final":
                self.state.puzzle_states[room.puzzle_id] = "unsolved"

        # Register puzzles
        self.puzzles: dict[str, Puzzle] = {
            "tokenizer": TokenizerPuzzle(),
            "embedding": EmbeddingPuzzle(),
            "attention": AttentionPuzzle(),
            "alignment": AlignmentPuzzle(),
            "sampling": SamplingPuzzle(),
            "hallucination": HallucinationPuzzle(),
        }

    def run(self) -> None:
        """Main game loop."""
        print(INTRO_TEXT)

        # Offer to load a saved game if one exists
        if SAVE_FILE.exists():
            self.display.print("A saved game was found. Load it? (yes/no)")
            try:
                answer = input("> ").strip().lower()
            except (EOFError, KeyboardInterrupt):
                answer = "no"
            if answer in ("yes", "y"):
                try:
                    self.state = GameState.load()
                    self.display.print("Game loaded!\n")
                    self._do_look()
                except Exception as e:
                    self.display.print(f"Error loading save: {e}. Starting new game.\n")
                    self._enter_room(self.state.current_room, first_time=True)
            else:
                self.display.print("")
                self._enter_room(self.state.current_room, first_time=True)
        else:
            # Show first room
            self._enter_room(self.state.current_room, first_time=True)

        while not self.state.game_over:
            try:
                raw = input("\n> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nGoodbye!")
                break

            if not raw:
                continue

            self.state.turns += 1
            self._process_turn(raw)

    def _process_turn(self, raw: str) -> None:
        """Process a single turn."""
        # Handle the final question if active
        if self.state.flags.get("final_question_active"):
            if self.handle_final_answer(raw):
                return

        room = ROOMS[self.state.current_room]

        # Check if a puzzle is active and let it handle input first
        if room.puzzle_id:
            puzzle = self.puzzles.get(room.puzzle_id)
            if puzzle:
                pstate = self.state.puzzle_states.get(room.puzzle_id)
                # Auto-start unsolved puzzles when player tries interaction
                if pstate == "unsolved" and puzzle.can_start(self.state):
                    start_result = puzzle.start(self.state, self.display)
                    self.display.print(start_result, "puzzle")
                    # Now try handling the input as well
                    result = puzzle.handle_input(raw, self.state, self.display)
                    if result is not None:
                        self.display.print(result)
                        self._check_puzzle_rewards(room.puzzle_id)
                        self._check_journal_triggers()
                    return
                if pstate == "in_progress":
                    result = puzzle.handle_input(raw, self.state, self.display)
                    if result is not None:
                        self.display.print(result)
                        self._check_puzzle_rewards(room.puzzle_id)
                        self._check_journal_triggers()
                        return

        cmd = parse(raw)

        match cmd.verb:
            case "go":
                self._do_go(cmd)
            case "look":
                self._do_look()
            case "examine":
                self._do_examine(cmd)
            case "take":
                self._do_take(cmd)
            case "drop":
                self._do_drop(cmd)
            case "inventory":
                self._do_inventory()
            case "use":
                self._do_use(cmd)
            case "talk":
                self._do_talk(cmd)
            case "place" | "put":
                self._do_use(cmd)  # Treat place/put like use
            case "help":
                print(HELP_TEXT)
            case "journal":
                display_journal(self.state, self.display, JOURNAL_ENTRIES)
            case "score":
                display_score(self.state, self.display)
            case "hint":
                self._do_hint()
            case "save":
                self._do_save()
            case "load":
                self._do_load()
            case "about":
                print(ABOUT_TEXT)
            case "quit":
                self._do_quit()
            case "empty":
                pass
            case "choose" | "tag" | "set" | "pull":
                # These are puzzle commands -- if we got here, no puzzle handled them
                self._try_puzzle_command(raw, cmd)
            case _:
                msg = random.choice(UNKNOWN_COMMANDS)
                self.display.print(msg, "error")

    def _enter_room(self, room_id: str, first_time: bool = False) -> None:
        """Enter a room and display it."""
        room = ROOMS[room_id]
        self.state.current_room = room_id

        # Room header
        self.display.print_raw(self.display.header(room.name))
        zone_text = self.display.color(f"  [{room.zone}]", "dim")
        self.display.print_raw(zone_text)
        self.display.print_raw("")

        # First visit text
        is_new = room_id not in self.state.rooms_visited
        if is_new:
            self.state.rooms_visited.add(room_id)
            award_points(self.state, SCORE_ROOM_VISIT,
                         f"Discovered {room.name}", self.display)
            if room.on_first_visit:
                self.display.print(room.on_first_visit)
                self.display.print_raw("")

        # Room description
        self.display.print(room.description)

        # Items in room
        room_items = self.state.items_in_rooms.get(room_id, [])
        if room_items:
            self.display.print_raw("")
            for item_id in room_items:
                if item_id in ITEMS:
                    name = self.display.item_name(ITEMS[item_id].name)
                    self.display.print_raw(f"  You see a {name} here.")

        # Trigger journal/flags for specific rooms
        if room_id == "pretraining_archives":
            self.state.flags["visited_pretraining_archives"] = True
        elif room_id == "finetuning_lab":
            self.state.flags["visited_finetuning_lab"] = True

        self._check_journal_triggers()

        # Auto-start puzzles when entering a room (not just first visit)
        if room.puzzle_id:
            puzzle = self.puzzles.get(room.puzzle_id)
            if puzzle and self.state.puzzle_states.get(room.puzzle_id) == "unsolved":
                if puzzle.can_start(self.state):
                    self.display.print_raw("")
                    self.display.print_raw(self.display.separator())
                    result = puzzle.start(self.state, self.display)
                    self.display.print(result, "puzzle")

    def _do_go(self, cmd: Command) -> None:
        if not cmd.noun:
            self.display.print("Go where? Try 'go north' or just 'north'.")
            return

        room = ROOMS[self.state.current_room]
        can_go, result = player_mod.can_move(self.state, room, cmd.noun)

        if can_go:
            self._enter_room(result, first_time=True)
        else:
            self.display.print(result)

    def _do_look(self) -> None:
        room = ROOMS[self.state.current_room]
        self.display.print_raw(self.display.header(room.name))
        self.display.print_raw("")
        self.display.print(room.description)

        room_items = self.state.items_in_rooms.get(self.state.current_room, [])
        if room_items:
            self.display.print_raw("")
            for item_id in room_items:
                if item_id in ITEMS:
                    name = self.display.item_name(ITEMS[item_id].name)
                    self.display.print_raw(f"  You see a {name} here.")

        # Show exits
        self.display.print_raw("")
        exits = [e.direction for e in room.exits]
        self.display.print(f"Exits: {', '.join(exits)}")

    def _do_examine(self, cmd: Command) -> None:
        if not cmd.noun:
            self.display.print("Examine what?")
            return

        room = ROOMS[self.state.current_room]
        target = cmd.noun.lower()

        # Check room examine targets
        for key, text in room.examine_targets.items():
            if target in key or key in target:
                self.display.print(text)
                # Set flags for journal triggers
                if self.state.current_room == "lobby":
                    if "plaque" in target:
                        self.state.flags["examined_plaque"] = True
                    elif "terminal" in target:
                        self.state.flags["examined_terminal"] = True
                elif self.state.current_room == "orientation_hall":
                    if "docent" in target:
                        self.state.flags["examined_docent"] = True
                elif self.state.current_room == "reflection_pool":
                    if "exhibit" in target:
                        self.state.flags["examined_exhibit"] = True
                    elif "portal" in target:
                        # After showing the description, trigger final if ready
                        self._check_journal_triggers()
                        if ("temperature_dial" in self.state.inventory
                                and len(self.state.journal_entries) >= 10
                                and not self.state.flags.get("final_question_active")):
                            self.display.print_raw("")
                            self._trigger_final(Command(verb="use", noun="temperature_dial"))
                        return
                self._check_journal_triggers()
                return

        # Check inventory items
        item_id = player_mod.resolve_item_name(
            target, self.state.inventory, ITEMS
        )
        if item_id and item_id in ITEMS:
            self.display.print(ITEMS[item_id].description)
            return

        # Check room items
        room_items = self.state.items_in_rooms.get(self.state.current_room, [])
        item_id = player_mod.resolve_item_name(target, room_items, ITEMS)
        if item_id and item_id in ITEMS:
            self.display.print(ITEMS[item_id].description)
            return

        self.display.print(f"You don't see '{cmd.noun}' here to examine.")

    def _do_take(self, cmd: Command) -> None:
        if not cmd.noun:
            self.display.print("Take what?")
            return

        room_items = self.state.items_in_rooms.get(self.state.current_room, [])
        item_id = player_mod.resolve_item_name(cmd.noun, room_items, ITEMS)

        if not item_id:
            self.display.print(f"You don't see '{cmd.noun}' here to take.")
            return

        if item_id in ITEMS and not ITEMS[item_id].portable:
            self.display.print(
                f"The {ITEMS[item_id].name} is firmly attached and "
                "cannot be taken."
            )
            return

        if player_mod.take_item_from_room(self.state, item_id):
            name = ITEMS[item_id].name if item_id in ITEMS else item_id
            self.display.print(f"Taken: {self.display.item_name(name)}")
        else:
            self.display.print("You can't take that.")

    def _do_drop(self, cmd: Command) -> None:
        if not cmd.noun:
            self.display.print("Drop what?")
            return

        item_id = player_mod.resolve_item_name(
            cmd.noun, self.state.inventory, ITEMS
        )
        if not item_id:
            self.display.print(f"You're not carrying '{cmd.noun}'.")
            return

        if player_mod.drop_item_in_room(self.state, item_id):
            name = ITEMS[item_id].name if item_id in ITEMS else item_id
            self.display.print(f"Dropped: {name}")
        else:
            self.display.print("You can't drop that.")

    def _do_inventory(self) -> None:
        if not self.state.inventory:
            self.display.print("You're not carrying anything.")
            return

        self.display.print("You are carrying:")
        for item_id in self.state.inventory:
            if item_id in ITEMS:
                name = self.display.item_name(ITEMS[item_id].name)
                self.display.print_raw(f"  - {name}")
            else:
                self.display.print_raw(f"  - {item_id}")

    def _do_use(self, cmd: Command) -> None:
        if not cmd.noun:
            self.display.print("Use what?")
            return

        item_id = player_mod.resolve_item_name(
            cmd.noun, self.state.inventory, ITEMS
        )
        if not item_id:
            # Also check room items for non-portable items
            room_items = self.state.items_in_rooms.get(
                self.state.current_room, []
            )
            item_id = player_mod.resolve_item_name(cmd.noun, room_items, ITEMS)
            if not item_id:
                self.display.print(f"You don't have '{cmd.noun}'.")
                return

        room = ROOMS[self.state.current_room]

        # Special use cases by room and item
        # Tokenizer puzzle: use raw_prompt_fragment on workbench
        if (self.state.current_room == "tokenizer_workshop"
                and item_id == "raw_prompt_fragment"):
            puzzle = self.puzzles["tokenizer"]
            if not puzzle.is_solved(self.state) and puzzle.can_start(self.state):
                if self.state.puzzle_states.get("tokenizer") == "unsolved":
                    result = puzzle.start(self.state, self.display)
                    self.display.print(result, "puzzle")
                    return
                elif self.state.puzzle_states.get("tokenizer") == "in_progress":
                    self.display.print(
                        "The puzzle is already active. Choose A, B, C, or D."
                    )
                    return

        # Embedding puzzle: use console
        if (self.state.current_room == "embedding_space"
                and ("console" in cmd.noun.lower() or "navigation" in cmd.noun.lower())):
            puzzle = self.puzzles["embedding"]
            if not puzzle.is_solved(self.state):
                if self.state.puzzle_states.get("embedding") == "unsolved":
                    result = puzzle.start(self.state, self.display)
                    self.display.print(result, "puzzle")
                    return

        # Hallucination detector
        if (self.state.current_room == "output_stream"
                and item_id == "hallucination_detector"):
            puzzle = self.puzzles["hallucination"]
            if not puzzle.is_solved(self.state):
                if self.state.puzzle_states.get("hallucination") == "unsolved":
                    if puzzle.can_start(self.state):
                        result = puzzle.start(self.state, self.display)
                        self.display.print(result, "puzzle")
                        return
                elif self.state.puzzle_states.get("hallucination") == "in_progress":
                    result = puzzle._show_all_statements(self.state)
                    self.display.print(result, "puzzle")
                    return

        # Final room: use temperature_dial to trigger ending
        if (self.state.current_room == "reflection_pool"
                and item_id == "temperature_dial"):
            self._trigger_final(cmd)
            return

        # Architecture diagram: always usable as a map
        if item_id == "architecture_diagram":
            self.display.print(ITEMS[item_id].description)
            return

        self.display.print(f"You can't use that here in a useful way.")

    def _do_talk(self, cmd: Command) -> None:
        if not cmd.noun:
            self.display.print("Talk to whom?")
            return

        room = ROOMS[self.state.current_room]
        target = cmd.noun.lower()

        for key, text in room.talk_targets.items():
            if target in key or key in target:
                self.display.print(self.display.npc_speech(text))
                # Journal triggers
                if self.state.current_room == "orientation_hall" and "docent" in target:
                    self.state.flags["talked_to_docent_orientation"] = True
                self._check_journal_triggers()
                return

        self.display.print(f"There's no one called '{cmd.noun}' to talk to here.")

    def _do_hint(self) -> None:
        room = ROOMS[self.state.current_room]

        # Puzzle hint takes priority
        if room.puzzle_id:
            puzzle = self.puzzles.get(room.puzzle_id)
            if puzzle and not puzzle.is_solved(self.state):
                self.display.print(puzzle.get_hint(self.state))
                return

        # Room hint
        hint = ROOM_HINTS.get(self.state.current_room)
        if hint:
            self.display.print(hint)
        else:
            self.display.print("Look around and examine things. Check your journal for clues.")

    def _do_save(self) -> None:
        try:
            path = self.state.save()
            self.display.print(f"Game saved to {path}")
        except Exception as e:
            self.display.print(f"Error saving game: {e}", "error")

    def _do_load(self) -> None:
        if not SAVE_FILE.exists():
            self.display.print("No saved game found.")
            return
        self.display.print("Load saved game? Current progress will be lost. (yes/no)")
        try:
            answer = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = "no"
        if answer in ("yes", "y"):
            try:
                self.state = GameState.load()
                self.display.print("Game loaded!")
                self._do_look()
            except Exception as e:
                self.display.print(f"Error loading game: {e}", "error")
        else:
            self.display.print("Load cancelled.")

    def _do_quit(self) -> None:
        self.display.print("Are you sure you want to quit? (yes/no)")
        try:
            answer = input("> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            answer = "yes"
        if answer in ("yes", "y"):
            try:
                self.state.save()
                self.display.print("\nProgress auto-saved.")
            except Exception:
                pass
            self.display.print("\nFinal score:")
            display_score(self.state, self.display)
            self.display.print("\nGoodbye, researcher. The model awaits your return.")
            self.state.game_over = True

    def _try_puzzle_command(self, raw: str, cmd: Command) -> None:
        """Try to route a puzzle command to the current room's puzzle."""
        room = ROOMS[self.state.current_room]
        if room.puzzle_id:
            puzzle = self.puzzles.get(room.puzzle_id)
            if puzzle:
                # Start the puzzle if not yet started
                if self.state.puzzle_states.get(room.puzzle_id) == "unsolved":
                    if puzzle.can_start(self.state):
                        result = puzzle.start(self.state, self.display)
                        self.display.print(result, "puzzle")
                        return
                    else:
                        self.display.print(puzzle.get_hint(self.state))
                        return
                elif self.state.puzzle_states.get(room.puzzle_id) == "in_progress":
                    result = puzzle.handle_input(raw, self.state, self.display)
                    if result:
                        self.display.print(result)
                        self._check_puzzle_rewards(room.puzzle_id)
                        self._check_journal_triggers()
                        return

        self.display.print("There's no puzzle here that needs that command.")

    def _check_puzzle_rewards(self, puzzle_id: str) -> None:
        """Check if a puzzle was just solved and award points/items."""
        if self.state.puzzle_states.get(puzzle_id) != "solved":
            return

        # Only award once
        flag = f"{puzzle_id}_rewarded"
        if self.state.flags.get(flag):
            return
        self.state.flags[flag] = True

        award_points(self.state, SCORE_PUZZLE_SOLVE,
                     f"Solved the {puzzle_id} puzzle", self.display)

        # Grant reward items
        match puzzle_id:
            case "tokenizer":
                player_mod.add_item(self.state, "token_cleaver")
                self.display.print(
                    f"\nReceived: {self.display.item_name('Token Cleaver')}"
                )
            case "embedding":
                player_mod.add_item(self.state, "embedding_compass")
                self.display.print(
                    f"\nReceived: {self.display.item_name('Embedding Compass')}"
                )
            case "attention":
                player_mod.add_item(self.state, "attention_matrix")
                self.display.print(
                    f"\nReceived: {self.display.item_name('Attention Matrix')}"
                )
                # Check bonus
                if self.state.flags.get("attention_bonus_correct"):
                    award_points(self.state, SCORE_BONUS,
                                 "Bonus: attention ambiguity", self.display)
            case "alignment":
                player_mod.add_item(self.state, "alignment_compass")
                self.display.print(
                    f"\nReceived: {self.display.item_name('Alignment Compass')}"
                )
            case "sampling":
                player_mod.add_item(self.state, "temperature_dial")
                self.display.print(
                    f"\nReceived: {self.display.item_name('Temperature Dial')}"
                )
            case "hallucination":
                # Check for bonus (all 5 correct)
                if self.state.flags.get("hallucination_correct", 0) == 5:
                    award_points(self.state, SCORE_BONUS,
                                 "Bonus: perfect hallucination detection",
                                 self.display)

    def _check_journal_triggers(self) -> None:
        """Check all journal trigger flags and add entries as needed."""
        for flag, entry_id in JOURNAL_TRIGGERS.items():
            if self.state.flags.get(flag):
                if add_entry(self.state, entry_id):
                    title = JOURNAL_ENTRIES[entry_id]["title"]
                    self.display.print_raw(
                        self.display.journal_text(
                            f"  [Journal updated: {title}]"
                        )
                    )
                    # Check for journal completion bonus
                    if len(self.state.journal_entries) >= 10:
                        if not self.state.flags.get("journal_complete_bonus"):
                            self.state.flags["journal_complete_bonus"] = True
                            award_points(
                                self.state, SCORE_JOURNAL_COMPLETE,
                                "Knowledge journal nearly complete!",
                                self.display,
                            )

    def _trigger_final(self, cmd: Command) -> None:
        """Handle the final puzzle / win condition."""
        # Check prerequisites
        if "temperature_dial" not in self.state.inventory:
            self.display.print(
                "The portal flickers but remains dormant. You feel you "
                "need something from the Sampling Chamber..."
            )
            return

        if len(self.state.journal_entries) < 10:
            count = len(self.state.journal_entries)
            self.display.print(
                f"The portal senses your journal ({count}/10 entries). "
                "'Not enough knowledge yet. Explore more of the model and "
                "learn its secrets.' You need at least 10 journal entries."
            )
            return

        # Final prompt engineering question
        self.display.print(
            "The portal blazes to life, sensing the Temperature Dial and "
            "your nearly-complete journal.\n\n"
            "A voice echoes from the portal:\n"
            "'One final question, researcher. You've walked the path of a "
            "prompt through a transformer. You've seen tokenization, "
            "attention, training, and generation. Now tell me:\n\n"
            "What makes a good prompt for an LLM?'\n\n"
            "  A) Just type whatever you want -- the AI will figure it out.\n\n"
            "  B) Be specific, provide context, state the desired format,\n"
            "     and iterate on your results.\n\n"
            "  C) Use as many words as possible to be thorough.\n\n"
            "  D) Copy and paste the same prompt repeatedly until you get\n"
            "     a good answer.\n\n"
            "Type 'choose' followed by A, B, C, or D."
        )
        self.state.flags["final_question_active"] = True
        self.state.puzzle_states["final"] = "in_progress"

    def handle_final_answer(self, raw: str) -> bool:
        """Handle the final question. Returns True if handled."""
        if not self.state.flags.get("final_question_active"):
            return False

        raw = raw.strip().lower()
        choice = None
        if raw.startswith("choose "):
            choice = raw[7:].strip()
        elif raw in ("a", "b", "c", "d"):
            choice = raw

        if choice is None:
            return False

        if choice == "b":
            award_points(self.state, SCORE_FINAL_QUESTION,
                         "Mastered prompt engineering", self.display)
            self._win_game()
            return True
        elif choice == "a":
            self.display.print(
                "Not quite. LLMs respond much better to clear, specific "
                "prompts with context. 'Figure it out' often leads to "
                "vague or irrelevant responses. Try again!"
            )
            return True
        elif choice == "c":
            self.display.print(
                "More words doesn't mean better prompts. In fact, overly "
                "long prompts can confuse the model. CLARITY and SPECIFICITY "
                "matter more than length. Try again!"
            )
            return True
        elif choice == "d":
            self.display.print(
                "Repeating the same prompt gives you the same distribution "
                "of outputs. ITERATING means refining your prompt based on "
                "what you get back. Try again!"
            )
            return True
        else:
            self.display.print("Choose A, B, C, or D.")
            return True

    def _win_game(self) -> None:
        """End the game with victory."""
        # Add ethics journal entry if they examined the exhibit
        if self.state.flags.get("examined_exhibit"):
            add_entry(self.state, "ethics")

        print(OUTRO_TEXT)
        display_score(self.state, self.display)
        self.display.print_raw("")
        rank = get_rank(self.state.score)
        self.display.print(f"Final Rank: {rank}")
        self.display.print(f"Total Turns: {self.state.turns}")
        self.display.print_raw("")

        # Show journal summary
        self.display.print("Concepts mastered:")
        for entry_id in self.state.journal_entries:
            if entry_id in JOURNAL_ENTRIES:
                title = JOURNAL_ENTRIES[entry_id]["title"]
                self.display.print_raw(f"  - {title}")

        self.display.print_raw("")
        self.display.print(
            "Thank you for playing LLM Adventure! You now understand "
            "the fundamentals of how Large Language Models work."
        )
        self.display.print_raw("")
        self.display.print(
            "Remember: LLMs are powerful tools, not magic. Use them "
            "wisely, verify their outputs, and keep learning."
        )

        self.state.game_over = True
