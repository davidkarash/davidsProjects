"""Classes and functions necessary to run simulation.
To use project, run dealer.py as a module or import and call the hand_simulation() function.
"""

inttorank: dict[int, str] = {2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'T', 11: 'J', 12: 'Q', 13: 'K', 14: 'A'}
ranktoint: dict[str, int] = {"2":2, "3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"T":10,"J":11,"Q":12,"K":13,"A":14}
suits: list[str] = ["h", "d", "s", "c"]
handrankings: dict[str, int] = {"sf" : 0, "4k" : 1, "fh": 2, "fl": 3, "st": 4, "3k": 5, "2p": 6, "1p": 7, "hc": 8}

class Card:
    rank: int = 0
    suit: str = ""

    def __init__(self, info: str):
        self.rank = ranktoint[info[0]]
        self.suit = info[1]


class Hand:
    cards: list[Card]

    def __init__(self, cards: list[Card]):
        for i in range(len(cards)-1):
            for j in range(0, len(cards)-i-1):
                if cards[j].rank > cards[j+1].rank:
                    cards[j], cards[j+1] = cards[j+1], cards[j]

        self.cards = cards

    def __str__(self) -> str:
        out: str = ""
        for c in self.cards:
            out += (str(c.rank) + c.suit)
        return out




def classify(hand: Hand) -> str:
    # TODO: check sf
    cards = hand.cards
    in_row: list[list[Card]] = []
    csuit: str = ""
    sf: str = ""
    st: str = ""
    adjust_for_dups: int = 0
    for i in range(3):
        in_row.append([])
        if cards[i].rank == cards[i+1].rank:
            continue
        adjust_for_dups = 0
        for j in range(5):
            if (i+j+1+adjust_for_dups) > 6:
                break
            if cards[i+j+adjust_for_dups].rank == cards[i+j+1+adjust_for_dups].rank:
                adjust_for_dups += 1
            if (i+j+1+adjust_for_dups) > 6:
                break
            if j == 0:
                if (cards[i+j+adjust_for_dups].rank)+1 == cards[i+j+1+adjust_for_dups].rank:
                    in_row[i].append(cards[i+j+adjust_for_dups])
                    in_row[i].append(cards[i+j+1+adjust_for_dups]);
                else:
                    break
            elif (cards[i+j+adjust_for_dups].rank)+1 == cards[i+j+1+adjust_for_dups].rank:
                in_row[i].append(cards[i+j+1+adjust_for_dups])
            else:
                break
    for set in in_row:
        if len(set) == 5:
            st = "st" + str(inttorank[set[4].rank])
            if set[0].suit == set[1].suit == set[2].suit == set[3].suit == set[4].suit:
                sf = "sf" + inttorank[set[4].rank]
    if sf != "":
        return sf
    ranks: dict[int, int] = {}
    suits: dict[str, list[Card]] = {"c": [], "h": [], "d": [], "s": []}

    # Find multiples of cards and suits
    for card in cards:
        # Multiples of cards
        if (card.rank not in ranks.keys()):
            ranks[card.rank] = 1
        else:
            ranks[card.rank] += 1
        # Multiples of suits
        suits[card.suit].append(card)
        
    trips: list[int] = []
    pairs: list[int] = []

    # Hand is four of a kind
    # Build list of three of a kind and pairs
    for x in ranks:
        if ranks[x] == 4:
            if cards[6].rank == ranks[x]:
                return "4k" + inttorank[x] + inttorank[cards[2].rank]
            else:
                return "4k" + inttorank[x] + inttorank[cards[6].rank]
        elif ranks[x] == 3:
            trips.append(x)
        elif ranks[x] == 2:
            pairs.append(x)
    
    # Hand is full house
    if len(trips) > 1:
        return "fh" + inttorank[trips[1]] + inttorank[trips[0]]
    elif len(trips) == 1 and len(pairs) > 0:
        return "fh" + inttorank[trips[0]] + inttorank[pairs[len(pairs)-1]]

    # Hand is flush
    for suit in suits:
        fl: str = "fl"
        count: int = len(suits[suit])
        if count >= 5:
            if count == 5:
                for card in suits[suit]:
                    fl += inttorank[card.rank]
                return fl
            elif count == 6:
                while count > 1:
                    fl += inttorank[suits[suit][count-1].rank]
                    count -= 1
                return fl
            else:
                while count > 2:
                    fl += inttorank[suits[suit][count-1].rank]
                    count -= 1
                return fl

    # Hand is straight
    if st != "":
        return st
    
    # Hand is three of a kind
    elif len(trips) > 0:
        trip: str = "3k" + inttorank[trips[0]]
        i = 6
        while len(trip) < 5:
            if trips[0] != cards[i].rank:
                trip += inttorank[cards[i].rank]
                i -= 1
            else:
                i -= 3
        return trip
    
    # Hand is two pair
    elif len(pairs) == 2:
        twop: str = "2p"
        i = 6
        for x in pairs:
            twop += inttorank[x]
            if x == cards[i].rank:
                i -= 2
        return twop + inttorank[cards[i].rank]
    
    # Hand is one pair
    elif len(pairs) == 1:
        onep: str = "1p" + inttorank[pairs[0]]
        i = 6
        while len(onep) < 6:
            if pairs[0] != cards[i].rank:
                onep += inttorank[cards[i].rank]
                i -= 1
            else:
                i -= 2
        return onep
    
    # Hand is high card
    hc: str = "hc"
    i = 6
    while len(hc) < 5:
        hc += inttorank[cards[i].rank]
        i -= 1
    return hc


def handMaker(cards: str) -> Hand:
    list_c: list[Card] = []
    for i in range(0, 14, 2):
        temp: str = ""
        for j in range(2):
            temp += cards[i+j]
        list_c.append(Card(temp))
    return Hand(list_c)


def checksf(hand: Hand) -> str:
    suits: dict[str, list[Card]] = {"c": [], "h": [], "d": [], "s": []}

    # Check for flush
    found_fl: bool = False
    for card in hand.cards:
        suits[card.suit].append(card)
    for suit in suits:
        if len(suits[suit]) > 4:
            found_fl = True
            break
    if found_fl:
        ...
    else:
        return ""

    cards = hand.cards
    in_row: list[list[Card]] = []
    csuit: str = ""
    sf: str = ""
    st: str = ""
    adjust_for_dups: int = 0
    for i in range(3):
        in_row.append([])
        if cards[i].rank == cards[i+1].rank:
            continue
        adjust_for_dups = 0
        for j in range(5):
            if (i+j+1+adjust_for_dups) > 6:
                break
            if cards[i+j+adjust_for_dups].rank == cards[i+j+1+adjust_for_dups].rank:
                adjust_for_dups += 1
            if (i+j+1+adjust_for_dups) > 6:
                break
            if j == 0:
                if ((cards[i+j+adjust_for_dups].rank)+1 == cards[i+j+1+adjust_for_dups].rank) and cards[i+j+adjust_for_dups].suit == cards[i+j+adjust_for_dups+1].suit:
                    in_row[i].append(cards[i+j+adjust_for_dups])
                    in_row[i].append(cards[i+j+1+adjust_for_dups]);
                else:
                    break
            elif (cards[i+j+adjust_for_dups].rank)+1 == cards[i+j+1+adjust_for_dups].rank and cards[i+j+adjust_for_dups].suit == cards[i+j+adjust_for_dups+1].suit:
                in_row[i].append(cards[i+j+1+adjust_for_dups])
            else:
                break
    for set in in_row:
        if len(set) == 5:
            if set[0].suit == set[1].suit == set[2].suit == set[3].suit == set[4].suit:
                sf = "sf" + inttorank[set[4].rank]
    return sf



def compare(hand1: str, hand2: str) -> int:
    # return values 0, 1, 2, indicate hand 1 wins, hand 2 wins, and tie, respectively
    # TODO: Implement efficient method to replace time wasted on calculating second hand classification
    # if classified[0:1] == "sf":
    #     hand2cls: str = checksf(hand)
    #     if hand2cls == "":
    #         return 0
    #     else:
    #         for i in range(2, 7):
    #             if int(classified[i]) > int(hand2cls[i]):
    #                 return 0
    #             elif int(classified[i]) < int(hand2cls[i]):
    #                 return 1
    #         return 2
    # elif classified[0:1] == "4k":
    class_hand1: str = classify(handMaker(hand1))
    class_hand2: str = classify(handMaker(hand2))
    hand1_val: int = handrankings[class_hand1[0:2]]
    hand2_val: int = handrankings[class_hand2[0:2]]
    if hand1_val < hand2_val:
        return 0
    elif hand1_val > hand2_val:
        return 1
    else:
        for i in range(len(class_hand1)-2):
            diff: int = ranktoint[class_hand1[i+2]] - ranktoint[class_hand2[i+2]]
            if diff > 0:
                return 0
            elif diff < 0:
                return 1
    return 2