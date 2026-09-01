import random

class Dice:
# Roll 20 side for start / some cards
    @staticmethod
    def d20():
        return random.randint(1, 20)

# Roll 6 side/tokens
    @staticmethod
    def d6():
        return random.randint(1, 6)

# Generic Roll - For Expansion
    @staticmethod
    def roll(sides, quantity=1):
        results = []
        for _ in range(quantity):

            results.append(random.randint(1, sides))
        return results if quantity > 1 else results[0]

if __name__ == "__main__":
    print(f"d20 roll (turn order): {Dice.d20()}")
    print(f"d6 roll: {Dice.d6()}")
