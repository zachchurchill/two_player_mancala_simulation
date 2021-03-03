import pytest

from mancala.mancala import Player, PlayerRow, get_new_board
from mancala.simulation import (
    ExampleRandomPlayerStrategy,
    PlayerStrategy,
    SimulationLoop,
)


def test_example_random_player_provides_strategy_name():
    assert ExampleRandomPlayerStrategy().strategy_name is not None


def test_example_random_player_strategy_chooses_valid_bins():
    random_strategy = ExampleRandomPlayerStrategy()

    for i in range(6):
        one_nonempty_bin_row = PlayerRow(
            bins=[1 if i == j else 0 for j in range(6)], goal=20
        )
        assert random_strategy.choose_bin(one_nonempty_bin_row) == i

    semi_empty_bin_row = PlayerRow(bins=[1, 0, 1, 0, 1, 0], goal=15)
    assert random_strategy.choose_bin(semi_empty_bin_row) in [0, 2, 4]


def test_example_random_player_strategy_raises_error_for_no_choices():
    random_strategy = ExampleRandomPlayerStrategy()
    with pytest.raises(ValueError):
        random_strategy.choose_bin(PlayerRow(bins=[0, 0, 0, 0, 0, 0], goal=10))


def test_simulation_loops_provides_player_strategies_in_dict_format():
    player_one = ExampleRandomPlayerStrategy()
    player_two = ExampleRandomPlayerStrategy()
    loop = SimulationLoop(player_one=player_one, player_two=player_two)
    assert Player.ONE in loop.player_one
    assert loop.player_one[Player.ONE] == player_one
    assert Player.TWO in loop.player_two
    assert loop.player_two[Player.TWO] == player_two


def test_simulation_loop_sets_up_starting_player_upon_instantiation():
    loop = SimulationLoop(
        player_one=ExampleRandomPlayerStrategy(),
        player_two=ExampleRandomPlayerStrategy(),
    )
    assert loop.starting_player is not None
    assert loop.starting_player.keys() < {Player.ONE, Player.TWO}


def test_simulation_loop_starts_off_with_no_run_and_winning_player():
    loop = SimulationLoop(
        player_one=ExampleRandomPlayerStrategy(),
        player_two=ExampleRandomPlayerStrategy(),
    )
    assert loop.has_run is False
    assert loop.winning_player is None


def test_simulation_loop_starts_with_new_board():
    loop = SimulationLoop(
        player_one=ExampleRandomPlayerStrategy(),
        player_two=ExampleRandomPlayerStrategy(),
    )
    assert len(loop.boards) == 1
    assert loop.boards[0] == get_new_board()


def test_simulation_loop_starts_with_no_turns():
    loop = SimulationLoop(
        player_one=ExampleRandomPlayerStrategy(),
        player_two=ExampleRandomPlayerStrategy(),
    )
    assert len(loop.turns) == 0


def test_simulation_loop_stops_when_goal_is_over_24():
    player_one = ExampleRandomPlayerStrategy()
    player_two = ExampleRandomPlayerStrategy()
    loop = SimulationLoop(player_one=player_one, player_two=player_two)
    assert loop.has_run is False
    assert loop.winning_player is None

    loop.run()
    assert loop.has_run is True
    assert len(loop.turns) > 1
    assert len(loop.boards) > 1

    if loop.winning_player:  # pragma: nocover
        winning_player, *_ = loop.winning_player.keys()
        assert loop.boards[-1][winning_player].goal >= 24
    else:  # pragma: nocover
        last_board = loop.boards[-1]
        assert last_board[Player.ONE].goal == 24
        assert last_board[Player.TWO].goal == 24
