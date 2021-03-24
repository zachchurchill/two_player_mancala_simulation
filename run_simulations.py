import json
from pprint import pprint
from typing import Optional

from mancala.mancala import Player
from mancala.simulation import SimulationLoop
from mancala.strategy import (
    AlwaysMaximumPlayerStrategy,
    AlwaysMinimumPlayerStrategy,
    EvenGoalOrPiecesOnOtherSideStrategy,
    EvenGoalStealAndPiecesOnOtherSideStrategy,
    ExampleRandomPlayerStrategy,
)


def min_vs_min(starting_player: Optional[Player] = None):
    loop = SimulationLoop(
        player_one=AlwaysMinimumPlayerStrategy(),
        player_two=AlwaysMinimumPlayerStrategy(),
        starting_player=starting_player,
    )
    print(f"Starting player: {loop.starting_player}")
    loop.run()
    pprint(json.loads(loop.serialize()))
    print()


def min_vs_max(starting_player: Optional[Player] = None):
    loop = SimulationLoop(
        player_one=AlwaysMaximumPlayerStrategy(),
        player_two=AlwaysMinimumPlayerStrategy(),
        starting_player=starting_player,
    )
    print(f"Starting player: {loop.starting_player}")
    loop.run()
    pprint(json.loads(loop.serialize()))
    print()


def max_vs_max(starting_player: Optional[Player] = None):
    loop = SimulationLoop(
        player_one=AlwaysMaximumPlayerStrategy(),
        player_two=AlwaysMaximumPlayerStrategy(),
        starting_player=starting_player,
    )
    print(f"Starting player: {loop.starting_player}")
    loop.run()
    pprint(json.loads(loop.serialize()))
    print()


def min_vs_even_goal(starting_player: Optional[Player] = None):
    loop = SimulationLoop(
        player_one=AlwaysMinimumPlayerStrategy(),
        player_two=EvenGoalOrPiecesOnOtherSideStrategy(),
        starting_player=starting_player,
    )
    print(f"Starting player: {loop.starting_player}")
    loop.run()
    pprint(json.loads(loop.serialize()))
    print()


def max_vs_even_goal(starting_player: Optional[Player] = None):
    loop = SimulationLoop(
        player_one=AlwaysMaximumPlayerStrategy(),
        player_two=EvenGoalOrPiecesOnOtherSideStrategy(),
        starting_player=starting_player,
    )
    print(f"Starting player: {loop.starting_player}")
    loop.run()
    pprint(json.loads(loop.serialize()))
    print()


def even_goal_vs_even_stealing_shedding(starting_player: Optional[Player] = None):
    loop = SimulationLoop(
        player_one=EvenGoalOrPiecesOnOtherSideStrategy(),
        player_two=EvenGoalStealAndPiecesOnOtherSideStrategy(),
        starting_player=starting_player,
    )
    print(f"Starting player: {loop.starting_player}")
    loop.run()
    pprint(json.loads(loop.serialize()))
    print()


if __name__ == "__main__":
    even_goal_vs_even_stealing_shedding(Player.ONE)
    even_goal_vs_even_stealing_shedding(Player.TWO)
