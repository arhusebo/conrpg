#!/usr/bin/env python

import random
import json
import conio as io
from actor import Player, Monster
from item import *
from battle import *
from savesys import *

class Game():
    def __init__(self):
        self.ITEMS_START = ['Stick', 'Wooden Shield']
        self.ITEMS_SHOP = ['Steel Sword', 'Health Potion', 'Knight Shield']

        self.items = self.importFromJson("data/items.json")
        self.monsters = self.importFromJson("data/monsters.json")
        self.player = None

    def importFromJson(self, path):
        with open(path, 'r') as f:
            return json.loads(f.read())

    # Town screen
    def town(self):
        io.cls()
        io.msg("Welcome to town! This is your main hub of operations.\n"+
        "From here you can view character details and access different areas.\n")
        inTown = True
        while(inTown):
            c = io.menu("What do you want to do?", ["Character Stats", "Inventory", "Shop", "Healing", "Enter Dungeon (Battle)", "Main Menu"])
            if c == 0:
                self.stats()
            elif c == 1:
                self.inventory()
            elif c == 2:
                self.shop()
            elif c == 3:
                self.healing()
            elif c == 4:
                self.battle()
            elif c == 5:
                inTown = False
        io.cls()

    # Player Stats screen
    def stats(self):
        back = False
        while not back:
            io.cls()
            bonusAttack = 0
            bonusDefense = 0
            for item in self.player.inventory:
                if item.attack:
                    bonusAttack += item.attack
                if item.defense:
                    bonusDefense += item.defense

            io.msg("\t ~ " + self.player.name + " ~\n")
            io.table([  ["Level", self.player.level],
                        ["Attack", str(self.player.attack) + " (+" + str(self.player.getBonusAttack()) + ")"],
                        ["Defense", str(self.player.defense) + " (+" + str(self.player.getBonusDefense()) + ")"]
            ])
            io.skipLine()
            io.progressBar(self.player.exp, self.player.getExpNextLevel(), 50, "Experience",True)

            if io.binChoice("\nGo back?") == True:
                back = True
        io.cls()

    # Player Intentory screen
    def inventory(self):
        back = False
        while not back:
            io.cls()
            io.msg("Inventory")
            io.skipLine()
            itemDisplayList = [["Item", "Value", "Description"]]
            for item in self.player.inventory:
                itemDisplayList.append([item.name, str(item.value), item.info])
            emptySlots = self.player.inventorySlots-len(self.player.inventory)
            for s in range(emptySlots):
                itemDisplayList.append(["[  EMPTY  ]", "---", "---"])
            io.table(itemDisplayList)
            io.msg("\n" + str(self.player.gold) + " gold\n")
            c = io.menu("Actions", ["Use item", "Back"])
            if c==0:
                self.useConsumable()
            elif c==1:
                back = True

        io.cls()

    def useConsumable(self):
        back = False
        while not back:
            io.cls()
            items = []
            displayList = []
            for i, item in enumerate(self.player.inventory):
                if item.consumable:
                    items.append(item)
                    displayList.append(item.name)
            if len(items) > 0:
                c = io.menu("Use item", displayList, "Cancel")
                if c>=0:
                    restoreValues = items[c].restoreValues
                    if 'hp' in restoreValues:
                        self.player.heal(restoreValues['hp'])
                    self.player.inventory.remove(items[c])
                    back = True
            else:
                io.msg("You have no consumables available.")
                c = io.binChoice("Go back?")
                if c:
                    back = True


    # Shop screen
    def shop(self):
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
                    cs = io.menu("Buy item\tGold: {}".format(self.player.gold), self.ITEMS_SHOP, "Back")
                    if cs == -1:
                        done = True
                        break
                    io.cls()
                    itemName = self.ITEMS_SHOP[cs]
                    itemData = self.items.get(itemName)
                    item = Item(itemName, **itemData)
                    verify = io.binChoice("Buy {} for {} gold?".format(itemName, item.value))
                    if verify == True:
                        if self.player.gold >= item.value:
                            if self.player.addItem(item):
                                self.player.gold -= item.value
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
                    cs = io.menu("Sell item", self.player.getInventoryItemNames(), "Back")
                    if cs == -1:
                        done = True
                        break
                    io.cls()
                    item = self.player.inventory[cs]
                    sellValue = int(item.value/2)
                    verify = io.binChoice("Sell {} for {} gold?".format(item.name, sellValue))
                    if verify == True:
                        self.player.gold += sellValue
                        del self.player.inventory[cs]
            elif c == 2:
                back = True
        io.cls()

    # Healing screen
    def healing(self):
        io.cls()
        back = False
        while not back:
            io.msg("You have {}/{} HP".format(self.player.hp, self.player.hpMax))
            if io.binChoice("Restore 100 HP? (10 gold)"):
                if self.player.hp < self.player.hpMax:
                    self.player.gold -= 10
                    self.player.heal(100)
                else:
                    if io.binChoice("You are already at full health. Go back?"):
                        back = True
            else:
                if io.binChoice("Go back?"):
                    back = True
            io.cls()

    # Battle screen
    def battle(self):
        io.cls()
        back = False
        enemiesAtLevel = []
        for monster in self.monsters.keys():
            levelRange = range(self.monsters.get(monster).get('levelMin'), self.monsters.get(monster).get('levelMax'))
            if self.player.level in levelRange:
                enemiesAtLevel.append(monster)
        enemy = random.choice(enemiesAtLevel)
        monster = Monster(enemy, **self.monsters[enemy])
        monster.setLevel(random.choice(list(range(monster.levelMin, monster.levelMax))))
        battle = Battle(self.player, monster)
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
                        if self.player.checkLevel():
                            io.msg("{} leveled up! You are now level {}".format(self.player.name, self.player.level))
                    elif(battle.player.isDead()):
                        io.msg(battle.player.name + "dies. You have been defeated!")
                else:
                    io.msg("The battle has ended.")
            elif c == 1:
                self.inventory()
            elif c == 2:
                self.stats()
            elif c == -1:
                back = True
        io.cls()

    # Below is non-ingame related parts
    # Main menu screen and highest parent
    def mainMenu(self):
        io.cls()
        running = True
        while running == True:
            c = io.menu("Main menu", ["New Game", "Load Game", "Save Game", "About", "Exit"])
            if c == 0:
                self.mm_newGame()
            elif c == 1:
                self.mm_loadGame()
            elif c == 2:
                self.mm_saveGame()
            elif c == 3:
                self.mm_about()
            elif c == 4:
                running = False
                io.msg("Exiting...")

    # Main Menu/New Game screen
    def mm_newGame(self):
        io.cls()
        io.msg(" -- Character Creation --")
        done = False
        self.player = Player()
        while not done:
            charName = io.textIn("Choose a name for your Character: ")
            io.cls()
            io.msg("Character name: " + charName)
            if io.binChoice("\nFinish Character creation and start game?") == True:
                self.player.name = charName
                self.player.base_hp = 100
                self.player.base_attack = 10
                self.player.base_defense = 10
                self.player.setLevel(1)
                self.player.exp = 0
                self.player.gold = 300
                self.player.inventorySlots = 4
                for itemName in self.ITEMS_START:
                    item = Item(itemName, **self.items[itemName])
                    self.player.addItem(item)
                done = True
            io.cls()
        self.town()

    #Main Menu/Load Game screen
    def mm_loadGame(self):
        io.cls()
        self.player = Player()
        loadGame('config/save.json', self.player, self.items)
        self.town()

    #Main Menu/Save Game screen
    def mm_saveGame(self):
        io.cls()
        if self.player:
            saveGame('config/save.json', self.player)
            io.msg("Game saved!")
        else:
            io.msg("There is no data to be saved.")

    #Main Menu/About screen
    def mm_about(self):
        io.cls()
        io.msg("conrpg v0.1 by Arel")

io.msg("conrpg v0.1")
game = Game()
game.mainMenu()
