from dataclasses import dataclass
from enum import Enum
from typing import Dict, List

from mancala.config import NUMBER_OF_BINS, NUMBER_OF_STARTING_PIECES


class Player(Enum):
    ONE = 0
    TWO = 1


def _ensure_bin_selection_is_correct(selected_bin: int) -> None:
    upper_bound = NUMBER_OF_BINS - 1
    if selected_bin < 0 or selected_bin > upper_bound:
        raise ValueError(f"bin must be between 0 and {upper_bound}, inclusive")


@dataclass
class Turn:
    player: Player
    selected_bin: int

    def __post_init__(self):
        _ensure_bin_selection_is_correct(self.selected_bin)


class PlayerRow:
    def __init__(self, bins: List[int], goal: int):
        if len(bins) != NUMBER_OF_BINS:
            raise ValueError(f"bins must be of length {NUMBER_OF_BINS}")
        if not all(b >= 0 for b in bins):
            raise ValueError("All bins must have a non-negative amount of pieces")
        if goal < 0:
            raise ValueError("goal must have a non-negative amount of pieces")

        self._bins = bins
        self._goal = goal

    def __repr__(self) -> str:
        return "[ {:>2} | {} ]".format(
            self.goal, ", ".join(["{:>2}".format(b) for b in self.bins])
        )

    @property
    def bins(self) -> List[int]:
        return self._bins

    @property
    def goal(self) -> int:
        return self._goal

    @classmethod
    def get_new_player_row(cls) -> "PlayerRow":
        return cls(
            bins=[NUMBER_OF_STARTING_PIECES for _ in range(NUMBER_OF_BINS)],
            goal=0,
        )

    def add_pieces_to_goal(self, pieces: int = 1) -> None:
        if pieces <= 0:
            raise ValueError("pieces should be positive")
        self._goal += pieces

    def add_piece_in_bin(self, bin: int) -> None:
        _ensure_bin_selection_is_correct(bin)
        self._bins[bin] += 1
