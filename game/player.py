"""Player-related operations: inventory, movement validation."""

from game.state import GameState
from game.world import Room, Item


def can_move(state: GameState, room: Room, direction: str) -> tuple[bool, str]:
    """Check if the player can move in a direction. Returns (can_move, message)."""
    for exit_ in room.exits:
        if exit_.direction == direction:
            if exit_.requires_flag and not state.flags.get(exit_.requires_flag):
                return False, exit_.locked_message
            if exit_.requires_item and exit_.requires_item not in state.inventory:
                return False, exit_.locked_message
            return True, exit_.destination
    available = [e.direction for e in room.exits]
    return False, f"There is no exit to the {direction}. Exits: {', '.join(available)}."


def has_item(state: GameState, item_id: str) -> bool:
    return item_id in state.inventory


def add_item(state: GameState, item_id: str) -> None:
    if item_id not in state.inventory:
        state.inventory.append(item_id)


def remove_item(state: GameState, item_id: str) -> bool:
    if item_id in state.inventory:
        state.inventory.remove(item_id)
        return True
    return False


def items_in_current_room(state: GameState) -> list[str]:
    return state.items_in_rooms.get(state.current_room, [])


def take_item_from_room(state: GameState, item_id: str) -> bool:
    room_items = state.items_in_rooms.get(state.current_room, [])
    if item_id in room_items:
        room_items.remove(item_id)
        add_item(state, item_id)
        return True
    return False


def drop_item_in_room(state: GameState, item_id: str) -> bool:
    if remove_item(state, item_id):
        if state.current_room not in state.items_in_rooms:
            state.items_in_rooms[state.current_room] = []
        state.items_in_rooms[state.current_room].append(item_id)
        return True
    return False


def resolve_item_name(name: str, candidates: list[str],
                       items_db: dict[str, Item]) -> str | None:
    """Resolve a player-typed item name to an item ID.

    Tries (in order): exact ID match, display name match, substring match.
    Handles spaces, underscores, and partial names flexibly.
    """
    if not name:
        return None

    raw = name.strip().lower()
    underscored = raw.replace(" ", "_")
    spaced = raw.replace("_", " ")

    # 1. Exact ID match (with underscores)
    if underscored in candidates:
        return underscored

    # 2. Exact display name match
    for cid in candidates:
        if cid in items_db:
            display = items_db[cid].name.lower()
            if display == spaced or display.replace(" ", "_") == underscored:
                return cid

    # 3. Substring match on both ID and display name
    matches = []
    for cid in candidates:
        # Check against the item ID
        if underscored in cid or spaced in cid:
            matches.append(cid)
            continue
        # Check against the display name
        if cid in items_db:
            display = items_db[cid].name.lower()
            if spaced in display or underscored in display:
                matches.append(cid)
                continue
            # Also check if any significant word matches
            name_words = set(spaced.split())
            display_words = set(display.split())
            # If all typed words appear in the display name, it's a match
            if name_words and name_words.issubset(display_words):
                matches.append(cid)

    if len(matches) == 1:
        return matches[0]

    # 4. If multiple matches, prefer the one that's an exact substring
    if len(matches) > 1:
        for m in matches:
            if underscored == m:
                return m
            if m in items_db and items_db[m].name.lower() == spaced:
                return m
        # Return the first match as a fallback
        return matches[0]

    return None
