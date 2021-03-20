import pytest

from mancala.mancala import Board, Player, PlayerRow, Turn
from mancala.serialize import to_serializable


def test_serialize_returns_type_error_for_unregistered_type():
    class NewType:
        pass

    with pytest.raises(TypeError):
        to_serializable(NewType())


@pytest.mark.parametrize(
    "serializable,serialized",
    [
        (None, None),
        (Player.ONE, "one"),
        (Player.TWO, "two"),
        (
            PlayerRow.get_new_player_row(),
            {
                "bins": PlayerRow.get_new_player_row().bins,
                "goal": PlayerRow.get_new_player_row().goal,
            },
        ),
        (Turn(Player.ONE, 4), {"player": "one", "selected_bin": 4}),
        (Turn(Player.TWO, 2), {"player": "two", "selected_bin": 2}),
    ],
)
def test_serialize_returns_correct_serialization(serializable, serialized):
    assert to_serializable(serializable) == serialized


def test_serialization_returns_correct_serialization_for_boards():
    p1 = Player.ONE
    p1_row = PlayerRow.get_new_player_row()
    p2 = Player.TWO
    p2_row = PlayerRow.get_new_player_row()
    board = Board({p1: p1_row, p2: p2_row})
    assert to_serializable(board) == {
        to_serializable(p1): to_serializable(p1_row),
        to_serializable(p2): to_serializable(p2_row),
    }
