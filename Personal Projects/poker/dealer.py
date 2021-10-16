from random import randint
from pokerreader import compare
import time

hands_out = tuple[str, str]
suits: dict[int, str] = {0:'c',1:'h',2:'s',3:'d'}
inv_suit: dict[str, int] = {'c':0,'h':1,'s':2,'d':3}
random_to_rank: dict[int, str] = {0:'2',1:'3',2:'4',3:'5',4:'6',5:'7',6:'8',7:'9',8:'T',9:'J',10:'Q',11:'K',12:'A'}
rank_to_random: dict[str, int] = {'2':0,'3':1,'4':2,'5':3,'6':4,'7':5,'8':6,'9':7,'T':8,'J':9,'Q':10,'K':11,'A':12}


def convert_val_to_card(val: int) -> str:
    rank: str = random_to_rank[val % 13]
    suit: str = suits[val // 13]
    return rank+suit


def hand_simulation() -> None:
    sims: int = int(input("How many simulations would you like to run? "))
    held_cards_1: str = input("Input player 1 hand: ")
    held_cards_2: str = input("input player 2 hand: ")
    start = time.time()
    full_hand_1: str = held_cards_1
    full_hand_2: str = held_cards_2
    h1_count: int = 0
    h2_count: int = 0
    ties: int = 0
    time_comparing: float = 0
    #deck: list[str] = ['2c','3c','4c','5c','6c','7c','8c','9c','Tc','Jc','Qc','Kc','Ac','2h','3h','4h','5h','6h','7h','8h','9h','Th','Jh','Qh','Kh','Ah','2s','3s','4s','5s','6s','7s','8s','9s','Ts','Js','Qs','Ks','As','2d','3d','4d','5d','6d','7d','8d','9d','Td','Jd','Qd','Kd','Ad']
    used_vals: list[int] = []
    used_vals.append(rank_to_random[held_cards_1[0]] + inv_suit[held_cards_1[1]]*13)
    used_vals.append(rank_to_random[held_cards_1[2]] + inv_suit[held_cards_1[3]]*13)

    used_vals.append(rank_to_random[held_cards_2[0]] + inv_suit[held_cards_2[1]]*13)
    used_vals.append(rank_to_random[held_cards_2[2]] + inv_suit[held_cards_2[3]]*13)
    for _ in range(sims):
        new_used_vals: list[int] = []
        full_hand_1 = held_cards_1
        full_hand_2 = held_cards_2
        comm = ""
        for i in range(5):
            attempt: int = randint(0,51)
            while attempt in used_vals or attempt in new_used_vals:
                attempt = randint(0, 51)
            comm += convert_val_to_card(attempt)
            new_used_vals.append(attempt)

        full_hand_1 += comm
        full_hand_2 += comm
        # start_compare = time.time()
        outcome = compare(full_hand_1, full_hand_2)
        # end_compare = time.time()
        # time_comparing += end_compare - start_compare
        if outcome == 0:
            h1_count += 1
        elif outcome == 1:
            h2_count += 1
        else:
            ties += 1
            

    p1_win_pct: float = h1_count/sims
    p2_win_pct: float = h2_count/sims
    tie_pct: float = ties/sims
    end = time.time()
    print(f"Hand 1 equity: {p1_win_pct}\nHand 2 equity: {p2_win_pct}\nTie chance: {tie_pct}")
    print(f"Time elapsed: {end-start}")
    # print("Time comparing: " + str(time_comparing))
    # print(str(time_comparing/(end-start)) + "%")


if __name__ == "__main__":
    hand_simulation()