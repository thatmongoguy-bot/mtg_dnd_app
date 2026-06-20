from player import Player
import player

class Game:
    def __init__(self, format_type = "Standard"):
        self.format_type = format_type
        self.players = []
        self.current_turn_index = 0

# Set rules based on format
        if format_type == "Commander":
            self.starting_life = 40
            self.track_commander_damage = True

        else:  # Standard
            self.starting_life = 20
            self.track_commander_damage = False

# Add player to the game.
    def add_player(self, name):
        player = Player(name, self.starting_life)
        self.players.append(player)
        return player

# Deal commander combat damage to player.
    def deal_commander_damage(self, player_index, commander_name, damage):
        if not self.track_commander_damage:
            print("Commander damage only tracked in Commander format.")
            return

        player = self.players[player_index]
        total = player.add_commander_damage(commander_name, damage)
        print(f"{player.name} took {damage} from {commander_name}. Total: {total}")

        loss, commander = player.check_commander_loss()
        if loss:
            print(f"{player.name} loses to commander damage from {commander}!")

# Advance to the next player's turn
    def next_turn(self):
        self.current_turn_index = (self.current_turn_index + 1) % len(self.players)
        return self.current_player

# Get the player whose turn it is
    @property
    def current_player(self):
        if self.players:
            return self.players[self.current_turn_index]
        return None

# Print current game status
    def get_status(self):
        print(f"\n=== {self.format_type} Game ===")
        for i, player in enumerate(self.players):
            turn_marker = " Current Turn" if i == self.current_turn_index else ""
            print(f"{player.name}: {player.life.value} life | Poison: {player.poison.value}{turn_marker}")
            if self.track_commander_damage and player.commander_damage:
                for cmd, dmg in player.commander_damage.items():
                    print(f"  {cmd}: {dmg} damage")

if __name__ == "__main__":

# Test Standard Game
    print("Testing Standard Format:")
    standard_game = Game("Standard")
    standard_game.add_player("Alice")
    standard_game.add_player("Bob")
    standard_game.get_status()

    print("\n---")

# Test Commander Game
    print("Testing Commander Format:")
    commander_game = Game("Commander")
    commander_game.add_player("David")
    commander_game.add_player("Matthew")
    commander_game.get_status()

    print("\n--- David attacks Matthew with Atraxa for 5 ---")
    commander_game.deal_commander_damage(1, "Atraxa", 5)
    commander_game.get_status()

    print("\n--- Matthew attacks David with Krenko for 16 ---")
    commander_game.deal_commander_damage(0, "Krenko", 16)
    commander_game.get_status()

    print("\nNext turn!")
    commander_game.next_turn()
    commander_game.get_status()
