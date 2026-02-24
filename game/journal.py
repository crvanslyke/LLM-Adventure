"""Knowledge journal system for tracking learned LLM concepts."""

from game.state import GameState
from game.display import Display


JOURNAL_ORDER = [
    "what_are_llms",
    "transformer_architecture",
    "tokenization",
    "embeddings",
    "attention_mechanism",
    "pretraining",
    "finetuning",
    "rlhf_alignment",
    "text_generation",
    "hallucinations_limitations",
    "ethics",
]


def add_entry(state: GameState, entry_id: str) -> bool:
    """Add a journal entry if not already recorded. Returns True if new."""
    if entry_id not in state.journal_entries:
        state.journal_entries.append(entry_id)
        return True
    return False


def display_journal(state: GameState, display: Display,
                     entries_db: dict[str, dict]) -> None:
    """Display the knowledge journal."""
    if not state.journal_entries:
        display.print("Your journal is empty. Explore and examine things "
                       "to learn about LLMs!")
        return

    display.print_raw(display.header("KNOWLEDGE JOURNAL"))
    display.print_raw("")

    for i, entry_id in enumerate(JOURNAL_ORDER, 1):
        if entry_id in state.journal_entries and entry_id in entries_db:
            entry = entries_db[entry_id]
            title = display.journal_text(f"  {i}. {entry['title']}")
            display.print_raw(title)
            display.print(f"     {entry['summary']}")
            display.print_raw("")
        elif entry_id in state.journal_entries:
            display.print_raw(f"  {i}. {entry_id}")
            display.print_raw("")
        else:
            display.print_raw(display.color(f"  {i}. ???", "dim"))
            display.print_raw("")

    discovered = len(state.journal_entries)
    total = len(JOURNAL_ORDER)
    display.print_raw(display.separator())
    display.print(f"Concepts discovered: {discovered}/{total}")
