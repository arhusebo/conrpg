#!/usr/bin/env python

import random
import json
import time
import conio as io
from actor import Player, Monster
from item import *
from battle import *
from savesys import *

class Game():
    def __init__(self):
        self.ITEMS_START = ['Stick', 'Wooden Shield']
        self.ITEMS_SHOP = ['Steel Sword', 'Health Potion', 'Knight Shield']

        self.items = self.import_from_json("data/items.json")
        self.monsters = self.import_from_json("data/monsters.json")
        self.player = None

        self.gfx = io.Graphics("data/graphics.txt")
        self.gfx.load()

    def import_from_json(self, path):
        with open(path, 'r') as f:
            return json.loads(f.read())

    # Town screen
    def town(self):
        io.cls()
        io.msg("""
            Welcome to town! This is your main hub of operations.
            From here you can view character details and access different areas.
        """)
        in_town = True
        def exit_town():
            nonlocal in_town
            in_town = False
        while(in_town):
            #self.gfx.draw('town')
            options = {
                "Character stats" : self.stats,
                "Inventory"       : self.inventory,
                "Shop"            : self.shop,
                "Healing"         : self.healing,
                "Enter Dungeon (Battle)": self.battle,
                "Main menu"       : exit_town,
            }
            c = io.menu("What do you want to do?", options.keys())
            options.get(c, lambda: None)()

        io.cls()

    # Player Stats screen
    def stats(self):
        back = False
        while not back:
            io.cls()

            io.msg("\t ~ " + self.player.name + " ~\n")
            io.table([
                ["Level", self.player.level],
                ["HP", f"{self.player.hp}/{self.player.hp_max}"],
                ["Attack", f"{self.player.attack} (+{self.player.get_bonus_attack()})"],
                ["Defense", f"{self.player.defense} (+{self.player.get_bonus_defense()})"]
            ])
            io.skip_line()
            io.progress_bar(self.player.exp, self.player.get_exp_next_level(), 50, "Experience",True)

            if io.bin_choice("\nGo back?") == True:
                back = True
        io.cls()

    # Player Intentory screen
    def inventory(self):
        back = False
        while not back:
            io.cls()
            io.msg("Inventory")
            io.skip_line()
            item_display_list = [["Item", "Value", "Description"]]
            for item in self.player.inventory.values():
                item_display_list.append([item.name, item.value, item.info])
            empty_slots = self.player.inventory_slots-len(self.player.inventory)
            for s in range(empty_slots):
                item_display_list.append(["[  EMPTY  ]", "---", "---"])
            io.table(item_display_list)
            io.msg("\n" + str(self.player.gold) + " gold\n")
            options = {
            }
            c = io.menu("Actions", ["Use item", "Back"])
            if c=="Use item":
                self.use_consumable()
            elif c=="Back":
                back = True

        io.cls()

    def use_consumable(self):
        back = False
        while not back:
            io.cls()
            items = []
            display_list = []
            for i, item in enumerate(self.player.inventory.values()):
                if item.consumable:
                    items.append(item)
                    display_list.append(item.name)
            if len(items) > 0:
                c = io.menu("Use item", display_list, "Cancel")
                if c in display_list:
                    restore_values = items[c].restore_values
                    if 'hp' in restore_values:
                        self.player.heal(restore_values['hp'])
                    del self.player.inventory[item.name]
                    back = True
            else:
                io.msg("You have no consumables available.")
                c = io.bin_choice("Go back?")
                if c:
                    back = True


    # Shop screen
    def shop(self):
        back = False
        while not back:
            io.msg("Entering the marketplace...")
            time.sleep(2)
            io.cls()
            io.msg("""
                Welcome to the shop!
                Buy equipment, consumables and other items here.
                You can also sell items, but only for half their value.
            """)
            self.gfx.draw('shop')
            c = io.menu("What do you want to do?", ["Buy", "Sell", "Leave"])
            io.cls()
            if c == "Buy":
                done = False
                while not done:
                    io.cls()
                    cs = io.menu("Buy item\tGold: {}".format(self.player.gold), self.ITEMS_SHOP, "Back")
                    if cs == "Back":
                        done = True
                        break
                    io.cls()
                    item_name = cs
                    item_data = self.items.get(item_name)
                    item = Item(item_name, **item_data)
                    verify = io.bin_choice("Buy {} for {} gold?".format(item_name, item.value))
                    if verify == True:
                        if self.player.gold >= item.value:
                            if self.player.add_item(item):
                                self.player.gold -= item.value
                                continue
                            if io.bin_choice("Inventory full. Return?"):
                                done = True
                            continue
                        if io.bin_choice("Not enough gold. Return?"):
                            done = True
            elif c == "Sell":
                done = False
                while not done:
                    io.cls()
                    cs = io.menu("Sell item", self.player.get_inventory_item_names(), "Back")
                    if cs == "Back":
                        done = True
                        break
                    io.cls()
                    item = self.player.inventory[cs]
                    sell_value = int(item.value/2)
                    verify = io.bin_choice("Sell {} for {} gold?".format(item.name, sell_value))
                    if verify == True:
                        self.player.gold += sell_value
                        del self.player.inventory[cs]
            elif c == "Leave":
                back = True
        io.msg("Leaving the marketplace...")
        time.sleep(2)
        io.cls()

    # Healing screen
    def healing(self):
        io.msg("Visiting the healing temple...")
        time.sleep(2)
        io.cls()
        back = False
        while not back:
            self.gfx.draw('healer')
            io.msg("You have {}/{} HP".format(self.player.hp, self.player.hp_max))
            if io.bin_choice("Restore 100 HP? (10 gold)"):
                if self.player.hp < self.player.hp_max:
                    self.player.gold -= 10
                    self.player.heal(100)
                else:
                    if io.bin_choice("You are already at full health. Go back?"):
                        back = True
            else:
                if io.bin_choice("Go back?"):
                    back = True
            io.msg("Leaving the temple...")
            time.sleep(2)
            io.cls()

    # Battle screen
    def battle(self):
        io.msg("Delving into the dungeon...")
        time.sleep(2)
        io.cls()
        back = False
        enemies_at_level = []
        for monster in self.monsters.keys():
            level_range = range(self.monsters.get(monster).get('level_min'), self.monsters.get(monster).get('level_max'))
            if self.player.level in level_range:
                enemies_at_level.append(monster)
        enemy = random.choice(enemies_at_level)
        monster = Monster(enemy, **self.monsters[enemy])
        monster.set_attributes(level = random.choice(list(range(monster.level_min, monster.level_max))))
        battle = Battle(self.player, monster)
        io.msg("Encountered a level {} {}".format(monster.level, monster.name))

        # Main battle loop
        while not back:
            io.skip_line(2)
            io.msg(battle.player.name + "'s HP: " + str(battle.player.hp) + "/" + str(battle.player.hp_max))
            io.msg(battle.monster.name + "'s HP: " + str(battle.monster.hp) + "/" + str(battle.monster.hp_max))
            c = io.menu("Choose an option", ["Attack", "Inventory", "Stats"], "Leave")
            io.cls()
            if c == "Attack":
                if not battle.is_battle_over():
                    time.sleep(.5)
                    io.msg("You attack and hit the " + battle.monster.name + " for " + str(battle.player_attack()) + " HP")
                    time.sleep(1)
                    io.msg(battle.monster.name + " attacks and hits you for " + str(battle.monster_attack()) + " HP")
                    time.sleep(1)
                    if(battle.monster.is_dead()):
                        io.msg(battle.monster.name + " dies. You are victorious!")
                        io.msg("{} experience gained.".format(battle.award_player_exp()))
                        if self.player.check_levelup():
                            self.player.levelup()
                            io.msg("{} leveled up! You are now level {}".format(self.player.name, self.player.level))
                    elif(battle.player.is_dead()):
                        io.msg(battle.player.name + "dies. You have been defeated!")
                else:
                    io.msg("The battle has ended.")
            elif c == "Inventory":
                self.inventory()
            elif c == "Stats":
                self.stats()
            elif c == "Leave":
                back = True
        io.msg("Returning to town...")
        time.sleep(2)
        io.cls()

    # Below is non-ingame related parts
    # Main menu screen and highest parent
    def main_menu(self):
        io.cls()
        io.msg("conrpg v1.1 by arhusebo & evva")
        io.skip_line()
        running = True
        def exit_game():
            nonlocal running
            running = False
            io.msg("Exiting...")
        while running:
            options = {
                "*New Game"  : self.mm_new_game,
                "*Load Game" : self.mm_load_game,
                "*Save Game" : self.mm_save_game,
                "*About"     : self.mm_about,
                "*Exit"      : exit_game,
            }
            c = io.map_menu("Main menu", options.keys())
            options.get(c, lambda: None)()

    # Main Menu/New Game screen
    def mm_new_game(self):
        io.cls()
        io.msg(" -- Character Creation --")
        done = False
        self.player = Player()
        while not done:
            char_name = io.text_in("Choose a name for your Character: ")
            io.cls()
            io.msg("Character name: " + char_name)
            if io.bin_choice("\nFinish Character creation and start game?") == True:
                self.player.name = char_name
                self.player.base_hp = 100
                self.player.base_attack = 10
                self.player.base_defense = 10
                self.player.set_attributes(level = 1)
                self.player.exp = 0
                self.player.gold = 300
                self.player.inventory_slots = 4
                for item_name in self.ITEMS_START:
                    item = Item(item_name, **self.items[item_name])
                    self.player.add_item(item)
                done = True
            io.cls()
        self.town()

    #Main Menu/Load Game screen
    def mm_load_game(self):
        io.cls()
        self.player = Player()
        if load_game('config/save.json', self.player, self.items):
            self.town()
        else:
            io.msg("No saved game available.")

    #Main Menu/Save Game screen
    def mm_save_game(self):
        io.cls()
        if self.player:
            save_game('config/save.json', self.player)
            io.msg("Game saved!")
        else:
            io.msg("There is no data to be saved.")

    #Main Menu/About screen
    def mm_about(self):
        io.cls()
        io.msg("conrpg v0.1 by Arel")

game = Game()
game.main_menu()
