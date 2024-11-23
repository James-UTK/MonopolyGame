# Simulates rolling two dice, returning two random values between 1 and 6.

import random

def roll_dice():
    return random.randint(1, 6), random.randint(1, 6)

if __name__ == "__main__":
    dice1, dice2 = roll_dice()
    print(f"Rolled: {dice1} and {dice2}")
