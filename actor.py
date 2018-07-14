from item import Inventory

class Actor():
    """Base Actor class, not meant to be used on its own, but rather inherited from."""
    
    STATUS_EFFECT_FUNCTIONS = {
        "healing": lambda actor: Actor.heal(actor, 10),
        "damaging": lambda actor: Actor.damage(actor, 5),
    }
    
    def __init__(self, **kwargs):
        self.name = "Actor"
        self.level = 1
        self.inventory = Inventory(capacity = 0, gold = 0)

        # default base stats
        self.base_stats = {
            "health":   1,
            "attack":   0,
            "defence":  0,
            "accuracy": 0.7,
            "evasion":  0.3,
            "speed":    1,
        }
        
        for key, value in kwargs.items():
            if key in self.base_stats:
                self.base_stats[key] = value
        
        # set current character stats
        self.stats = self.base_stats.copy()
        self.set_stats(self.level)
        
        self.item_stats = {
            "health":0,
            "attack":0,
            "defence":0,
            "accuracy":0,
            "evasion":0,
            "speed":0,
        }
        
        self.effect_stats = {
            "health":0,
            "attack":0,
            "defence":0,
            "accuracy":0,
            "evasion":0,
            "speed":0,
        }
        
        self.status_effects = {}

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
    
    def get_stats():
        return sum(base_stats, item_attribues, )

    def heal(self, amount):
        self.hp = min(self.stats['health'], self.hp + amount)

    def damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def get_bonus_attack(self):
        from item import Weapon
        return sum(item.attack for item in self.inventory if isinstance(item, Weapon))

    def get_bonus_defence(self):
        from item import Armour
        return sum(item.defence for item in self.inventory if isinstance(item, Armour))
    
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
        return self.base_stats['accuracy'] + self.get_bonus_accuracy()

    def get_total_evasion(self):
        return self.base_stats['evasion'] + self.get_bonus_evasion()
    
    def get_total_speed(self):
        return self.base_stats['speed'] + self.get_bonus_speed()

    def is_dead(self):
        return self.hp == 0

    def set_stats(self, level):
        """Sets actor stats based on level"""
        self.level = level
        stats = {
            "attack":self.base_stats["attack"] + level - 1,
            "defence":self.base_stats["defence"] + level - 1,
            "health":self.base_stats["health"] + 10 * (level - 1),
        }
        self.stats = stats

        self.hp = stats["health"]
    
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
            self.set_stats(self.level)


class Monster(Actor):
    """Monster class for monster specific data and methodology."""
    def __init__(self, name, level_min = 0, level_max = 0, **kwargs):
        super().__init__()
        self.name = name
        self.level_min = level_min
        self.level_max = level_max

if __name__ == '__main__':
    actor = Actor(health=100)
    actor.add_status_effect("healing", 3)
    actor.add_status_effect("damaging", 2)
    for i in range(4):
        print(actor.status_effects, actor.hp)
        actor.turn()