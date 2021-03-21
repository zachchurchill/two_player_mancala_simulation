from typing import List

import pytest

from mancala.mancala import PlayerRow
from mancala.strategy import (
    AlwaysMaximumPlayerStrategy,
    AlwaysMinimumPlayerStrategy,
    EvenGoalOrPiecesOnOtherSideStrategy,
    ExampleRandomPlayerStrategy,
    PlayerStrategy,
)


def _get_all_strategies() -> List[PlayerStrategy]:
    return [
        AlwaysMaximumPlayerStrategy(),
        AlwaysMinimumPlayerStrategy(),
        EvenGoalOrPiecesOnOtherSideStrategy(),
        ExampleRandomPlayerStrategy(),
    ]


@pytest.mark.parametrize("strategy", _get_all_strategies())
def test_player_strategy_provides_strategy_name(strategy):
    assert strategy.strategy_name is not None


@pytest.mark.parametrize("strategy", _get_all_strategies())
def test_player_strategy_raises_error_for_no_choices(strategy):
    with pytest.raises(ValueError):
        strategy.choose_bin(PlayerRow(bins=[0, 0, 0, 0, 0, 0], goal=10))


def test_example_random_player_strategy_chooses_valid_bins():
    random_strategy = ExampleRandomPlayerStrategy()

    for i in range(6):
        one_nonempty_bin_row = PlayerRow(
            bins=[1 if i == j else 0 for j in range(6)], goal=20
        )
        assert random_strategy.choose_bin(one_nonempty_bin_row) == i

    semi_empty_bin_row = PlayerRow(bins=[1, 0, 1, 0, 1, 0], goal=15)
    assert random_strategy.choose_bin(semi_empty_bin_row) in [0, 2, 4]


def test_always_minimum_player_strategy_chooses_bin_with_least_pieces():
    always_min_strategy = AlwaysMinimumPlayerStrategy()

    for i in range(6):
        one_nonempty_bin_row = PlayerRow(
            bins=[1 if i == j else 0 for j in range(6)], goal=20
        )
        assert always_min_strategy.choose_bin(one_nonempty_bin_row) == i

    all_ones_row = PlayerRow(bins=[1, 1, 1, 1, 1, 1], goal=15)
    assert always_min_strategy.choose_bin(all_ones_row) == 0

    two_ones_at_end_of_row = PlayerRow(bins=[2, 0, 4, 3, 1, 1], goal=12)
    assert always_min_strategy.choose_bin(two_ones_at_end_of_row) == 4


def test_always_maximum_player_strategy_chooses_bin_with_least_pieces():
    always_max_strategy = AlwaysMaximumPlayerStrategy()

    for i in range(6):
        one_nonempty_bin_row = PlayerRow(
            bins=[1 if i == j else 0 for j in range(6)], goal=20
        )
        assert always_max_strategy.choose_bin(one_nonempty_bin_row) == i

    all_ones_row = PlayerRow(bins=[1, 1, 1, 1, 1, 1], goal=15)
    assert always_max_strategy.choose_bin(all_ones_row) == 0

    two_sixes_at_end_of_row = PlayerRow(bins=[1, 0, 4, 3, 6, 6], goal=7)
    assert always_max_strategy.choose_bin(two_sixes_at_end_of_row) == 4


def test_even_goal_strategy_chooses_bin_with_goal_making_moves():
    even_goal_strategy = EvenGoalOrPiecesOnOtherSideStrategy()

    for i in range(6):
        chosen_bin = even_goal_strategy.choose_bin(
            PlayerRow(bins=[(i + 1) if i == j else 0 for j in range(6)], goal=0)
        )
        assert chosen_bin == i

    documentation_example_row = PlayerRow(bins=[4, 0, 3, 8, 1, 0], goal=5)
    assert even_goal_strategy.choose_bin(documentation_example_row) == 2


@pytest.mark.parametrize(
    "bins,expected_selection",
    [
        ([5, 1, 0, 8, 1, 0], 0),
        ([4, 1, 0, 8, 1, 0], 3),
        ([0, 0, 1, 0, 2, 1], 2),
        ([0, 0, 1, 2, 0, 1], 2),
        ([0, 0, 1, 3, 0, 1], 3),
        ([0, 0, 0, 0, 0, 1], 5),
    ],
)
def test_even_goal_strategy_chooses_bin_with_max_opponent_pieces(
    bins, expected_selection
):
    even_goal_strategy = EvenGoalOrPiecesOnOtherSideStrategy()
    assert (
        even_goal_strategy.choose_bin(PlayerRow(bins=bins, goal=0))
        == expected_selection
    )
