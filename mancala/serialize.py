from functools import singledispatch
from typing import Any, Dict

from mancala.mancala import Player, PlayerRow


@singledispatch
def serialize(arg) -> Any:
    raise TypeError(f"serialize not defined for {type(arg)}")


@serialize.register
def serialize_player(arg: Player) -> str:
    enum_to_serialized_value = {
        Player.ONE: "one",
        Player.TWO: "two",
    }
    return enum_to_serialized_value[arg]


@serialize.register
def serialize_player_row(arg: PlayerRow) -> Dict[str, Any]:
    return {"bins": arg.bins, "goal": arg.goal}
