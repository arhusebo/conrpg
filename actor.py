class Actor():
    """Base Actor class, not meant to be used on its own, but rather inherited from."""
    def __init__(self):
        self.name = "Actor"
        self.level = 1
        self.gold =  0
        self.inventory = {}
        self.inventory_slots = 0

        self.base_hp = 1
        self.base_attack = 0
        self.base_defense = 0
        self.hp = self.hp_max = self.base_hp
        self.attack = self.base_attack
        self.defense = self.base_defense

    def add_item(self, item):
        """Tries to add item to actor inventory based on available inventory slots.

        Parameters:
        name -- name of item being added
        item -- dictionary containing key-value pairs of attributes

        Returns:
        True if added successfully, False otherwise
        """
        if len(self.inventory) < self.inventory_slots:
            self.inventory[item.name] = item
            return True
        return False

    def heal(self, amount):
        self.hp = min(self.hp_max, self.hp + amount)

    def damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def get_bonus_attack(self):
        return sum(item.attack for item in self.inventory.values() if item.attack)

    def get_bonus_defense(self):
        return sum(item.defense for item in self.inventory.values() if item.defense)

    def is_dead(self):
        return self.hp == 0

    def get_inventory_item_names(self):
        return [item.name for item in self.inventory]

    def set_attributes(self, level):
        """Sets actor stats based on level"""
        self.level = level
        self.attack = self.base_attack + level - 1
        self.defense = self.base_defense + level - 1
        self.hp_max = self.base_hp + 10 * (level - 1)
        self.hp = self.hp_max

class Player(Actor):
    """Player class for player specific data and methodology."""
    def __init__(self):
        super().__init__()
        self.exp = 0

    def get_exp_next_level(self):
        """Returns total exp required for the next level"""
        return int(100 * pow(self.level, 1.9))

    def check_levelup(self):
        return self.exp > self.get_exp_next_level()

    def levelup(self):
        while self.exp > self.get_exp_next_level():
            self.level += 1
            self.set_attributes(self.level)

    def remove_gold(self, amount):
        """Removes given amount. Returns False if there is insufficient gold available."""
        if self.gold < amount:
            return False
        self.gold -= amount
        return True

class Monster(Actor):
    """Monster class for monster specific data and methodology."""
    def __init__(self, name, **kwargs):
        super().__init__()
        self.name = name

        self.base_hp = kwargs.get('hp', 1)
        self.base_attack = kwargs.get('attack', 0)

        self.hp = self.hp_max = self.base_hp
        self.attack = self.base_attack

        self.level_min = kwargs.get('level_min', 0)
        self.level_max = kwargs.get('level_max', 0)
