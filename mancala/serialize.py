from functools import singledispatch
from typing import Any

from mancala.mancala import Player


@singledispatch
def serialize(arg) -> Any:
    raise TypeError(f"serialize not defined for {type(arg)}")


@serialize.register
def _(arg: Player) -> str:
    enum_to_serialized_value = {
        Player.ONE: "one",
        Player.TWO: "two",
    }
    return enum_to_serialized_value[arg]
