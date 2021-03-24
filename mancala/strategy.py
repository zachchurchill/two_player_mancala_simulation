import random
from abc import ABCMeta, abstractmethod
from typing import Optional

from mancala.mancala import PlayerRow


class PlayerStrategy(metaclass=ABCMeta):
    @property
    @abstractmethod
    def strategy_name(self) -> str:
        """Provide a unique name for the strategy."""

    @abstractmethod
    def choose_bin(
        self, player_row: PlayerRow, opponent_row: Optional[PlayerRow] = None
    ) -> int:
        """Provides the player's bin selection for the Turn."""


class ExampleRandomPlayerStrategy(PlayerStrategy):
    @property
    def strategy_name(self) -> str:
        return "random-selection"

    def choose_bin(
        self, player_row: PlayerRow, opponent_row: Optional[PlayerRow] = None
    ) -> int:
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

    def choose_bin(
        self, player_row: PlayerRow, opponent_row: Optional[PlayerRow] = None
    ) -> int:
        nonempty_bins_with_index = [
            (i, b_i) for i, b_i in enumerate(player_row.bins) if b_i > 0
        ]
        # Return first index with the minimal amount of pieces in bin
        if len(nonempty_bins_with_index) > 0:
            return min(nonempty_bins_with_index, key=lambda item: item[1])[0]
        else:
            raise ValueError("player_row does not contain any non-empty-bins")


class AlwaysMaximumPlayerStrategy(PlayerStrategy):
    @property
    def strategy_name(self) -> str:
        return "always-maximum"

    def choose_bin(
        self, player_row: PlayerRow, opponent_row: Optional[PlayerRow] = None
    ) -> int:
        nonempty_bins_with_index = [
            (i, b_i) for i, b_i in enumerate(player_row.bins) if b_i > 0
        ]
        # Return first index with the maximum amount of pieces in bin
        if len(nonempty_bins_with_index) > 0:
            return max(nonempty_bins_with_index, key=lambda item: item[1])[0]
        else:
            raise ValueError("player_row does not contain any non-empty-bins")


class EvenGoalOrPiecesOnOtherSideStrategy(PlayerStrategy):
    """Custom strategy focused on goal making or shedding pieces.

    This strategy will first try to see if there are any bins that
    contain the correct amount of pieces to make a goal, where the
    first bin to contain such an amount of pieces is chosen. For
    example, if the row is [  5 |  4,  0,  3,  8,  1,  0 ], then
    the strategy would choose bin 2 (zero-indexed) so that a goal is
    scored. Now, if no such bin exists, then the strategy will look
    for the bin that tries to move the most pieces to the opponent's
    row. Assuming the following example above first chose bin 2 to
    score a goal and get another turn, [  6 |  5,  1,  0,  8,  1,  0 ],
    the strategy would then choose bin 0 because although bin 3 would
    put the same number of pieces on the opponent's side (4), the
    strategy chooses the first such bin.

    """

    @property
    def strategy_name(self) -> str:
        return "even-goal-or-more-pieces-to-opponent"

    def choose_bin(
        self, player_row: PlayerRow, opponent_row: Optional[PlayerRow] = None
    ) -> int:
        if all(b_i == 0 for b_i in player_row.bins):
            raise ValueError("player_row does not contain any non-empty-bins")

        goal_making_bins = [
            i for i, b_i in enumerate(player_row.bins) if b_i > 0 and b_i == i + 1
        ]
        if len(goal_making_bins) > 0:
            return goal_making_bins[0]

        number_of_pieces_in_opponents_row = [
            (i, b_i - i - 1) for i, b_i in enumerate(player_row.bins) if b_i > 0
        ]
        return max(number_of_pieces_in_opponents_row, key=lambda item: item[1])[0]


class EvenGoalStealAndPiecesOnOtherSideStrategy(PlayerStrategy):
    """Strategy focused on goal making, steal pieces, and shedding pieces.

    Similar to `EvenGoalOrPiecesOnOtherSideStrategy`, this strategy will
    first try to make a goal. But before trying to put the most pieces on
    the opponent's row, this strategy will check if there are any moves that
    would result in steal pieces from the opponent. Additionally, if there
    are several such moves, then the move that maximizes the pieces stolen
    will be selected. Finally, if neither of the previous move types are an
    option, then a bin will be selected which maximizes the number of pieces
    moved toward/to the opponent's row.

    """

    @property
    def strategy_name(self) -> str:
        return "even-goal-then-stealing-finally-shedding"

    def choose_bin(
        self, player_row: PlayerRow, opponent_row: Optional[PlayerRow] = None
    ) -> int:
        if all(b_i == 0 for b_i in player_row.bins):
            raise ValueError("player_row does not contain any non-empty-bins")
        elif not isinstance(opponent_row, PlayerRow):
            raise ValueError("strategy requires opponent_row be provided")

        # goal making
        goal_making_bins = [
            i for i, b_i in enumerate(player_row.bins) if b_i > 0 and b_i == i + 1
        ]
        if len(goal_making_bins) > 0:
            return goal_making_bins[0]

        # stealing
        potential_stealing_bins = [
            i
            for i, (p_b_i, o_b_i) in enumerate(zip(player_row.bins, opponent_row.bins))
            if p_b_i == 0 and o_b_i > 0
        ]
        move_result_bins = [
            (i, i - b_i)  # if > 0, then this gives resulting bin within player's row
            for i, b_i in enumerate(player_row.bins)
            if b_i > 0
        ]
        stealing_bin_moves = [
            (i, opponent_row.bins[ending_i])
            for i, ending_i in move_result_bins
            if ending_i in potential_stealing_bins
        ]
        if len(stealing_bin_moves) > 0:
            return max(stealing_bin_moves, key=lambda item: item[1])[0]

        # shedding
        number_of_pieces_in_opponents_row = [
            (i, b_i - i - 1) for i, b_i in enumerate(player_row.bins) if b_i > 0
        ]
        return max(number_of_pieces_in_opponents_row, key=lambda item: item[1])[0]
