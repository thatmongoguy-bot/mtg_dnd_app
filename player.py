from counter import Counter

class Player:
    def __init__(self, name, starting_life=40):
        self.name = name
        self.life = Counter("Life", starting_life)
        self.poison = Counter("Poison", 0)
        self.creatures = {} # Holds creatures and their +1/+1
        self.commander_damage = {} # Commander Name -> damage dealt by that commander
        

# Add creature with 0 +1/+1 counters
    def add_creature(self, creature_name):
        self.creatures[creature_name] = Counter(f"+1/+1 on {creature_name}", 0)

# Add one +1/+1 counter to a creature
    def buff_creature(self, creature_name):
        if creature_name in self.creatures:
            self.creatures[creature_name].increment()

# Remove one +1/+1 counter to a creature
    def debuff_creature(self, creature_name):
        if creature_name in self.creatures:
            self.creatures[creature_name].decrement()

    def add_commander_damage(self, commander_name, damage):
        if commander_name not in self.commander_damage:
            self.commander_damage[commander_name] = 0
        self.commander_damage[commander_name] += damage
        return self.commander_damage[commander_name]

    def get_commander_damage(self, commander_name):
        return self.commander_damage.get(commander_name, 0)

    def check_commander_loss(self):
        for commander, damage in self.commander_damage.items():
            if damage >= 21:
                return True, commander
        return False, None


if __name__ == "__main__":
    p = Player("Gideon", 40)
    print(f"{p.name} has {p.life.value} life")

    p.add_creature("Llanowar Elves")
    p.buff_creature("Llanowar Elves")
    print(f"{p.name}'s Llanowar Elves has {p.creatures['Llanowar Elves'].value} +1/+1 counters")

# Test commander damage
    p.add_commander_damage("Atraxa", 10)
    p.add_commander_damage("Atraxa", 11)
    print(f"{p.name}'s Atraxa has taken {p.get_commander_damage('Atraxa')} damage")

    loss, commander = p.check_commander_loss()
    if loss:
        print(f"{p.name} has lost with {commander}")
    else:
        print(f"{p.name} is still in the game")