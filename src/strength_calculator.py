def base14(values):
    if len(values) > 6:
        raise ValueError("too many values")

    pad_values = values + [0] * (6 - len(values))

    base14_output = 0
    for i in range(6):
        base14_output += pad_values[i] * 14**(5 - i)  

    return base14_output

def get_kickers(rank_counter, exclude_ranks, n):
    kickers = []
    for r in range(12, -1, -1):
        if r in exclude_ranks:
            continue
        if rank_counter[r] > 0:
            kickers.append(r)
        if len(kickers) == n:
            break
    return kickers

def hand_strength_calculator(hand, community_cards):

    strength = 0

    test_board = hand + community_cards

    suit_counter = [0,0,0,0]
    for card in test_board:
        suit_counter[card[1]] += 1

    rank_counter = [0 for i in range(13)]
    for card in test_board:
        rank_counter[card[0]] += 1

    flush_exists = False
    found_straight_flush = False
    # straight flush
    for suit_index, suit_count in enumerate(suit_counter):
        if suit_count >= 5:
            flush_exists = True
            flush = [card for card in test_board if card[1] == suit_index]

            flush_rank_counter = [0 for i in range(13)]
            for card in flush:
                flush_rank_counter[card[0]] += 1

            for high in range(12,3,-1):
                if flush_rank_counter[high-4:high+1] == [1,1,1,1,1]:
                    strength = base14([9, high])
                    found_straight_flush = True
                    
                    break

            if found_straight_flush == False and flush_rank_counter[12] == flush_rank_counter[0] == flush_rank_counter[1] == flush_rank_counter[2] == flush_rank_counter[3] == 1:
                strength = base14([9, 3])
                found_straight_flush = True

        if flush_exists == True:
            break

    # record all pairing data

    quads = None
    trips_list = []
    pairs_list = []

    for i in range(12,-1,-1):
        r = rank_counter[i]

        if r == 4:
            quads = i

        if r == 3:
            trips_list.append(i)

        if r == 2:
            pairs_list.append(i)


    highest_trips = trips_list[0] if len(trips_list)>0 else None
    highest_pair = pairs_list[0] if len(pairs_list)>0 else None
    second_highest_pair = pairs_list[1] if len(pairs_list) > 1 else None

    # full house
    fullhouse_pair_component = None
    if highest_trips is not None:
        other_candidates = [t for t in trips_list if t != highest_trips] + pairs_list
        if len(other_candidates)>0:
            fullhouse_pair_component = max(other_candidates)

    # straight 
    straight_found = False
    straight_high = None
    if not found_straight_flush:
        for high in range(12,3,-1):
            for j in range(4,-1,-1):
                if rank_counter[high - j] == 0:
                    break
            else:
                straight_found = True
                straight_high = high
                break

    # wheel 
    wheel_found = False
    if not found_straight_flush and straight_found == False and rank_counter[0] > 0 and rank_counter[1] > 0 and rank_counter[2] > 0 and rank_counter[3] > 0 and rank_counter[12] > 0:
        wheel_found = True

    if not found_straight_flush:
        if quads is not None:
            kickers = get_kickers(rank_counter, {quads}, 1)
            strength = base14([8, quads] + kickers)

        elif fullhouse_pair_component is not None:
            strength = base14([7, highest_trips, fullhouse_pair_component]) 

        elif flush_exists == True:
            flush_ranks = sorted([card[0] for card in flush], reverse=True)[:5]  # was [:4]
            strength = base14([6] + flush_ranks)

        elif straight_found == True:
            strength = base14([5, straight_high])  

        elif wheel_found == True:
            strength = base14([5, 3])  

        elif highest_trips is not None:
            kickers = get_kickers(rank_counter, {highest_trips}, 2)
            strength = base14([4, highest_trips] + kickers)

        elif highest_pair is not None and second_highest_pair is not None:
            kickers = get_kickers(rank_counter, {highest_pair, second_highest_pair}, 1)
            strength = base14([3, highest_pair, second_highest_pair] + kickers)

        elif highest_pair is not None:
            kickers = get_kickers(rank_counter, {highest_pair}, 3)
            strength = base14([2, highest_pair] + kickers)

        else:
            kickers = get_kickers(rank_counter, set(), 5)
            strength = base14([1] + kickers)

    return strength