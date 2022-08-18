def getCleanMoney(money: int) -> str:
    money = str(money)[::-1]
    return (" ".join([money[i:i+3] for i in range(0, len(money), 3)]))[::-1] + "$"


class Player:

    def __init__(self, name: str, money: int, gold: int, action_nb: int, actions):
        self.name = name
        self.money = money
        self.gold = gold
        self.actionNumber = action_nb
        self.actions = actions

    def buy(self, type: str, value: int) -> str:
        action = self.getAction(type)
        value = 100 * int(value/100)
        if action.to_buy == 0:
            return f"Error : there isn't action of type {action.char} left"
        elif value < action.value:
            return f"Error : The value of this action is {action.value}"
        elif self.money < value:
            return "Error : you don't have enough money"
        self.money -= value
        action.add(self)
        self.actionNumber += 1
        action.value = value
        return f"{self.name} bought {action.name} for {getCleanMoney(value)}. He now has {getCleanMoney(self.money)}"

    def sell(self, type: str, value: int) -> str:
        action = self.getAction(type)
        if action.possessors[self] < value:
            return f"Error : You don't have enough action of type {action.char} left"
        self.money += value * action.value
        action.remove(self, value)
        self.actionNumber -= value
        if action.to_buy == 10:
            action.value = 1000
        return f"{self.name} sold {action.name} ({value}). He now has {getCleanMoney(self.money)}"

    def addMoney(self, value: int) -> str:
        if value <= 0:
            return "You can't add a negative amount of money"
        self.money += 100 * int(value)
        return f"{self.name} has now {getCleanMoney(self.money)}"

    def removeMoney(self, value: int) -> str:
        if self.money - value == 0:
            return "You don't have enough money"
        self.money -= 100 * int(value)
        return f"{self.name} has now {getCleanMoney(self.money)}"

    def control(self) -> str:
        total = int(self.money - 100 * int(0.3 * (self.money + 1000 * (self.actionNumber + self.gold))))
        if total < 0:
            self.money = 0
            return f"{self.name} still need to pay {getCleanMoney(-total)}"
        else:
            self.money = total
            return f"{self.name} has now {getCleanMoney(self.money)}"

    def crises(self) -> str:
        total = int(self.money - 100 * int(0.9 * (self.money + 1000 * (self.actionNumber + self.gold))/100))
        if total < 0:
            self.money = 0
            return f"{self.name} still need to pay {getCleanMoney(-total)}"
        else:
            self.money = total
            return f"{self.name} has now {getCleanMoney(self.money)}"

    def getAction(self, char: str):
        if char == 'a':
            return self.actions[0]
        elif char == 'd':
            return self.actions[1]
        elif char == 'u':
            return self.actions[2]
        elif char == 'm':
            return self.actions[3]
        elif char == 's':
            return self.actions[4]
        elif char == 'p':
            return self.actions[5]
        else:
            return None

    def bank(self) -> str:
        self.money += int((0.1 * (self.money + 1000 * (self.actionNumber + self.gold)))/100)*100
        return f"{self.name} now has {getCleanMoney(self.money)}"

    def start(self) -> str:
        self.money += 200 * self.gold + 100 * self.actionNumber
        return f"{self.name} now has {getCleanMoney(self.money)}"