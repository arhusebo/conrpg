import os
import json
from item import Item

def saveGame(path, player):
    data = {}
    data['name'] = player.name
    data['level'] = player.level
    data['exp'] = player.exp
    data['gold'] = player.gold
    data['hpMax'] = player.hpMax
    data['hp'] = player.hp
    data['attack'] = player.attack
    data['defense'] = player.defense
    data['inventory'] = player.getInventoryItemNames()
    data['inventorySlots'] = player.inventorySlots
    data['base_hp'] = player.base_hp
    data['base_attack'] = player.base_attack
    data['base_defense'] = player.base_defense

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w') as f:
        dataString = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        f.write(dataString)

def loadGame(path, player, items):
    data = {}
    if(os.path.exists(os.path.dirname(path))):
        with open(path, 'r') as f:
            data = json.loads(f.read())
    else:
        return False

    inventoryItems = []
    for item in data.get('inventory'):
        inventoryItems.append(Item(item, **items[item]))

    player.name = data.get('name', "Player")
    player.level = data.get('level', 1)
    player.exp = data.get('exp', 0)
    player.gold = data.get('gold', 0)
    player.hpMax = data.get('hpMax', 1)
    player.hp = data.get('hp', 1)
    player.attack = data.get('attack', 0)
    player.defense = data.get('defense', 0)
    player.inventory = inventoryItems
    player.inventorySlots = data.get('inventorySlots', [])
    player.base_hp = data.get('base_hp', 1)
    player.base_attack = data.get('base_attack', 0)
    player.base_defense = data.get('base_defense', 0)

    return True
