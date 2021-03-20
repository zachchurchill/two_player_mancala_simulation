import pytest

from mancala.config import NUMBER_OF_BINS, NUMBER_OF_STARTING_PIECES
from mancala.mancala import (
    Player,
    PlayerRow,
    Turn,
    get_new_board,
    take_turn,
    who_gets_next_turn,
)


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


@pytest.mark.parametrize(
    "selected_bin,players_result_row,opponents_result_row",
    [
        (
            0,
            PlayerRow([0, 4, 4, 4, 4, 4], 1),
            PlayerRow([4, 4, 4, 5, 5, 5], 0),
        ),
        (
            1,
            PlayerRow([5, 0, 4, 4, 4, 4], 1),
            PlayerRow([4, 4, 4, 4, 5, 5], 0),
        ),
        (
            2,
            PlayerRow([5, 5, 0, 4, 4, 4], 1),
            PlayerRow([4, 4, 4, 4, 4, 5], 0),
        ),
        (
            3,
            PlayerRow([5, 5, 5, 0, 4, 4], 1),
            PlayerRow.get_new_player_row(),
        ),
        (
            4,
            PlayerRow([5, 5, 5, 5, 0, 4], 0),
            PlayerRow.get_new_player_row(),
        ),
        (
            5,
            PlayerRow([4, 5, 5, 5, 5, 0], 0),
            PlayerRow.get_new_player_row(),
        ),
    ],
)
def test_first_moves_on_a_new_game_board(
    selected_bin, players_result_row, opponents_result_row
):
    # Ensure the turn works for both Players, and that the function
    # does not change the original board
    player_one_turn_board = get_new_board()
    player_one_turn = Turn(Player.ONE, selected_bin)
    new_player_one_turn_board = take_turn(player_one_turn_board, player_one_turn)
    assert player_one_turn_board == get_new_board()
    assert new_player_one_turn_board[Player.ONE] == players_result_row
    assert new_player_one_turn_board[Player.TWO] == opponents_result_row

    player_two_turn_board = get_new_board()
    player_two_turn = Turn(Player.TWO, selected_bin)
    new_player_two_turn_board = take_turn(player_two_turn_board, player_two_turn)
    assert player_two_turn_board == get_new_board()
    assert new_player_two_turn_board[Player.ONE] == opponents_result_row
    assert new_player_two_turn_board[Player.TWO] == players_result_row


@pytest.mark.parametrize(
    "player,opponent", [(Player.ONE, Player.TWO), (Player.TWO, Player.ONE)]
)
def test_double_wrap_turn(player, opponent):
    turn = Turn(player, 1)
    board = {
        player: PlayerRow(bins=[0, 10, 0, 0, 2, 0], goal=12),
        opponent: PlayerRow(bins=[1, 6, 8, 0, 2, 7], goal=3),
    }

    new_board = take_turn(board, turn)

    assert new_board[player] == PlayerRow(bins=[1, 0, 0, 0, 3, 1], goal=13)
    assert new_board[opponent] == PlayerRow(bins=[2, 7, 9, 1, 3, 8], goal=3)


@pytest.mark.parametrize(
    "player,opponent", [(Player.ONE, Player.TWO), (Player.TWO, Player.ONE)]
)
def test_double_wrap_turn_that_ends_in_goal(player, opponent):
    turn = Turn(player, 0)
    board = {
        player: PlayerRow(bins=[14, 0, 0, 0, 2, 0], goal=10),
        opponent: PlayerRow(bins=[1, 6, 4, 0, 1, 7], goal=3),
    }

    new_board = take_turn(board, turn)

    assert new_board[player] == PlayerRow(bins=[1, 1, 1, 1, 3, 1], goal=12)
    assert new_board[opponent] == PlayerRow(bins=[2, 7, 5, 1, 2, 8], goal=3)


@pytest.mark.parametrize(
    "player,opponent", [(Player.ONE, Player.TWO), (Player.TWO, Player.ONE)]
)
def test_triple_wrap_turn(player, opponent):
    turn = Turn(player, 0)
    board = {
        player: PlayerRow(bins=[16, 1, 5, 0, 5, 2], goal=6),
        opponent: PlayerRow(bins=[0, 2, 1, 2, 1, 0], goal=7),
    }

    new_board = take_turn(board, turn)

    assert new_board[player] == PlayerRow(bins=[1, 2, 6, 1, 6, 3], goal=8)
    assert new_board[opponent] == PlayerRow(bins=[1, 3, 2, 3, 3, 2], goal=7)


@pytest.mark.parametrize(
    "player,opponent", [(Player.ONE, Player.TWO), (Player.TWO, Player.ONE)]
)
def test_last_piece_in_empty_bin_steals_opponents_pieces(player, opponent):
    """
    The idea here is that if a player takes a turn that results
    in their last piece landing in a previously empty bin on their side,
    then the player gets to steal the pieces in the same bin on their
    opponents side. Both the last piece that landed in the previously empty
    bin and their opponents pieces go into the player's goal.
    """
    board = {
        player: PlayerRow(bins=[0, 10, 0, 0, 0, 2], goal=12),
        opponent: PlayerRow(bins=[1, 6, 7, 1, 2, 7], goal=3),
    }

    # In-player row scenario
    in_player_row_board = take_turn(board, Turn(player, 5))
    assert in_player_row_board[player] == PlayerRow(bins=[0, 10, 0, 0, 1, 0], goal=14)
    assert in_player_row_board[opponent] == PlayerRow(bins=[1, 6, 7, 0, 2, 7], goal=3)

    # Double-wrap scenario
    double_wrap_board = take_turn(board, Turn(player, 1))
    assert double_wrap_board[player] == PlayerRow(bins=[1, 0, 0, 0, 0, 3], goal=17)
    assert double_wrap_board[opponent] == PlayerRow(bins=[2, 7, 8, 2, 0, 8], goal=3)


@pytest.mark.parametrize(
    "player,opponent", [(Player.ONE, Player.TWO), (Player.TWO, Player.ONE)]
)
def test_last_piece_in_empty_bin_only_steals_if_opponent_has_pieces(player, opponent):
    board = {
        player: PlayerRow(bins=[0, 10, 0, 0, 0, 2], goal=12),
        opponent: PlayerRow(bins=[1, 6, 7, 0, 3, 7], goal=3),
    }
    new_board = take_turn(board, Turn(player, 5))
    assert new_board[player] == PlayerRow(bins=[0, 10, 0, 1, 1, 0], goal=12)
    assert new_board[opponent] == PlayerRow(bins=[1, 6, 7, 0, 3, 7], goal=3)


@pytest.mark.parametrize(
    "player,opponent", [(Player.ONE, Player.TWO), (Player.TWO, Player.ONE)]
)
def test_who_gets_next_turn_returns_correct_player(player, opponent):
    # player makes optimal first game move to get another turn
    prior_board = {
        player: PlayerRow(bins=[4, 4, 4, 4, 4, 4], goal=0),
        opponent: PlayerRow(bins=[4, 4, 4, 4, 4, 4], goal=0),
    }
    turn = Turn(player, 3)
    new_board = {
        player: PlayerRow(bins=[5, 5, 5, 0, 4, 4], goal=1),
        opponent: PlayerRow.get_new_player_row(),
    }
    assert who_gets_next_turn(prior_board, turn, new_board) == player

    # player makes a move to steal pieces from opponent
    prior_board = {
        player: PlayerRow(bins=[0, 10, 0, 0, 0, 2], goal=12),
        opponent: PlayerRow(bins=[1, 6, 7, 1, 2, 7], goal=3),
    }
    turn = Turn(player, 5)
    new_board = {
        player: PlayerRow(bins=[0, 10, 0, 0, 1, 0], goal=14),
        opponent: PlayerRow(bins=[1, 6, 7, 0, 2, 7], goal=3),
    }
    assert who_gets_next_turn(prior_board, turn, new_board) == opponent

    # player makes double-wrap move to steal pieces from opponent
    prior_board = {
        player: PlayerRow(bins=[0, 10, 0, 0, 0, 2], goal=12),
        opponent: PlayerRow(bins=[1, 6, 7, 1, 2, 7], goal=3),
    }
    turn = Turn(player, 1)
    new_board = {
        player: PlayerRow(bins=[1, 0, 0, 0, 0, 3], goal=17),
        opponent: PlayerRow(bins=[2, 7, 8, 2, 0, 8], goal=3),
    }
    assert who_gets_next_turn(prior_board, turn, new_board) == opponent

    # player makes double-wrap move and ends in goal
    prior_board = {
        player: PlayerRow(bins=[14, 0, 0, 0, 2, 0], goal=10),
        opponent: PlayerRow(bins=[1, 6, 4, 0, 1, 7], goal=3),
    }
    turn = Turn(player, 0)
    new_board = {
        player: PlayerRow(bins=[1, 1, 1, 1, 3, 1], goal=12),
        opponent: PlayerRow(bins=[2, 7, 5, 1, 2, 8], goal=3),
    }
    assert who_gets_next_turn(prior_board, turn, new_board) == player
