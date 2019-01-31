from stats import Stats
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


class Equippable(Item):
    '''Item class for equipment

    Slots:
        0 - Armor
        1 - Helmet
        2 - Feet
        3 - Main-hand
        4 - Off-hand
    '''
    def __init__(self, slot, stats, **kwargs):
        super().__init__(**kwargs)
        self.slot=slot
        self.stats = Stats(**stats)

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
        "equippable"  : Equippable,
        "collectible" : Collectible,
    }.get(item_dict["type"], Item)

    return Constructor(name=name, **item_dict)


class Inventory:
    def __init__(self, capacity, gold):
        self.slots = []
        self.equipment_slots = [None]*5
        self.capacity = capacity

        self.gold = gold
        self.equipment_stats = Stats()

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
            if isinstance(item, Equippable):
                self.equip(item)
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

    def equip(self, item):
        if isinstance(item, Equippable):
            self.equipment_slots[item.slot] = item
            self.update_equipment_stats()

    def unequip(self, slot):
        item = self.slots[slot]
        if isinstance(item, Equippable):
            if item in self.equipment_slots:
                self.equipment_slots[slot] = None
                self.update_equipment_stats()

    def update_equipment_stats(self):
        self.equipment_stats = Stats()
        for slot in self.equipment_slots:
            if slot:
                self.equipment_stats += slot.stats
