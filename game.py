#!/usr/bin/env python

import random
import json
import time
import conio as io
from actor import Player, Monster
from item import *
from battle import *
from savesys import *

class STATUS:
    SUCCESS = True
    EXIT = False

    @staticmethod
    def ESCAPE(): return False

    @staticmethod
    def CONTINUE(): return True

class Game():
    def __init__(self):
        self.ITEMS_START = ['Stick', 'Wooden Shield']
        self.ITEMS_SHOP = ['Steel Sword', 'Health Potion', 'Knight Shield']

        self.items = self.import_from_json("data/items.json")
        self.monsters = self.import_from_json("data/monsters.json")
        self.player = None

        self.settings = Settings("config/settings.cfg")
        io.USE_UNDERLINE = self.settings.read_boolean('underline')

        self.gfx = io.Graphics("data/graphics.txt", self.settings.read('graphics'))
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
        while(in_town):
            self.gfx.draw('town')
            options = {
                "*Character stats" : self.stats,
                "*Inventory"       : self.inventory,
                "*Shop"            : self.shop,
                "*Healing"         : self.healing,
                "*Enter Dungeon (Battle)": self.battle,
                "*Main menu"       : STATUS.ESCAPE,
            }
            c = io.map_menu("What do you want to do?", options.keys(), abort="*Main menu")
            in_town = options.get(c, STATUS.CONTINUE)()

        io.cls()

    # Player Stats screen
    def stats(self):
        io.cls()

        io.msg("\t ~ " + self.player.name + " ~\n")
        io.table(
            ["Level", self.player.level],
            ["HP", f"{self.player.hp}/{self.player.hp_max}"],
            ["Attack", f"{self.player.attack} (+{self.player.get_bonus_attack()})"],
            ["Defence", f"{self.player.defence} (+{self.player.get_bonus_defence()})"]
        )
        io.skip_line()
        io.progress_bar(self.player.exp, self.player.get_exp_next_level(), 50, "Experience",True)

        io.acknowledge()
        io.cls()
        return STATUS.SUCCESS

    # Player Intentory screen
    def inventory(self):
        inventoring = True
        while inventoring:
            io.cls()
            io.msg("Inventory")
            io.skip_line()
            item_display_list = [["Item", "Value", "Description"]]
            for item in self.player.inventory.values():
                item_display_list.append([item.name, item.value, item.info])
            empty_slots = self.player.inventory_slots-len(self.player.inventory)
            for s in range(empty_slots):
                item_display_list.append(["[  EMPTY  ]", "---", "---"])

            # Print items in a table
            io.table(*item_display_list)

            # Print gold
            io.skip_line(2)
            io.msg(f"{self.player.gold} gold")
            io.skip_line(2)

            # Options
            options = {
                "*Use item" : self.use_consumable,
                "*Back"     : STATUS.ESCAPE,
            }
            c = io.map_menu("Actions", options.keys(), abort="*Back")
            inventoring = options.get(c, STATUS.CONTINUE)()

        io.cls()
        return STATUS.SUCCESS

    def use_consumable(self):
        consuming = True
        while consuming:
            io.cls()

            from item import Consumable
            consumables = [c for c in self.player.inventory.values() if isinstance(c, Consumable)]
            consumable_names = [i.name for i in consumables]
            if len(consumables) > 0:
                choice = io.menu("Use item", consumable_names, "Cancel")

                #FIX subclass restorable items
                if choice in consumable_names:
                    consumable = self.player.inventory[choice]
                    self.player.heal(consumable.restore)
                    io.msg(f"""
                        You have healed yourself for {consumable.restore} hp.
                        You now have {self.player.hp}/{self.player.hp_max} hp.
                    """)
                    del self.player.inventory[choice]
                    io.acknowledge()
                else:
                    consuming = False
            else:
                io.msg("You have no consumables available.")
                consuming = not io.bin_choice("Go back?")
        return STATUS.SUCCESS


    # Shop screen
    def shop(self):
        io.msg("Entering the marketplace...")
        time.sleep(1)
        def buy():
            buying = True
            while buying:
                io.cls()
                choice = io.menu(f"Buy item\tGold: {self.player.gold}", self.ITEMS_SHOP, abort="Back")
                if choice == "Back":
                    buying = False
                    break
                io.cls()
                item = Item_constructor(name=choice)
                accept_transaction = io.bin_choice(f"Buy {item.name} for {item.value} gold?")
                if accept_transaction:
                    if self.player.gold >= item.value:
                        if self.player.add_item(item):
                            self.player.gold -= item.value
                            continue

                        buying = io.bin_choice("Inventory full. Return?")
                    else:
                        buying = io.bin_choice("Not enough gold. Return?")
            return STATUS.SUCCESS

        def sell():
            selling = True
            while selling:
                io.cls()
                cs = io.menu("Sell item", self.player.inventory.keys(), abort="Back")
                if cs == "Back":
                    selling = False
                    break

                io.cls()
                item = self.player.inventory[cs]
                sell_value = int(item.value/2)
                accept_transaction = io.bin_choice(f"Sell {item.name} for {sell_value} gold?")
                if accept_transaction:
                    self.player.gold += sell_value
                    del self.player.inventory[cs]
            return STATUS.SUCCESS

        shopping = True
        while shopping:
            io.cls()
            io.msg("""
                Welcome to the shop!
                Buy equipment, consumables and other items here.
                You can also sell items, but only for half their value.
            """)
            self.gfx.draw('shop')
            options = {
                "*Buy"   : buy,
                "*Sell"  : sell,
                "*Leave" : STATUS.ESCAPE
            }
            c = io.map_menu("What do you want to do?", options.keys(), abort="*Leave")
            shopping = options.get(c, STATUS.CONTINUE)()
            io.cls()

        io.msg("Leaving the marketplace...")
        time.sleep(1)
        io.cls()
        return STATUS.SUCCESS

    # Healing screen
    def healing(self):
        io.msg("Visiting the healing temple...")
        time.sleep(1)
        io.cls()
        healing = True
        while healing:
            self.gfx.draw('healer')
            io.msg("You have {}/{} HP".format(self.player.hp, self.player.hp_max))
            if io.bin_choice("Restore 100 HP? (10 gold)"):
                if self.player.hp < self.player.hp_max:
                    self.player.gold -= 10
                    self.player.heal(100)
                else:
                    if io.bin_choice("You are already at full health. Go back?"):
                        healing = False
            else:
                healing = not io.bin_choice("Go back?")
        io.msg("Leaving the temple...")
        time.sleep(1)
        io.cls()
        return STATUS.SUCCESS

    # Battle screen
    def battle(self):
        io.msg("Delving into the dungeon...")
        time.sleep(1)
        io.cls()

        enemies_at_level = []
        for monster in self.monsters.keys():
            level_range = range(self.monsters.get(monster).get('level_min'), self.monsters.get(monster).get('level_max'))
            if self.player.level in level_range:
                enemies_at_level.append(monster)

        enemy = random.choice(enemies_at_level)
        monster = Monster(enemy, **self.monsters[enemy])
        monster.set_attributes(level = 2) #TEMP random.randint(monster.level_min, monster.level_max))
        battle = Battle(self.player, monster)
        io.msg(f"Encountered a level {monster.level} {monster.name}")

        def attack():
            io.cls()
            time.sleep(.2)
            io.msg(f"You attack and hit the {battle.monster.name} for {battle.player_attack()} HP")
            time.sleep(.5)
            io.msg(f"{battle.monster.name} attacks and hits you for {battle.monster_attack()} HP")
            time.sleep(1.5)
            if(battle.monster.is_dead()):
                io.msg(f"{battle.monster.name} dies. You are victorious!")
                io.msg(f"{battle.award_player_exp()} experience gained.")
                if self.player.check_levelup():
                    self.player.levelup()
                    io.msg(f"{self.player.name} leveled up! You are now level {self.player.level}")

                io.acknowledge()
                return STATUS.EXIT
            return STATUS.SUCCESS

        # Main battle loop
        fighting = True
        while fighting:
            io.skip_line(2)
            io.msg(f"{battle.player.name}'s HP: {battle.player.hp}/{battle.player.hp_max}")
            io.msg(f"{battle.monster.name}'s HP: {battle.monster.hp}/{battle.monster.hp_max}")

            options = {
                "*Attack"    : attack,
                "*Inventory" : self.inventory,
                "*Stats"     : self.stats,
                "*Run"       : STATUS.ESCAPE,
            }
            c = io.map_menu("Choose an option", options.keys(), "*Run")
            fighting = options.get(c, STATUS.CONTINUE)()
            io.cls()

        def loot():
            io.cls()
            io.acknowledge("To be implemented")
            return STATUS.SUCCESS

        looting = battle.monster.is_dead()
        while looting:
            options = {
                "*Loot"      : loot,
                "*Inventory" : self.inventory,
                "*Stats"     : self.stats,
                "*Return to town"     : STATUS.ESCAPE,
            }
            c = io.map_menu("Choose an option", options.keys(), "*Return to town")
            looting = options.get(c, STATUS.CONTINUE)()
            io.cls()

        io.msg("Returning to town...")
        time.sleep(1)
        io.cls()
        return STATUS.SUCCESS

    # Below is non-ingame related parts
    # Main menu screen and highest parent
    def main_menu(self):
        io.cls()
        io.msg("conrpg v1.1 by arhusebo & evva")
        io.skip_line()
        running = True
        while running:
            self.gfx.draw('title')
            options = {
                "*New Game"  : self.mm_new_game,
                "*Load Game" : self.mm_load_game,
                "*Save Game" : self.mm_save_game,
                "*About"     : self.mm_about,
                "*Exit"      : STATUS.ESCAPE,
            }
            c = io.map_menu("Main menu", options.keys(), abort="*Exit")
            running = options.get(c, STATUS.SUCCESS)()
        io.cls()
        io.msg("Thanks for playing!")

    # Main Menu/New Game screen
    def mm_new_game(self):
        io.cls()
        io.msg(" -- Character Creation --")
        creating_char = True
        self.player = Player()
        while creating_char:
            char_name = io.text_in("Choose a name for your Character: ")
            io.cls()
            io.msg("Character name: " + char_name)
            if io.bin_choice("\nFinish Character creation and start game?") == True:
                self.player.name = char_name
                self.player.base_hp = 100
                self.player.base_attack = 10
                self.player.base_defence = 10
                self.player.set_attributes(level = 1)
                self.player.exp = 0
                self.player.gold = 300
                self.player.inventory_slots = 4
                for item_name in self.ITEMS_START:
                    item = Item(item_name, **self.items[item_name])
                    self.player.add_item(item)
                creating_char = False
            io.cls()
        self.town()
        return STATUS.SUCCESS

    #Main Menu/Load Game screen
    def mm_load_game(self):
        io.cls()
        self.player = Player()
        if load_game('config/save.json', self.player, self.items):
            self.town()
        else:
            io.msg("No saved game available.")
        return STATUS.SUCCESS

    #Main Menu/Save Game screen
    def mm_save_game(self):
        io.cls()
        if self.player:
            save_game('config/save.json', self.player)
            io.msg("Game saved!")
        else:
            io.msg("There is no data to be saved.")
        return STATUS.SUCCESS

    #Main Menu/About screen
    def mm_about(self):
        io.cls()
        io.acknowledge("conrpg v0.1 by Arel")
        io.cls()
        return STATUS.SUCCESS

game = Game()
game.main_menu()
