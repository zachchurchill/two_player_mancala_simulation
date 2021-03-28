#!/usr/bin/env bash

readonly STRATEGIES=(
  "AlwaysMaximumPlayerStrategy"
  "AlwaysMinimumPlayerStrategy"
  "EvenGoalOrPiecesOnOtherSideStrategy"
  "EvenGoalStealAndPiecesOnOtherSideStrategy"
  "ExampleRandomPlayerStrategy"
)
strategies_length=${#STRATEGIES[@]}

for (( i=0; i<$strategies_length; i++ ))
do
  player_one_strategy="${STRATEGIES[$i]}"
  for (( j=$i; j<$strategies_length; j++ ))
  do
    player_two_strategy="${STRATEGIES[$j]}"

    export MANCALA_PLAYER_ONE="$player_one_strategy"
    export MANCALA_PLAYER_TWO="$player_two_strategy"
    output_file="${player_one_strategy}_vs_${player_two_strategy}.html"
    jupyter nbconvert --execute --to html --output "$output_file" template.ipynb
  done
done
