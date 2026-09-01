from .game import Game
from .dice import Dice
from .rulebook import Rulebook

class MTGMenu:
    def __init__(self):
        self.game = None
        self.rules = Rulebook("data/mtg_rules2026.txt")

    def start(self):
        print("\n=== Welcome to MTG Assistant ===")

# Choose Format
        print("\n1. Standard (20 Life)")
        print("2. Commander (40 Life)")
        choice = input("Choose a Format: ")
        if choice == "1":
            self.game = Game("Standard")
        else:
            self.game = Game("Commander")

# Add Players
        num_players = int(input("Number of Players (2-8): "))
        for i in range(num_players):
            name = input(f"Player {i + 1} name: ")
            self.game.add_player(name)
        self.main_menu()

    def main_menu(self):
        while True:
            print("\n" + "=" * 40)
            self.game.get_status()
            print("\n--- Menu ---")
            print("1. Deal damage to player")
            print("2. Heal a player")
            print("3. Add poison counter")
            print("4. Roll Dice")
            print("5. Search rulebook")
            print("6. Next Turn")
            print("7. Deal Commander Damage")
            print("8. Undo")
            print("9. Redo")
            print("10. Exit")

            choice = input("\nChoice: ")

            if choice == "1":
                self.deal_damage()
            elif choice == "2":
                self.heal()
            elif choice == "3":
                self.add_poison()
            elif choice == "4":
                self.roll_dice()
            elif choice == "5":
                self.search_rules()
            elif choice == "6":
                self.game.next_turn()
                print(f"\n--- It is now {self.game.current_player.name}'s turn ---")

            elif choice == "7":
                self.commander_damage()
            elif choice == "8":
                self.game.undo()
            elif choice == "9":
                self.game.redo()
            elif choice == "10":
                print("Thanks for playing!")
                break

    def deal_damage(self):
        self.game.save_state()  # Save state before dealing damage
        self.show_players()
        idx = int(input("Player number: ")) - 1
        damage = int(input("Amount of damage: "))
        for _ in range(damage):
            self.game.players[idx].life.decrement()
            print(f"{self.game.players[idx].name} took {damage} damage.")

    def heal(self):
        self.game.save_state()  # Save state before healing
        self.show_players()
        idx = int(input("Player number: ")) - 1
        amount = int(input("Amount to heal: "))
        for _ in range(amount):
            self.game.players[idx].life.increment()
            print(f"{self.game.players[idx].name} was healed by {amount}.")

    def add_poison(self):
        self.game.save_state()  # Save state before adding poison
        self.show_players()
        idx = int(input("Player number: ")) - 1
        self.game.players[idx].poison.increment()
        print(f"{self.game.players[idx].name} now has {self.game.players[idx].poison.value} poison counters.")

    def roll_dice(self):
        print("\n1. d20")
        print("2. d6")
        print("3. Custom")

        choice = input(" Choose: ")
        if choice == "1":
            print(f"Rolled: {Dice.d20()}")
        elif choice == "2":
            print(f"Rolled: {Dice.d6()}")
        elif choice == "3":
            sides = int(input("Number of sides: "))
            print(f"Rolled: {Dice.roll(sides)}")

    def search_rules(self):
        keyword = input("Search Keyword: ")
        self.rules.show_results(keyword)

    def commander_damage(self):
        if not self.game.track_commander_damage:
            print("Commander damage only in commander format.")
            return
        self.game.save_state()  # Save state before dealing commander damage
        self.show_players()
        idx = int(input ("Player to hit: ")) - 1
        commander = input("commander Name: ")
        damage = int(input("Damage:"))
        self.game.deal_commander_damage(idx, commander, damage)

    def show_players(self):
        print("\nPlayers:")
        for i, p in enumerate(self.game.players):
            print(f"{i + 1}. {p.name} ({p.life.value} life)")

if __name__ == "__main__":
    menu = MTGMenu()
    menu.start()