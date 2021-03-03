import random
from abc import ABCMeta, abstractmethod

from mancala.mancala import PlayerRow


class PlayerStrategy(metaclass=ABCMeta):
    @abstractmethod
    def choose_bin(self, player_row: PlayerRow) -> int:
        """Provides the player's bin selection for the Turn."""


class ExampleRandomPlayerStrategy(PlayerStrategy):
    def choose_bin(self, player_row: PlayerRow) -> int:
        nonempty_bins_with_index = [
            (i, b_i) for i, b_i in enumerate(player_row.bins) if b_i > 0
        ]
        if len(nonempty_bins_with_index) > 0:
            return random.choice(nonempty_bins_with_index)[0]
        else:
            raise ValueError("player_row does not contain any non-empty bins")
