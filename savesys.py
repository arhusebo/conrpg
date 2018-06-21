import os
import json
import configparser
from item import Item_constructor

class Settings:
    """Instantiable class for reading and writing settings"""
    defaults = {'graphics': 'ascii'}
    def __init__(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.path = path
        self.cfg = configparser.ConfigParser()
        self.data = self.cfg.read(path)
        if not 'SETTINGS' in self.cfg.sections():
            self.cfg['SETTINGS'] = Settings.defaults
            with open(path, 'w') as f:
                self.cfg.write(f)

    def read(self, key):
        return self.cfg['SETTINGS'][key]

    def write(self, key, value):
        self.cfg['SETTINGS'][key] = value
        with open(self.path, 'w') as f:
            self.cfg.write(f)

def save_game(path, player):
    data = {}
    data['name'] = player.name
    data['level'] = player.level
    data['exp'] = player.exp
    data['gold'] = player.gold
    data['hp_max'] = player.hp_max
    data['hp'] = player.hp
    data['attack'] = player.attack
    data['defense'] = player.defense
    data['inventory'] = list(player.inventory.keys())
    data['inventory_slots'] = player.inventory_slots
    data['base_hp'] = player.base_hp
    data['base_attack'] = player.base_attack
    data['base_defense'] = player.base_defense

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        data_string = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        f.write(data_string)

def load_game(path, player, items):
    data = {}
    if(os.path.exists(os.path.dirname(path))):
        with open(path, 'r') as f:
            data = json.loads(f.read())
    else:
        return False

    inventory_items = {}
    for item_name in data.get('inventory'):
        inventory_items[item_name] = Item_constructor(item_name)

    player.name = data.get('name', "Player")
    player.level = data.get('level', 1)
    player.exp = data.get('exp', 0)
    player.gold = data.get('gold', 0)
    player.hp_max = data.get('hp_max', 1)
    player.hp = data.get('hp', 1)
    player.attack = data.get('attack', 0)
    player.defence = data.get('defence', 0)
    player.inventory = inventory_items
    player.inventory_slots = data.get('inventory_slots', {})
    player.base_hp = data.get('base_hp', 1)
    player.base_attack = data.get('base_attack', 0)
    player.base_defence = data.get('base_defence', 0)

    return True
