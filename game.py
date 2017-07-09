#!/usr/bin/env python

import random
import conio as io
from actor import Player, Monster
from item import *
from monster import *
from battle import *

player = Player()

# Town screen
def town():
    io.cls()
    io.msg("Welcome to town! This is your main hub of operations.\n"+
    "From here you can view character details and access different areas.\n")
    inTown = True
    while(inTown):
        c = io.menu("What do you want to do?", ["Character Stats", "Inventory", "Shop", "Healing", "Enter Dungeon (Battle)", "Main Menu"])
        if c == 0:
            stats()
        elif c == 1:
            inventory()
        elif c == 2:
            shop()
        elif c == 3:
            healing()
        elif c == 4:
            battle()
        elif c == 5:
            inTown = False
    io.cls()

# Player Stats screen
def stats():
    back = False
    while not back:
        io.cls()
        bonusAttack = 0
        bonusDefense = 0
        for item in player.inventory:
            if item.attack:
                bonusAttack += item.attack
            if item.defense:
                bonusDefense += item.defense

        io.msg("\t ~ " + player.name + " ~\n")
        io.table([  ["Level", player.level],
                    ["Attack", str(player.attack) + " (+" + str(player.getBonusAttack()) + ")"],
                    ["Defense", str(player.defense) + " (+" + str(player.getBonusDefense()) + ")"]
        ])
        io.skipLine()
        io.progressBar(player.exp, player.getExpNextLevel(), 50, "Experience",True)

        if io.binChoice("\nGo back?") == True:
            back = True
    io.cls()

# Player Intentory screen
def inventory():
    back = False
    while not back:
        io.cls()
        io.msg("Inventory")
        io.skipLine()
        itemDisplayList = [["Item", "Value", "Description"]]
        for item in player.inventory:
            itemDisplayList.append([item.name, str(item.value), item.info])
        emptySlots = player.inventorySlots-len(player.inventory)
        for s in range(emptySlots):
            itemDisplayList.append(["[  EMPTY  ]", "---", "---"])
        io.table(itemDisplayList)
        io.msg("\n" + str(player.gold) + " gold\n")
        c = io.menu("Actions", ["Use item", "Back"])
        if c==0:
            useConsumable()
        elif c==1:
            back = True

    io.cls()

def useConsumable():
    back = False
    while not back:
        io.cls()
        items = []
        displayList = []
        for i, item in enumerate(player.inventory):
            if item.consumable:
                items.append(item)
                displayList.append(item.name)
        if len(items) > 0:
            c = io.menu("Use item", displayList, "Cancel")
            if c>=0:
                player.inventory.remove(items[c])
                back = True
        else:
            io.msg("You have no consumables available.")
            c = io.binChoice("Go back?")
            if c:
                back = True


# Shop screen
def shop():
    back = False
    while not back:
        io.cls()
        io.msg("Welcome to the shop!\n"+
        "Buy equipment, consumables and other items here.\n"+
        "You can also sell items, but only for half their value.")
        c = io.menu("What do you want to do?", ["Buy", "Sell", "Leave"])
        io.cls()
        if c == 0:
            done = False
            while not done:
                io.cls()
                cs = io.menu("Buy item\tGold: {}".format(player.gold), items_shop, "Back")
                if cs == -1:
                    done = True
                    break
                io.cls()
                itemName = items_shop[cs]
                itemData = items.get(itemName)
                item = Item()
                item.createFromDict(itemName, itemData)
                verify = io.binChoice("Buy {} for {} gold?".format(itemName, item.value))
                if verify == True:
                    if player.gold >= item.value:
                        if player.addItem(item):
                            player.gold -= item.value
                            continue
                        if io.binChoice("Inventory full. Return?"):
                            done = True
                        continue
                    if io.binChoice("Not enough gold. Return?"):
                        done = True
        elif c == 1:
            done = False
            while not done:
                io.cls()
                cs = io.menu("Sell item", player.getInventoryItemNames(), "Back")
                if cs == -1:
                    done = True
                    break
                io.cls()
                item = player.inventory[cs]
                sellValue = int(item.value/2)
                verify = io.binChoice("Sell {} for {} gold?".format(item.name, sellValue))
                if verify == True:
                    player.gold += sellValue
                    del player.inventory[cs]
        elif c == 2:
            back = True
    io.cls()

# Healing screen
def healing():
    io.cls()
    back = False
    while not back:
        io.msg("You have {}/{} HP".format(player.hp, player.hpMax))
        if io.binChoice("Restore 100 HP? (10 gold)"):
            if player.hp < player.hpMax:
                player.gold -= 10
                player.heal(100)
            else:
                if io.binChoice("You are already at full health. Go back?"):
                    back = True
        else:
            if io.binChoice("Go back?"):
                back = True
        io.cls()

# Battle screen
def battle():
    io.cls()
    back = False
    enemiesAtLevel = []
    for monster in monsters.keys():
        if player.level in monsters.get(monster).get('level'):
            enemiesAtLevel.append(monster)
    enemy = random.choice(enemiesAtLevel)
    monster = Monster(enemy, monsters[enemy])
    monster.setLevel(random.choice(list(monster.levelRange)))
    battle = Battle(player, monster)
    io.msg("Encountered a level {} {}".format(monster.level, monster.name))

    # Main battle loop
    while not back:
        io.skipLine(2)
        io.msg(battle.player.name + "'s HP: " + str(battle.player.hp) + "/" + str(battle.player.hpMax))
        io.msg(battle.monster.name + "'s HP: " + str(battle.monster.hp) + "/" + str(battle.monster.hpMax))
        c = io.menu("Choose an option", ["Attack", "Invetory", "Stats"], "Leave")
        io.cls()
        if c == 0:
            if not battle.isBattleOver():
                io.msg("You attack and hit the " + battle.monster.name + " for " + str(battle.playerAttack()) + " HP")
                io.msg(battle.monster.name + " attacks and hits you for " + str(battle.monsterAttack()) + " HP")
                if(battle.monster.isDead()):
                    io.msg(battle.monster.name + " dies. You are victorious!")
                    io.msg("{} experience gained.".format(battle.awardPlayerExp()))
                    if player.checkLevel():
                        io.msg("{} leveled up! You are now level {}".format(player.name, player.level))
                elif(battle.player.isDead()):
                    io.msg(battle.player.name + "dies. You have been defeated!")
            else:
                io.msg("The battle has ended.")
        elif c == 1:
            inventory()
        elif c == 2:
            stats()
        elif c == -1:
            back = True
    io.cls()

# Below is non-ingame related parts
# Main menu screen and highest parent
def mainMenu():
    io.cls()
    running = True
    while running == True:
        c = io.menu("Main menu", ["New Game", "Load Game", "Save Game", "About", "Exit"])
        if c == 0:
            mm_newGame()
        elif c == 1:
            mm_loadGame()
        elif c == 2:
            mm_saveGame()
        elif c == 3:
            mm_about()
        elif c == 4:
            running = False
            io.msg("Exiting...")

# Main Menu/New Game screen
def mm_newGame():
    io.cls()
    io.msg(" -- Character Creation --")
    done = False
    while not done:
        player.name = io.textIn("Choose a name for your Character: ")
        io.cls()
        io.msg("playeracter name: " + player.name)
        if io.binChoice("\nFinish Character creation and start game?") == True:
            player.base_hp = 100
            player.base_attack = 10
            player.base_defense = 10
            player.setLevel(1)
            player.exp = 0
            player.gold = 300
            player.inventorySlots = 4
            for itemName in items_start:
                item = Item()
                item.createFromDict(itemName, items.get(itemName))
                if player.addItem(item) == False:
                    break
            done = True
        io.cls()
    town()

#Main Menu/Load Game screen
def mm_loadGame():
    io.cls()
    io.msg("Feature not yet implemented. Returning to main menu...")

#Main Menu/Save Game screen
def mm_saveGame():
    io.cls()
    io.msg("Feature not implementet. Returning to main menu...")

#Main Menu/About screen
def mm_about():
    io.cls()
    io.msg("conrpg v0.1 by Arel")

# Run game
io.msg("conrpg v0.1")
mainMenu()
