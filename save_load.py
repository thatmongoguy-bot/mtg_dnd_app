import json

# Save the game to a JSON file
class SaveLoad:
    @staticmethod
    def save(game, filename = "mtg_save.json"):
        data = {"format_type": game.format_type, 
                "starting_life": game.starting_life,
                "track_commander_damage": game.track_commander_damage,
                "current_turn_index": game.current_turn_index,
                "players": []
            }
        for player in game.players:
            player_data = {"name": player.name,
                           "life": player.life.value,
                           "poison": player.poison.value,
                           "creatures": {},
                           "commander_damage": player.commander_damage}

# Save creature +1/+1 counters
            for creature_name, counter in player.creatures.items():
                player_data["creatures"][creature_name] = counter.value
            data["players"].append(player_data)
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)

        print(f"Game saved to {filename}")

# Load the game from a JSON file
    @staticmethod
    def load(filename = "mtg_save.json"):

        from game import Game
        from player import Player

        with open(filename, 'r') as f:
            data = json.load(f)

# Recreate the game
        game = Game(data["format_type"])
        game.current_turn_index = data["current_turn_index"]

# Recreate players
        for player_data in data["players"]:
            player = Player(player_data["name"], data["starting_life"])
            player.life._value = player_data["life"]
            player.poison._value = player_data["poison"]
            player.commander_damage = player_data["commander_damage"]

# Recreate creatures
            for creature_name, counter_value in player_data["creatures"].items():
                
                player.add_creature(creature_name)

                for _ in range(counter_value):
                    player.buff_creature(creature_name)
                    game.players.append(player)

        print(f"Game loaded from {filename}")
        return game

# Test the save / load system
if __name__ == "__main__":

    print("Testing save/load system...")
    print("Creating a test game...")

    from game import Game
    test_game = Game("Commander")
    test_game.add_player("Alice")
    test_game.add_player("Bob")

    test_game.players[0].life.decrement()

    test_game.players[0].life.decrement()
    test_game.players[1].add_commander_damage("Atraxa", 10)
    test_game.players[0].add_creature("Grizzly Bears")
    test_game.players[0].buff_creature("Grizzly Bears")

    test_game.players[0].buff_creature("Grizzly Bears")
    test_game.get_status()

    print("\n--- Saving ---")
    SaveLoad.save(test_game, "test_save.json")

    print("\n--- Loading ---")
    loaded_game = SaveLoad.load("test_save.json")
    loaded_game.get_status()
