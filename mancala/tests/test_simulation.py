import pytest

from mancala.mancala import Player, PlayerRow, get_new_board
from mancala.simulation import SimulationLoop
from mancala.strategy import ExampleRandomPlayerStrategy


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
