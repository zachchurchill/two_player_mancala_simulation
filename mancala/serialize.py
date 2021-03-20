from functools import singledispatch
from typing import Any, Dict, List, Union

from mancala.mancala import Board, Player, PlayerRow, Turn


@singledispatch
def to_serializable(arg) -> Any:
    raise TypeError(f"to_serializable not defined for {type(arg)}")


@to_serializable.register
def to_serializable_none(arg: None) -> None:
    return None


@to_serializable.register
def to_serializable_player(arg: Player) -> str:
    enum_to_to_serializabled_value = {
        Player.ONE: "one",
        Player.TWO: "two",
    }
    return enum_to_to_serializabled_value[arg]


@to_serializable.register
def to_serializable_player_row(arg: PlayerRow) -> Dict[str, Union[List[int], int]]:
    return {"bins": arg.bins, "goal": arg.goal}


@to_serializable.register
def to_serializable_turn(arg: Turn) -> Dict[str, Union[str, int]]:
    return {"player": to_serializable(arg.player), "selected_bin": arg.selected_bin}


@to_serializable.register
def to_serializable_board(arg: Board) -> Dict[str, Dict[str, Union[List[int], int]]]:
    return {to_serializable(p): to_serializable(p_row) for p, p_row in arg.items()}
