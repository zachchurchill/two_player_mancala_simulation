from functools import singledispatch
from typing import Any, Dict, List, Union

from mancala.mancala import Board, Player, PlayerRow, Turn


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
def serialize_player_row(arg: PlayerRow) -> Dict[str, Union[List[int], int]]:
    return {"bins": arg.bins, "goal": arg.goal}


@serialize.register
def serialize_turn(arg: Turn) -> Dict[str, Union[str, int]]:
    return {"player": serialize(arg.player), "selected_bin": arg.selected_bin}


@serialize.register
def serialize_board(arg: Board) -> Dict[str, Dict[str, Union[List[int], int]]]:
    return {serialize(p): serialize(p_row) for p, p_row in arg.items()}
