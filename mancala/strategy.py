import random
from abc import ABCMeta, abstractmethod

from mancala.mancala import PlayerRow


class PlayerStrategy(metaclass=ABCMeta):
    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """Provide a unique name for the strategy."""

    @abstractmethod
    def choose_bin(self, player_row: PlayerRow) -> int:
        """Provides the player's bin selection for the Turn."""


class ExampleRandomPlayerStrategy(PlayerStrategy):
    @property
    def strategy_name(self) -> str:
        return "random-selection"

    def choose_bin(self, player_row: PlayerRow) -> int:
        nonempty_bins_with_index = [
            (i, b_i) for i, b_i in enumerate(player_row.bins) if b_i > 0
        ]
        if len(nonempty_bins_with_index) > 0:
            return random.choice(nonempty_bins_with_index)[0]
        else:
            raise ValueError("player_row does not contain any non-empty bins")


class AlwaysMinimumPlayerStrategy(PlayerStrategy):
    @property
    def strategy_name(self) -> str:
        return "always-minimum"

    def choose_bin(self, player_row: PlayerRow) -> int:
        nonempty_bins_with_index = [
            (i, b_i) for i, b_i in enumerate(player_row.bins) if b_i > 0
        ]
        # Return first index with the minimal amount of pieces in bin
        if len(nonempty_bins_with_index) > 0:
            return min(nonempty_bins_with_index, key=lambda item: item[1])[0]
        else:
            raise ValueError("player_row does not contain any non-empty-bins")
