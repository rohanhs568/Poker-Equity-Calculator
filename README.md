# Poker Equity Calculator

Monte Carlo hand equity calculator. Input 2 hands and no of trials, returns no of wins each.

## How it works

- **`strength_calculator.py`** evaluates a 7-card hand (2 hole cards + 5 board cards) and returns a single comparable number. Ranks are packed into one integer using base-14 encoding, so two hand strengths can just be compared with `>`.
- **`equity_calculator.py`** runs the simulation. Deals random boards from the remaining deck, evaluates both hands each time using the module above, and tallies wins (splitting ties 0.5/0.5).

## Status

Works for heads-up, all-in equity between two known hands. No range support yet

Follow up idea: Pricer for showing one hand in different setups.
