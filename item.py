class Item():
    """Container class for holding item data"""
    def __init__(self, name, value=0, info='', **kwargs):
        self.name = name
        self.value = value
        self.info = info
        
class Consumable(Item):
    def __init__(self, restore, **kwargs):
        super().__init__(**kwargs)
        self.restore = restore
        
    
class Weapon(Item):
    def __init__(self, attack, **kwargs):
        super().__init__(**kwargs)
        self.attack = attack
    
class Armour(Item):
    def __init__(self, defence, **kwargs):
        super().__init__(**kwargs)
        self.defence = defence
    
class Collectible(Item):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
    
def Item_constructor(name):
    Constructor = {
        "consumable"  : Consumable,
        "weapon"      : Weapon,
        "armour"      : Armour,
        "collectible" : Collectible,
    }.get(name, Item)
    
    def import_from_json(path):
        import json
        with open(path, 'r') as f:
            return json.loads(f.read())
        
    item_dict = import_from_json("data/items.json")[name]
    return Constructor(name=name, **item_dict)