"""I created this file to simulate the famous Monty Hall problem after seeing a tweet that
mathematicians had done the problem wrong for years. Surprise surprise, math was right."""

import random

total: int = 0

swap: bool = input("Would you like to swap? (y/n) ") == "y"

try:
    trials: int = int(input("How many trials would you like to run? "))
except:
    TypeError
    print("Error: Trials must be an integer.")
    exit()

for i in range(1):
    a: int = random.randint(1,3)
    door1 = False
    door2 = False
    door3 = False

    if a == 1:
        door1 = True
    elif a == 2:
        door2 = True
    elif a == 3:
        door3 = True
    else:
        print("uhhhh?")

    if not swap:
        if door1:
            total += 1
    else:
        if door1:
            b = random.randint(2, 3)
            if b == 2:
                if door3:
                    total += 1
            if b == 3:
                if door2:
                    total += 1
        
        if door2:
            total += 1
        
        if door3:
            total += 1

print(total)