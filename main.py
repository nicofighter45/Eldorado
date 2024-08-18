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
                     Action('s', "Secret"), Action('p', "Petrolier")]
players: [Player] = []

read = input("To you want to import data ? (yes/no)\n")


if read == "yes":
    with open(input("Name of the file :\n") + '.txt', 'r') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines):
            line = lines[i].split(" ")
            if i < 6:
                if line[0] == actions[i].name:
                    actions[i].value = int(line[1])
                    actions[i].to_buy = int(line[2])
            else:
                player = Player(line[0], int(line[1]), int(line[2]), int(line[4]), int(line[5]), actions)
                gold_number -= int(line[2])
                a = 1
                while a <= int(line[3]):
                    action_line = lines[a + i].split(" ")
                    player.getAction(action_line[0]).possessors[player] = int(action_line[1])
                    a += 1
                players.append(player)
                i += a
            i += 1

else:
    initial_money = int(input("Initial money: "))
    init_players: [str, str] = input(
        "\n\n    Players :\n\n  --  Example  --\nnicolas,a;antoine,u\n  ----------------\n\n").split(';')
    for player in init_players:
        data = player.split(",")
        player = Player(data[0], initial_money, 0, 0, 0, actions)
        player.getAction(data[1]).add(player)
        players.append(player)


def printPlayers():
    global players
    print("\n\n\nPlayers :")
    for player in players:
        print(f"  {player.name}:\n    Money: {getCleanMoney(player.money)}")
        if player.debt > 0:
            print(f"    Debt: {getCleanMoney(10000 * player.debt)}")
        if player.gold > 0:
            print(f"    Gold: {player.gold}")
        if player.base_start > 0:
            print(f"    Base Start: {getCleanMoney(player.base_start)}")
        has_action = False
        totalMoney = player.money + player.gold * 1000 - player.debt * 10000
        for action in actions:
            nb = action.possessors.get(player)
            if not nb is None and nb > 0:
                if not has_action:
                    print("    Action:")
                    has_action = True
                print(f"      {action.name} : {nb} ({getCleanMoney(action.value)})")
                totalMoney += nb * action.value
        print(f"    Capital: {getCleanMoney(totalMoney)}")


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
                  "\n  export <name>                      : export the game on a txt file"
                  "\n  crises <action>                    : economic crises"
                  "\n  success <action> <amount>          : success for an action and for a given amount"
                  "\n  <player> buyd                      : buy diamond with gold"
                  "\n  <player> buy <action> '<value>'    : buy an action and set it's value"
                  "\n  <player> sell <action> '<amount>'  : sell a number of action (default one)"
                  "\n  <player> buyg <amount>             : buy gold"
                  "\n  <player> sellg <amount>            : sell gold"
                  "\n  <player> add <amount>              : add money"
                  "\n  <player> rm <amount>               : remove money"
                  "\n  <player> debt <amount>             : add debt"
                  "\n  <player> debtrm '<amount>'         : remove debt"
                  "\n  <player> rm <amount>               : remove money"
                  "\n  <player> control                   : control"
                  "\n  <player> bank                      : get your money from the bank"
                  "\n  <player> start                     : get your money from the start case"
                  "\n  <player> setstart <amount>         : set bonus start of a player"
                  "\n  calc <calcul>                      : calcul anything"
                  )
        else:
            command = command.split(" ")
            player = getPlayer(command[0])
            if command[0] == "crises":
                print("\nEconomic crises :")
                eco = False
                for action in actions:
                    if action.char == command[1]:
                        for player in action.possessors.keys():
                            if action.possessors.get(player) > 0:
                                eco = True
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
                            if action.possessors.get(player) > 0:
                                print(player.addMoney(int(action.possessors.get(player) * int(command[2]) * 100)))
                if not success:
                    print("No one has this action")
            elif command[0] == "calc":
                print(eval(command[1]))
            elif command[1] == "control":
                print(player.control())
            elif command[0] == "export":
                with open(command[1] + ".txt", "w") as file:
                    for action in actions:
                        file.write(f"{action.name} {action.value} {action.to_buy}\n")
                    for player in players:
                        action_type_nb = 0
                        action_string = ""
                        for action in actions:
                            nb = action.possessors.get(player)
                            if nb is not None and nb > 0:
                                action_string += f"{action.char} {nb}\n"
                                action_type_nb += 1
                        file.write(f"{player.name} {player.money} {player.gold} {action_type_nb} {player.debt} {player.base_start}\n")
                        file.write(action_string + "\n")
            elif command[1] == "buyd":
                if actions[1].to_buy < 3:
                    print("There isn't enough diamond")
                elif player.gold < 10:
                    print("You don't have enough gold")
                else:
                    player.gold -= 10
                    gold_number += 10
                    actions[1].add(player)
                    actions[1].add(player)
                    actions[1].add(player)
                    print(f"{player.name} now has {player.gold} gold ingot and {actions[1].possessors.get(player)} "
                          f"diamonds")
            elif command[1] == "bank":
                print(player.bank())
            elif command[1] == "start":
                print(player.start())
            elif command[1] == "setstart":
                print(player.setstart(int(command[2])))
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
            elif command[1] == "debtrm" and len(command) == 2:
                print(player.removeDebt(player.debt*1000))
            elif command[1] == "debtrm":
                print(player.removeDebt(int(command[2])))
            elif command[1] == "debt":
                print(player.addDebt(int(command[2])))
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
