import pickle
import time
from itertools import combinations

from equity_calculator import equity_calculator


ranks = list(range(13))
suits = list(range(4))
deck = [(rank, suit) for rank in ranks for suit in suits]

all_hands = list(combinations(deck, 2))


def suit_pattern(cards):
    seen = {}
    pattern = []

    for rank, suit in cards:
        if suit not in seen:
            seen[suit] = len(seen)

        pattern.append((rank, seen[suit]))

    return tuple(pattern)


def canonical_ordered(first, second):
    return min(
        suit_pattern(list(first_order) + list(second_order))
        for first_order in (first, first[::-1])
        for second_order in (second, second[::-1])
    )


def canonical_matchup(hero, villain):
    hero_first = canonical_ordered(hero, villain)
    villain_first = canonical_ordered(villain, hero)

    if hero_first <= villain_first:
        return hero_first, False

    return villain_first, True


if __name__ == "__main__":
    trials = 10000

    results = {}
    count = 0
    start_time = time.time()

    for i, hero in enumerate(all_hands):
        for villain in all_hands[i + 1:]:
            if set(hero) & set(villain):
                continue

            key, swapped = canonical_matchup(hero, villain)

            if key in results:
                continue

            hero_first_pattern = canonical_ordered(hero, villain)
            villain_first_pattern = canonical_ordered(villain, hero)

            if hero_first_pattern == villain_first_pattern:
                equity = (trials / 2, trials / 2)
            else:
                equity = equity_calculator(
                    list(hero),
                    list(villain),
                    trials
                )

                if swapped:
                    equity = equity[::-1]

            results[key] = equity
            count += 1

            if count % 100 == 0:
                elapsed = time.time() - start_time

                print(
                    f"{count} unique matchups computed... "
                    f"({elapsed:.1f}s elapsed, "
                    f"{elapsed / count:.2f}s/matchup)"
                )

            if count % 1000 == 0:
                with open("equity_table.pkl", "wb") as file:
                    pickle.dump(results, file)

                print(
                    f"  -> saved checkpoint at "
                    f"{count} matchups"
                )

    elapsed = time.time() - start_time

    print(
        f"Done. {len(results)} unique matchups computed "
        f"in {elapsed:.1f}s"
    )

    with open("equity_table.pkl", "wb") as file:
        pickle.dump(results, file)

    print("Final results saved to equity_table.pkl")