import pytest

from mancala.mancala import PlayerRow
from mancala.strategy import (
    AlwaysMaximumPlayerStrategy,
    AlwaysMinimumPlayerStrategy,
    ExampleRandomPlayerStrategy,
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


def test_always_minimum_player_provides_strategy_name():
    assert AlwaysMinimumPlayerStrategy().strategy_name is not None


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


def test_always_minimum_player_strategy_raises_error_for_no_choices():
    always_min_strategy = AlwaysMinimumPlayerStrategy()
    with pytest.raises(ValueError):
        always_min_strategy.choose_bin(PlayerRow(bins=[0, 0, 0, 0, 0, 0], goal=12))


def test_always_maximum_player_provides_strategy_name():
    assert AlwaysMaximumPlayerStrategy().strategy_name is not None


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


def test_always_maximum_player_strategy_raises_error_for_no_choices():
    always_max_strategy = AlwaysMaximumPlayerStrategy()
    with pytest.raises(ValueError):
        always_max_strategy.choose_bin(PlayerRow(bins=[0, 0, 0, 0, 0, 0], goal=12))
