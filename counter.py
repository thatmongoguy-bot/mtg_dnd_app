class Counter:
    def __init__(self, name, starting_value=0):
        self.name = name
        self._value = starting_value

    @property
    def value(self):
        return self._value

    def increment(self, amount=1):
        self._value += amount
        return self._value

    def decrement(self, amount=1):
        self._value -= amount
        return self._value

    def reset(self):
        self._value = 0


if __name__ == "__main__":
    life = Counter("Life", 40)
    print(f"Starting life: {life.value}")

    life.decrement()
    print(f"After 1 damage: {life.value}")

    life.increment()
    print(f"After 1 healing: {life.value}")