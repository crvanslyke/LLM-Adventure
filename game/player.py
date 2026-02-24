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

    Tries: exact match, display name match, substring match.
    """
    if not name:
        return None

    name = name.strip().lower().replace(" ", "_")

    # Exact ID match
    if name in candidates:
        return name

    # Display name match
    for cid in candidates:
        if cid in items_db:
            if items_db[cid].name.lower().replace(" ", "_") == name:
                return cid

    # Also try the raw name with spaces
    name_spaced = name.replace("_", " ")

    # Substring match
    matches = []
    for cid in candidates:
        if name in cid or name_spaced in cid:
            matches.append(cid)
        elif cid in items_db:
            item_name_lower = items_db[cid].name.lower()
            if name_spaced in item_name_lower or name in item_name_lower:
                matches.append(cid)

    if len(matches) == 1:
        return matches[0]

    return None
