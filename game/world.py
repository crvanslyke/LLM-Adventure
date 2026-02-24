"""Immutable world definitions: Room, Exit, Item dataclasses."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Exit:
    direction: str
    destination: str
    requires_flag: str | None = None
    requires_item: str | None = None
    locked_message: str = "The way is blocked."


@dataclass(frozen=True)
class Item:
    id: str
    name: str
    description: str
    portable: bool = True
    use_message: str = "You can't use that here."


@dataclass(frozen=True)
class Room:
    id: str
    name: str
    zone: str
    description: str
    exits: tuple[Exit, ...]
    items: tuple[str, ...] = ()
    on_first_visit: str | None = None
    puzzle_id: str | None = None
    examine_targets: dict[str, str] = field(default_factory=dict)
    talk_targets: dict[str, str] = field(default_factory=dict)
