from strength_calculator import base14, hand_strength_calculator

rank = [0,1,2,3,4,5,6,7,8,9,10,11,12] 
suit = [0, 1, 2, 3]

from itertools import product
deck = list(product(rank,suit))

import random

def equity_calculator(hand1, hand2, no_of_trials):
    hand1_wins = 0
    hand2_wins = 0

    deck = list(product(rank, suit))

    for card in hand1:
        deck.remove(card)
    for card in hand2:
        deck.remove(card)

    for _ in range(no_of_trials):
        board = random.sample(deck, 5)

        hand1_strength = hand_strength_calculator(hand1, board)
        hand2_strength = hand_strength_calculator(hand2, board)

        if hand1_strength > hand2_strength:
            hand1_wins += 1

        elif hand1_strength < hand2_strength:
            hand2_wins += 1

        else:
            hand1_wins += 0.5
            hand2_wins += 0.5

    return hand1_wins, hand2_wins

         


        


