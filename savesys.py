import os
import json
import configparser
from item import Item_constructor, Inventory

class Settings:
    """Instantiable class for reading and writing settings"""
    defaults = {'graphics': 'ascii',
                'underline': 'true'}
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

    def read_boolean(self, key):
        return self.cfg['SETTINGS'].getboolean(key)

    def write(self, key, value):
        self.cfg['SETTINGS'][key] = value
        with open(self.path, 'w') as f:
            self.cfg.write(f)

def save_game(path, player):
    data = {}
    data['name'] = player.name
    data['level'] = player.level
    data['exp'] = player.exp
    data['gold'] = player.inventory.gold
    data['hp'] = player.hp
    data['inventory'] = player.inventory.item_names()
    data['inventory_slots'] = player.inventory.capacity
    data['base_attributes'] = player.base_attributes

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

    player.name = data.get('name', "Player")
    player.level = data.get('level', 1)
    player.exp = data.get('exp', 0)
    player.hp = data.get('hp', 1)
    player.inventory = Inventory(
        capacity = data.get('inventory_slots', 0),
        gold = data.get('gold', 0)
    )
    for item_name in data.get('inventory'):
        player.inventory.add(Item_constructor(item_name))
    player.base_attributes = data.get('base_attributes')
    
    return True
