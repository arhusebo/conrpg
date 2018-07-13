#!/usr/bin/env python

import random
import json
import time
import conio as io
import adventure2
from status import STATUS
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
                "*Enter Dungeon"   : self.adventure,
                "*Main menu"       : STATUS.ESCAPE,
            }
            c = io.map_menu("What do you want to do?", options.keys(), abort="*Main menu")
            in_town = options.get(c, STATUS.CONTINUE)()

        io.cls()

    # Player Stats screen
    def stats(self):
        io.cls()

        io.progress_bar(self.player.exp, self.player.get_exp_next_level(), 50, f"{self.player.name}, level {self.player.level} Adventurer",True)
        io.skip_line(3)
        io.progress_bar(self.player.hp, self.player.attributes['health'], 25, "Health", True)
        io.skip_line(1)
        io.progress_bar(100, 100, 25, "Energy", True)
        io.skip_line(1)
        io.progress_bar(100, 100, 25, "Hunger")
        io.skip_line(2)
        io.table(
            ["Attack", f"{self.player.attributes['attack']}",f"(+{self.player.get_bonus_attack()})"],
            ["Defence", f"{self.player.attributes['defence']}",f"(+{self.player.get_bonus_defence()})"],
            ["Accuracy", f"{self.player.base_attributes['accuracy']}",f"(+{self.player.get_bonus_accuracy()})"],
            ["Evasion", f"{self.player.base_attributes['evasion']}",f"(+{self.player.get_bonus_evasion()})"],
            ["Speed", f"{self.player.base_attributes['speed']}",f"(+{self.player.get_bonus_speed()})"],
        )

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
            for item in self.player.inventory:
                item_display_list.append([item.name, item.value, item.info])
            empty_slots = self.player.inventory.free_space()
            for s in range(empty_slots):
                item_display_list.append(["[  EMPTY  ]", "---", "---"])

            # Print items in a table
            io.table(*item_display_list)

            # Print gold
            io.skip_line(2)
            io.msg(f"{self.player.inventory.gold} gold")
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
            consumables = [c for c in self.player.inventory if isinstance(c, Consumable)]
            consumable_names = [i.name for i in consumables]
            if len(consumables) > 0:
                choice = io.menu("Use item", consumable_names, "Cancel")

                #FIX subclass restorable items
                if choice in consumable_names:
                    consumable = self.player.inventory.remove(choice)
                    self.player.heal(consumable.restore)
                    io.msg(f"""
                        You have healed yourself for {consumable.restore} hp.
                        You now have {self.player.hp}/{self.player.attributes['health']} hp.
                    """)
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
                choice = io.menu(f"Buy item\tGold: {self.player.inventory.gold}", self.ITEMS_SHOP, abort="Back")
                if choice == "Back":
                    buying = False
                    break
                io.cls()
                item = Item_constructor(name=choice)
                accept_transaction = io.bin_choice(f"Buy {item.name} for {item.value} gold?")
                if accept_transaction:
                    if self.player.inventory.gold >= item.value:
                        if self.player.inventory.add(item):
                            self.player.inventory.gold -= item.value
                            continue

                        buying = io.bin_choice("Inventory full. Return?")
                    else:
                        buying = io.bin_choice("Not enough gold. Return?")
            return STATUS.SUCCESS

        def sell():
            selling = True
            while selling:
                io.cls()
                cs = io.menu("Sell item", self.player.inventory.item_names(), abort="Back")
                if cs == "Back":
                    selling = False
                    break

                io.cls()
                item = self.player.inventory.item_by_name(cs)
                sell_value = int(item.value/2)
                accept_transaction = io.bin_choice(f"Sell {item.name} for {sell_value} gold?")
                if accept_transaction:
                    self.player.inventory.gold += sell_value
                    self.player.inventory.remove(cs)
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
        
        healing = True
        while healing:
            io.cls()
            self.gfx.draw('healer')
            io.msg("You have {}/{} HP".format(self.player.hp, self.player.attributes['health']))
            if io.bin_choice("Restore 100 HP? (10 gold)"):
                if self.player.hp < self.player.attributes['health']:
                    if self.player.inventory.gold >= 10:
                        self.player.inventory.gold -= 10
                        self.player.heal(100)
                    io.acknowledge("You don't have enough gold!")
                else:
                    if io.bin_choice("You are already at full health. Go back?"):
                        healing = False
            else:
                healing = not io.bin_choice("Go back?")
        io.msg("Leaving the temple...")
        time.sleep(1)
        io.cls()
        return STATUS.SUCCESS
    
    # Dungeon
    adventure = adventure2.adventure
    
    # Battle screen
    def battle(self):
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
            # perform a turn and unpack turn results
            player_start, player_attack, monster_attack = battle.turn()
            player_attack_outcomes, player_attack_damage = player_attack
            monster_attack_outcomes, monster_attack_damage = monster_attack
            
            def show_player_outcomes():
                if 'hit' in player_attack_outcomes:
                    io.msg(f"You attack and hit the {battle.monster.name} for {player_attack_damage} HP")
                elif 'miss' in player_attack_outcomes:
                    io.msg("You miss")
                elif 'dodge' in player_attack_outcomes:
                    io.msg(f"{battle.monster.name} dodges your attack")
            
            def show_monster_outcomes():
                if 'hit' in monster_attack_outcomes:
                    io.msg(f"{battle.monster.name} attacks and hits you for {monster_attack_damage} HP")
                elif 'miss' in monster_attack_outcomes:
                    io.msg(f"{battle.monster.name} misses")
                elif 'dodge' in monster_attack_outcomes:
                    io.msg(f"You dodge {battle.monster.name}'{'s'*(not battle.monster.name.endswith('s'))} attack")
            
            io.cls()
            time.sleep(.2)
            if player_start:
                show_player_outcomes()
                time.sleep(.5)
                show_monster_outcomes()
            else:
                show_monster_outcomes()
                time.sleep(.5)
                show_player_outcomes()
            time.sleep(1.5)
            if('kill' in player_attack_outcomes):
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
            io.progress_bar(battle.player.hp, battle.player.attributes['health'], 25, battle.player.name, True)
            io.skip_line(4)
            io.progress_bar(battle.monster.hp, battle.monster.attributes['health'], 25, battle.monster.name, True)
            io.skip_line(4)
            #io.msg(f"{battle.player.name}'s HP: {battle.player.hp}/{battle.player.attributes['health']}")
            #io.msg(f"{battle.monster.name}'s HP: {battle.monster.hp}/{battle.monster.hp_max}")

            options = {
                "*Attack"    : attack,
                "*Inventory" : self.inventory,
                "*Stats"     : self.stats,
                "*Run"       : STATUS.ESCAPE,
            }
            c = io.map_menu("Choose an option", options.keys(), "*Run")
            fighting = options.get(c, STATUS.CONTINUE)()
            io.cls()

        looting = battle.monster.is_dead()
        while looting:
            options = {
                "*Loot"      : self.loot,
                "*Inventory" : self.inventory,
                "*Stats"     : self.stats,
                "*Return to dungeon" : STATUS.ESCAPE,
            }
            c = io.map_menu("Choose an option", options.keys(), "*Return to dungeon")
            looting = options.get(c, STATUS.CONTINUE)()
            io.cls()

        io.msg("Returning to dungeon...", duration=1)
        io.cls()
        return STATUS.SUCCESS
    
    
    def loot(self):
        io.cls()
        gold = random.randint(10, 30)
        self.player.inventory.gold += gold
        io.acknowledge(f"You found {gold} gold!")
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
                self.player.base_attributes['health'] = 100
                self.player.base_attributes['attack'] = 10
                self.player.base_attributes['defence'] = 10
                self.player.set_attributes(level = 1)
                self.player.exp = 0
                self.player.inventory.gold = 300
                self.player.inventory.capacity = 4
                for item_name in self.ITEMS_START:
                    item = Item(item_name, **self.items[item_name])
                    self.player.inventory.add(item)
                creating_char = False
            io.cls()
        self.town()
        return STATUS.SUCCESS

    #Main Menu/Load Game screen
    def mm_load_game(self):
        io.cls()
        self.player = Player()
        if load_game('config/save.json', self.player, self.items):
            self.player.set_attributes(level=self.player.level)
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
