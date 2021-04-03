# Checking for Voting Machine Fraud in the State of Nevada

This checks for patterns between voter turnout and age in Nevada in the 2020 General Presidential Election.

## Setup

Requires python3.

## Running

1. Obtain voter list. See Data Source.
2. Move and rename the eligible voter list file to `./data/voters.csv`
3. Move and rename the voter history file to `./data/votes.csv`
4. Plot turnout vs. age by running: `./plot_turnout_by_age.py`

## Data source

The Nevada voter list and voter history are free, but you must first request access: https://www.nvsos.gov/sos/elections/voters/nevvoter-statewide-list

Voting machine vendor list: https://www.nvsos.gov/sos/elections/election-resources/voting-system

