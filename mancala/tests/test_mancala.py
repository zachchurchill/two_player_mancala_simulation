import pytest

from mancala.config import NUMBER_OF_BINS, NUMBER_OF_STARTING_PIECES
from mancala.mancala import Player, PlayerRow, Turn, get_new_board


@pytest.mark.parametrize("player", Player)
def test_turn_selected_bin_must_exist_on_board(player):
    with pytest.raises(ValueError):
        Turn(player, -1)

    with pytest.raises(ValueError):
        Turn(player, NUMBER_OF_BINS)

    for selected_bin in range(NUMBER_OF_BINS):
        assert Turn(player, selected_bin) is not None


def test_player_row_needs_number_of_bins_equal_to_game_config():
    with pytest.raises(ValueError):
        PlayerRow(bins=[], goal=0)

    with pytest.raises(ValueError):
        PlayerRow(
            bins=[NUMBER_OF_STARTING_PIECES for _ in range(NUMBER_OF_BINS + 1)],
            goal=0,
        )

    assert (
        PlayerRow(
            bins=[NUMBER_OF_STARTING_PIECES for _ in range(NUMBER_OF_BINS)],
            goal=0,
        )
        is not None
    )


def test_player_row_requires_non_negative_entries():
    with pytest.raises(ValueError):
        PlayerRow(bins=[-1 for _ in range(NUMBER_OF_BINS)], goal=0)

    with pytest.raises(ValueError):
        PlayerRow(
            bins=[NUMBER_OF_STARTING_PIECES for _ in range(NUMBER_OF_BINS)],
            goal=-1,
        )

    assert PlayerRow(bins=[0 for _ in range(NUMBER_OF_BINS)], goal=0) is not None


def test_player_row_provides_convenience_function_for_new_row():
    assert hasattr(PlayerRow, "get_new_player_row")
    new_player_row = PlayerRow.get_new_player_row()
    assert new_player_row.bins == [
        NUMBER_OF_STARTING_PIECES for _ in range(NUMBER_OF_BINS)
    ]
    assert new_player_row.goal == 0


def test_player_row_provides_method_to_add_pieces_to_goal():
    player_row = PlayerRow(bins=[4, 4, 4, 4, 4, 4], goal=0)
    player_row.add_pieces_to_goal(5)
    assert player_row.goal == 5

    player_row.add_pieces_to_goal(3)
    assert player_row.goal == 8


def test_player_row_add_pieces_to_goal_defaults_to_one():
    player_row = PlayerRow(bins=[4, 4, 4, 4, 4, 4], goal=0)
    player_row.add_pieces_to_goal()
    assert player_row.goal == 1


def test_player_row_cannot_add_non_positive_pieces_to_goal():
    player_row = PlayerRow.get_new_player_row()
    with pytest.raises(ValueError):
        player_row.add_pieces_to_goal(-1)
    with pytest.raises(ValueError):
        player_row.add_pieces_to_goal(0)


def test_player_row_provides_method_to_pieces_to_bins():
    player_row = PlayerRow(bins=[4, 4, 4, 4, 4, 4], goal=0)
    for b in range(len(player_row.bins)):
        player_row.add_piece_in_bin(b)
        assert player_row.bins[b] == 5

        player_row.add_piece_in_bin(b)
        assert player_row.bins[b] == 6


def test_player_row_add_pieces_to_bin_must_be_correct_bin_selection():
    new_player_row = PlayerRow.get_new_player_row()
    with pytest.raises(ValueError):
        new_player_row.add_piece_in_bin(-1)
    with pytest.raises(ValueError):
        new_player_row.add_piece_in_bin(NUMBER_OF_BINS)


def test_player_row_provides_nice_representation():
    new_player_row = PlayerRow.get_new_player_row()
    assert repr(new_player_row) == "[  0 |  4,  4,  4,  4,  4,  4 ]"

    player_row = PlayerRow([12, 0, 1, 9, 10, 4], goal=10)
    assert repr(player_row) == "[ 10 | 12,  0,  1,  9, 10,  4 ]"


def test_player_row_provides_equality_operations():
    player_row = PlayerRow(bins=[1, 2, 3, 4, 5, 6], goal=7)
    identical_player_row = PlayerRow(bins=[1, 2, 3, 4, 5, 6], goal=7)
    assert player_row == identical_player_row
    assert player_row != PlayerRow(bins=[6, 5, 4, 3, 2, 1], goal=7)
    assert player_row != 42


def test_get_new_game_board_provides_new_player_rows():
    new_board = get_new_board()
    assert Player.ONE in new_board.keys() and Player.TWO in new_board.keys()
    assert all(
        [
            player_row == PlayerRow.get_new_player_row()
            for player_row in new_board.values()
        ]
    )
