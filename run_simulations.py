import json
from pprint import pprint

from mancala.simulation import SimulationLoop
from mancala.strategy import (
    AlwaysMaximumPlayerStrategy,
    AlwaysMinimumPlayerStrategy,
    EvenGoalOrPiecesOnOtherSideStrategy,
    ExampleRandomPlayerStrategy,
)


def min_vs_min():
    loop = SimulationLoop(
        player_one=AlwaysMinimumPlayerStrategy(),
        player_two=AlwaysMinimumPlayerStrategy(),
    )
    pprint(loop.starting_player)
    loop.run()
    pprint(json.loads(loop.serialize()))


def min_vs_max():
    loop = SimulationLoop(
        player_one=AlwaysMaximumPlayerStrategy(),
        player_two=AlwaysMinimumPlayerStrategy(),
    )
    pprint(loop.starting_player)
    loop.run()
    pprint(json.loads(loop.serialize()))


def max_vs_max():
    loop = SimulationLoop(
        player_one=AlwaysMaximumPlayerStrategy(),
        player_two=AlwaysMaximumPlayerStrategy(),
    )
    pprint(loop.starting_player)
    loop.run()
    pprint(json.loads(loop.serialize()))


def min_vs_even_goal():
    loop = SimulationLoop(
        player_one=AlwaysMinimumPlayerStrategy(),
        player_two=EvenGoalOrPiecesOnOtherSideStrategy(),
    )
    pprint(loop.starting_player)
    loop.run()
    pprint(json.loads(loop.serialize()))


def max_vs_even_goal():
    loop = SimulationLoop(
        player_one=AlwaysMaximumPlayerStrategy(),
        player_two=EvenGoalOrPiecesOnOtherSideStrategy(),
    )
    pprint(loop.starting_player)
    loop.run()
    pprint(json.loads(loop.serialize()))


if __name__ == "__main__":
    min_vs_even_goal()
