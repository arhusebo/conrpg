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
    def import_from_json(path):
        import json
        with open(path, 'r') as f:
            return json.loads(f.read())

    item_dict = import_from_json("data/items.json")[name]
    
    Constructor = {
        "consumable"  : Consumable,
        "weapon"      : Weapon,
        "armour"      : Armour,
        "collectible" : Collectible,
    }.get(item_dict["type"], Item)
    
    return Constructor(name=name, **item_dict)


class Inventory:
    def __init__(self, capacity, gold):
        self.slots = []
        self.capacity = capacity
        
        self.gold = gold
        
    def __contains__(self, item):
        for slot_item in self.slots:
            if slot_item.name == item.name:
                return True
        return False
        
    def __iter__(self):
        return iter(self.slots)
    
    def item_names(self):
        return [item.name for item in self.slots]
    
    def free_space(self):
        return self.capacity - len(self.slots)
    
    def add(self, item):
        """Tries to add item to actor inventory based on available inventory slots.
        Returns False if the inventory is full."""
        if len(self.slots) < self.capacity:
            self.slots.append(item)
            return True
        return False
    
    def remove(self, item_name):
        for i, slot_item in enumerate(self.slots):
            if slot_item.name == item_name:
                del self.slots[i]
                return slot_item

    def item_by_name(self, item_name):
        for i, slot_item in enumerate(self.slots):
            if slot_item.name == item_name:
                return slot_item
            
    def remove_gold(self, amount):
        """Removes given amount. Returns False if there is insufficient gold available."""
        if self.gold < amount:
            return False
        self.gold -= amount
        return True