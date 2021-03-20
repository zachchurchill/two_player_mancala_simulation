import random
from typing import Dict, List, Optional

from mancala.mancala import (
    Board,
    Player,
    PlayerRow,
    Turn,
    get_new_board,
    take_turn,
    who_gets_next_turn,
)
from mancala.strategy import PlayerStrategy


class SimulationLoop:
    def __init__(self, player_one: PlayerStrategy, player_two: PlayerStrategy):
        self._strategies = {
            Player.ONE: player_one,
            Player.TWO: player_two,
        }
        self._reset_simulation()

    def _reset_simulation(self) -> None:
        self._has_run = False
        self._starting_player = random.choice([Player.ONE, Player.TWO])
        self._winning_player: Optional[Player] = None
        self._turns: List[Turn] = []
        self._boards = [get_new_board()]

    @property
    def player_one(self) -> Dict[Player, PlayerStrategy]:
        return {Player.ONE: self._strategies[Player.ONE]}

    @property
    def player_two(self) -> Dict[Player, PlayerStrategy]:
        return {Player.TWO: self._strategies[Player.TWO]}

    @property
    def starting_player(self) -> Dict[Player, PlayerStrategy]:
        return {self._starting_player: self._strategies[self._starting_player]}

    @property
    def turns(self) -> List[Turn]:
        return self._turns

    @property
    def boards(self) -> List[Board]:
        return self._boards

    @property
    def has_run(self) -> bool:
        return self._has_run

    @property
    def winning_player(self) -> Optional[Dict[Player, PlayerStrategy]]:
        if self.has_run and self._winning_player is not None:
            return {self._winning_player: self._strategies[self._winning_player]}
        return None

    def _is_end_of_game(self) -> bool:
        """In reality, the first player to get >24 pieces is the winner."""
        latest_board = self.boards[-1]
        return latest_board[Player.ONE].goal > 24 or latest_board[Player.TWO].goal > 24

    def _set_winner(self) -> None:
        latest_board = self.boards[-1]
        if latest_board[Player.ONE].goal > 24:
            self._winning_player = Player.ONE
        elif latest_board[Player.TWO].goal > 24:
            self._winning_player = Player.TWO

    def run(self, reset_simulation=False) -> None:  # pragma: nocover
        if self.has_run and not reset_simulation:
            return
        self._reset_simulation()

        current_player = self._starting_player
        current_turn = 0
        while True:
            # Set up objects for current player on this turn
            current_board = self._boards[current_turn]
            current_player_row = current_board[current_player]
            current_player_strategy = self._strategies[current_player]

            # Allow current player to select a bin from their row, and ensure it is valid
            try:
                selected_bin = current_player_strategy.choose_bin(current_player_row)
            except ValueError:
                # Assuming ValueError is thrown if player can't move, i.e. all bins are empty
                if all([b == 0 for b in current_player_row.bins]):
                    player_one_row = current_board[Player.ONE]
                    player_two_row = current_board[Player.TWO]

                    resulting_player_one_goal = (
                        sum(player_one_row.bins) + player_one_row.goal
                    )
                    resulting_player_two_goal = (
                        sum(player_two_row.bins) + player_two_row.goal
                    )
                    new_board = {
                        Player.ONE: PlayerRow(
                            bins=[0, 0, 0, 0, 0, 0], goal=resulting_player_one_goal
                        ),
                        Player.TWO: PlayerRow(
                            bins=[0, 0, 0, 0, 0, 0], goal=resulting_player_two_goal
                        ),
                    }
                    # self._turns.append(Turn.GameEndingTurn)  TODO
                    self._boards.append(new_board)
                    if resulting_player_one_goal > resulting_player_two_goal:
                        self._winning_player = Player.ONE
                    elif resulting_player_one_goal < resulting_player_two_goal:
                        self._winning_player = Player.TWO
                    else:
                        self._winning_player = None  # tie
                    self._has_run = True
                    break

            if current_player_row.bins[selected_bin] == 0:
                raise ValueError(
                    "Player strategies need to ensure they pick non-empty bins in 'choose_bin'"
                )

            # Perform turn with selected bin and save simulation data
            turn = Turn(current_player, selected_bin)
            new_board = take_turn(current_board, turn)
            self._turns.append(turn)
            self._boards.append(new_board)

            # Check if game has ended; otherwise, update who is up next
            if self._is_end_of_game():
                self._set_winner()
                self._has_run = True
                break
            current_player = who_gets_next_turn(current_board, turn, new_board)
            current_turn += 1
