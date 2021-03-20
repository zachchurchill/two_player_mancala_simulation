import pytest

from mancala.mancala import PlayerRow
from mancala.strategy import ExampleRandomPlayerStrategy


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
