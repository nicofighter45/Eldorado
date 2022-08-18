class Action:

    def __init__(self, char: str, name: str):
        self.char = char
        self.value = 1000
        self.to_buy = 10
        self.possessors = {}
        self.name = name

    def add(self, player):
        if self.possessors.get(player) is None:
            self.possessors[player] = 1
        else:
            self.possessors[player] = self.possessors.get(player) + 1
        self.to_buy -= 1

    def remove(self, player, value: int):
        self.possessors[player] = self.possessors.get(player) - value
        self.to_buy += value
