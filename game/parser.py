"""Command parsing: converts raw input into structured Command objects."""

from dataclasses import dataclass


@dataclass
class Command:
    verb: str
    noun: str | None = None
    preposition: str | None = None
    indirect: str | None = None


# Direction aliases
DIRECTION_ALIASES: dict[str, str] = {
    "n": "north", "s": "south", "e": "east", "w": "west",
    "u": "up", "d": "down",
    "ne": "northeast", "nw": "northwest",
    "se": "southeast", "sw": "southwest",
}

DIRECTIONS = set(DIRECTION_ALIASES.values()) | set(DIRECTION_ALIASES.keys())

# Verb aliases
VERB_ALIASES: dict[str, str] = {
    "l": "look",
    "x": "examine",
    "inspect": "examine",
    "i": "inventory",
    "inv": "inventory",
    "get": "take",
    "grab": "take",
    "h": "help",
    "?": "help",
    "q": "quit",
    "exit": "quit",
    "j": "journal",
    "notes": "journal",
    "log": "journal",
    "sc": "score",
    "restore": "load",
    "speak": "talk",
    "ask": "talk",
    "select": "choose",
    "pick": "choose",
    "read": "examine",
}

# No-argument commands
SOLO_VERBS = {"look", "inventory", "help", "quit", "score", "journal", "about",
              "save", "load"}


def normalize_direction(word: str) -> str:
    return DIRECTION_ALIASES.get(word, word)


def parse(raw: str) -> Command:
    """Parse raw input into a structured Command."""
    raw = raw.strip().lower()
    if not raw:
        return Command(verb="empty")

    tokens = raw.split()

    # Normalize first token through alias map
    first = VERB_ALIASES.get(tokens[0], tokens[0])

    # Bare direction word -> go <direction>
    if first in DIRECTIONS or tokens[0] in DIRECTIONS:
        direction = normalize_direction(tokens[0])
        return Command(verb="go", noun=direction)

    # Solo verbs
    if first in SOLO_VERBS and len(tokens) == 1:
        return Command(verb=first)
    if first in SOLO_VERBS and len(tokens) > 1:
        # e.g. "look at X" -> treat as examine
        if first == "look" and len(tokens) >= 2:
            if tokens[1] == "at" and len(tokens) > 2:
                return Command(verb="examine", noun=" ".join(tokens[2:]))
            elif tokens[1] != "at":
                return Command(verb="examine", noun=" ".join(tokens[1:]))
        return Command(verb=first)

    # "go <direction>"
    if first == "go" and len(tokens) >= 2:
        direction = normalize_direction(VERB_ALIASES.get(tokens[1], tokens[1]))
        return Command(verb="go", noun=direction)

    # "talk to <npc>"
    if first == "talk" and len(tokens) >= 3 and tokens[1] == "to":
        return Command(verb="talk", noun=" ".join(tokens[2:]))
    if first == "talk" and len(tokens) >= 2:
        return Command(verb="talk", noun=" ".join(tokens[1:]))

    # "pick up <item>" special case
    if tokens[0] == "pick" and len(tokens) >= 3 and tokens[1] == "up":
        return Command(verb="take", noun=" ".join(tokens[2:]))

    # "put down <item>"
    if tokens[0] == "put" and len(tokens) >= 3 and tokens[1] == "down":
        return Command(verb="drop", noun=" ".join(tokens[2:]))

    # Commands with prepositions: "use X on Y", "place X on Y", "put X on Y"
    if first in ("use", "place", "put") and len(tokens) >= 4:
        # Find the preposition
        for i, t in enumerate(tokens[1:], 1):
            if t in ("on", "with", "at", "in"):
                noun = " ".join(tokens[1:i])
                indirect = " ".join(tokens[i + 1:])
                return Command(verb=first, noun=noun,
                               preposition=t, indirect=indirect)

    # "set <dial> <value>" for sampling puzzle
    if first == "set" and len(tokens) >= 3:
        return Command(verb="set", noun=tokens[1],
                        preposition="to", indirect=" ".join(tokens[2:]))

    # "pull lever" / "pull"
    if first == "pull":
        noun = " ".join(tokens[1:]) if len(tokens) > 1 else None
        return Command(verb="pull", noun=noun)

    # "tag <number> <label>" for hallucination puzzle
    if first == "tag" and len(tokens) >= 3:
        return Command(verb="tag", noun=tokens[1],
                        preposition=None, indirect=" ".join(tokens[2:]))

    # "choose <option>"
    if first == "choose" and len(tokens) >= 2:
        return Command(verb="choose", noun=" ".join(tokens[1:]))

    # General verb + noun
    verb = first
    noun = " ".join(tokens[1:]) if len(tokens) > 1 else None

    return Command(verb=verb, noun=noun)
