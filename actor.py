class Actor():
    """Base Actor class, not meant to be used on its own, but rather inherited from."""
    
    STATUS_EFFECT_FUNCTIONS = {
        "healing": lambda actor: Actor.heal(actor, 10),
        "damaging": lambda actor: Actor.damage(actor, 5),
    }
    
    def __init__(self):
        self.name = "Actor"
        self.level = 1
        self.gold =  0
        self.inventory = {}
        self.inventory_slots = 0

        self.base_hp = 1
        self.base_attack = 0
        self.base_defence = 0
        self.base_accuracy = .7
        self.base_evasion = .3
        self.base_speed = 1
        self.hp = self.hp_max = self.base_hp
        self.attack = self.base_attack
        self.defence = self.base_defence
        
        self.status_effects = {}

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

    def add_status_effect(self, effect, duration):
        """adds a status effect with a duration of game turns"""
        if effect in Actor.STATUS_EFFECT_FUNCTIONS:
            self.status_effects.update({effect:duration})
    
    def remove_status_effect(self, effect):
        """removes a status effect"""
        del self.status_effects[effect]
    
    def turn(self):
        status_effects = self.status_effects.copy()
        for key in self.status_effects:
            # execute status effect functions
            Actor.STATUS_EFFECT_FUNCTIONS[key](self)
            # tick and remove expired effects
            status_effects[key] -= 1
            if status_effects[key] <= 0:
                del status_effects[key]
        self.status_effects = status_effects

    def heal(self, amount):
        self.hp = min(self.hp_max, self.hp + amount)

    def damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def get_bonus_attack(self):
        from item import Weapon
        return sum(item.attack for item in self.inventory.values() if isinstance(item, Weapon))

    def get_bonus_defence(self):
        from item import Armour
        return sum(item.defence for item in self.inventory.values() if isinstance(item, Armour))
    
    def get_bonus_accuracy(self):
        #return sum(item.accuracy for item in self.inventory.values() if isinstance(item, Item))
        return 0
        
    def get_bonus_evasion(self):
        #return sum(item.evasion for item in self.inventory.values() if isinstance(item, Item))
        return 0
    
    def get_bonus_speed(self):
        #return sum(item.speed for item in self.inventory.values() if isinstance(item, Item))
        return 0

    def get_total_accuracy(self):
        return self.base_accuracy + self.get_bonus_accuracy()

    def get_total_evasion(self):
        return self.base_evasion + self.get_bonus_evasion()
    
    def get_total_speed(self):
        return self.base_speed + self.get_bonus_speed()

    def is_dead(self):
        return self.hp == 0

    def get_inventory_item_names(self):
        return [item.name for item in self.inventory]

    def set_attributes(self, level):
        """Sets actor stats based on level"""
        self.level = level
        self.attack = self.base_attack + level - 1
        self.defence = self.base_defence + level - 1
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

if __name__ == '__main__':
    actor = Actor()
    actor.hp = actor.base_hp = actor.hp_max = 100
    actor.add_status_effect("healing", 3)
    actor.add_status_effect("damaging", 2)
    for i in range(4):
        print(actor.status_effects, actor.hp)
        actor.turn()