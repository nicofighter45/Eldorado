from Action import Action
from Player import Player, getCleanMoney

gold_number = 21


def buyGold(player: Player, value: int) -> str:
    global gold_number
    if value <= 0:
        return "You can't add a negative amount of gold"
    elif value > gold_number:
        return f"There is just {gold_number} gold left"
    elif value * 1000 > player.money:
        return "You don't have enough money"
    player.removeMoney(value * 1000)
    player.gold += value
    gold_number -= value
    return f"{player.name} now has {player.gold} gold ingot and {getCleanMoney(player.money)}"


def sellGold(player: Player, value: int) -> str:
    global gold_number
    if value > player.gold:
        return "You don't have enough gold"
    elif value <= 0:
        return "You can't sell a negative amount of gold"
    player.addMoney(value * 1000)
    player.gold -= value
    gold_number += value
    return f"{player.name} now has {player.gold} gold ingot and {getCleanMoney(player.money)}"


actions: [Action] = [Action('a', "Avion"), Action('d', "Diamant"), Action('u', "Uranium"), Action('m', "Missile"),
                     Action('s', "Secret"), Action('p', "Pétrolier")]
players: [Player] = []

read = input("To you want to import data ? (yes/no)\n")


if read == "yes":
    with open('game.txt', 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].split(" ")
            print(line)
            if i < 6:
                if line[0] == actions[i].char:
                    actions[i].value = int(line[1])
                    actions[i].to_buy = int(line[2])
            else:
                player = Player(line[0], int(line[1]), int(line[2]), int(line[3]), actions)
                gold_number -= int(line[2])
                a = 1
                while a <= int(line[4]):
                    action_line = lines[a + i].split(" ")
                    player.getAction(action_line[0]).possessors[player] = int(action_line[1])
                    a += 1
                players.append(player)
                i += a - 1
            i += 1

else:
    initial_money = int(input("Initial money: "))
    init_players: [str, str] = input(
        "\n\n    Players :\n\n  --  Example  --\nnicolas,a;antoine,u\n  ----------------\n\n").split(';')
    for player in init_players:
        data = player.split(",")
        player = Player(data[0], initial_money, 0, 1, actions)
        player.getAction(data[1]).add(player)
        players.append(player)


def printPlayers():
    global players
    print("\n\n\nPlayers :")
    for player in players:
        print(
            f"  {player.name}:"
            f"\n    Money: {getCleanMoney(player.money)}"
            f"\n    Gold: {player.gold}"
            f"\n    Action:"
        )
        totalMoney = player.money + player.gold * 1000
        for action in actions:
            nb = action.possessors.get(player)
            if not nb is None and nb > 0:
                print(f"      {action.name} : {nb} ({getCleanMoney(action.value)})")
                totalMoney += nb * action.value
        print(f"    Total: {getCleanMoney(totalMoney)}")


def printActions():
    global actions
    print(f"\nActions :\n  Gold : {gold_number} left")
    for action in actions:
        print(f"  {action.name} : {getCleanMoney(action.value)} ({action.to_buy} left)")


def getPlayer(name: str) -> Player:
    global players
    for player in players:
        if player.name == name:
            return player


printPlayers()
while True:
    command = input("\n")
    try:
        if command == "action":
            printActions()
        elif command == "player":
            printPlayers()
        elif command == "help" or command == "?":
            print("\n Help :"
                  "\n  action                             : get all actions informations"
                  "\n  player                             : get all players informations"
                  "\n  help|?                             : this page"
                  "\n  crises <action>                    : economic crises"
                  "\n  success <action> <amount>          : success for an action and for a given amount"
                  "\n  <player> buyd                      : buy diamond with gold"
                  "\n  <player> buy <action> '<value>'    : buy an action and set it's value "
                  "\n  <player> sell <action> '<amount>'  : sell a number of action (default one)"
                  "\n  <player> buyg <amount>             : buy gold"
                  "\n  <player> sellg <amount>            : sell gold"
                  "\n  <player> add <amount>              : add money"
                  "\n  <player> rm <amount>               : remove money"
                  "\n  <player> control                   : control"
                  "\n  <player> bank                      : get your money from the bank"
                  "\n  <player> start                     : get your money from the start case"
                  "\b  calc <calcul>                      : calcul anything"
                  )
        else:
            command = command.split(" ")
            player = getPlayer(command[0])
            if command[0] == "crises":
                print("\nEconomic crises :")
                eco = False
                for action in actions:
                    if action.char == command[1]:
                        eco = True
                        for player in action.possessors.keys():
                            print(player.crises())
                if not eco:
                    print("No one was touch by the crises")
            elif command[0] == "success":
                print("\nSuccess :")
                success = False
                for action in actions:
                    if action.char == command[1]:
                        success = True
                        for player in action.possessors.keys():
                            print(player.addMoney(int(action.possessors.get(player) * int(command[2]) * 100)))
                if not success:
                    print("No one has this action")
            elif command[0] == "calc":
                print(eval(command[1]))
            elif command[1] == "control":
                print(player.control())
            elif command[1] == "buyd":
                if actions[1].to_buy < 3:
                    print("There isn't enough diamond")
                elif player.gold < 10:
                    print("You don't have enough gold")
                else:
                    player.gold -= 10
                    actions[1].add(player)
                    actions[1].add(player)
                    actions[1].add(player)
                    print(f"{player.name} now has {player.gold} gold ingot and {actions[1].possessors.get(player)} "
                          f"diamonds")
            elif command[1] == "bank":
                print(player.bank())
            elif command[1] == "start":
                print(player.start())
            elif command[1] == "buyg":
                print(buyGold(player, int(command[2])))
            elif command[1] == "sellg":
                print(sellGold(player, int(command[2])))
            elif command[1] == "add":
                if int(command[2]) <= 0:
                    print("You can't add a negative amount of money")
                else:
                    print(player.addMoney(int(command[2])))
            elif command[1] == "rm":
                if player.money < int(command[2]):
                    print("Error : You don't have enough money")
                else:
                    print(player.removeMoney(int(command[2])))
            elif command[1] == "buy" and len(command) == 3:
                print(player.buy(command[2], player.getAction(command[2]).value))
            elif command[1] == "sell" and len(command) == 3:
                print(player.sell(command[2], 1))
            elif command[1] == "buy":
                print(player.buy(command[2], int(command[3])))
            elif command[1] == "sell":
                print(player.sell(command[2], int(command[3])))
            else:
                print("Error, command misspell")
    except:
        print("Error, command misspell")
