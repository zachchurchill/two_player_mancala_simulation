#!/usr/bin/env bash

readonly STRATEGIES=(
  "AlwaysMaximumPlayerStrategy"
  "AlwaysMinimumPlayerStrategy"
  "EvenGoalOrPiecesOnOtherSideStrategy"
  "EvenGoalStealAndPiecesOnOtherSideStrategy"
  "ExampleRandomPlayerStrategy"
)

for player_one_strategy in "${STRATEGIES[@]}"
do
  for player_two_strategy in "${STRATEGIES[@]}"
  do
    export MANCALA_PLAYER_ONE="$player_one_strategy"
    export MANCALA_PLAYER_TWO="$player_two_strategy"
    output_file="${player_one_strategy}_vs_${player_two_strategy}.html"
    jupyter nbconvert --execute --to html --output "$output_file" template.ipynb
  done
done
