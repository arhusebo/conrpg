from item import Inventory, Equippable
from stats import Stats

class Actor():
    """Base Actor class, not meant to be used on its own, but rather inherited from."""

    base_stats = Stats(health=1.0,
                        attack=0.0,
                        defense=0.0,
                        accuracy=0.7,
                        evasion=0.3,
                        speed=1.0)

    def __init__(self, name="Actor", level=1, base_stats=base_stats):
        self.name = name
        self.level = level
        self.alive = True
        self.inventory = Inventory(capacity = 0, gold = 0)
        self.base_stats = base_stats
        self.status_effects = []
        self.update_status_effects()
        self.set_level(level)
        self.hp = self.get_stats().health

    def update(self):
        self.update_status_effects()
        self.inventory.update_equipment_stats()

    def update_status_effects(self):
        self.effect_stats = Stats()
        for effect in self.status_effects:
            if not effect.active:
                del effect
            else:
                effect.tick()

    def get_stats(self):
        return self.stats + self.inventory.equipment_stats + self.effect_stats

    def heal(self, amount):
        self.hp = min(self.hp + amount, self.get_stats().health)

    def damage(self, amount):
        self.hp = max(0, self.hp - amount)

    def set_level(self, level):
        """Sets actor stats based on level"""
        self.level = level
        self.stats = Stats()
        self.stats.attack = self.base_stats.attack + (level - 1)
        self.stats.defense = self.base_stats.defense + (level - 1)
        self.stats.accuracy = self.base_stats.accuracy + (level - .1)
        self.stats.evasion = self.base_stats.evasion + (level - .1)
        self.stats.speed = self.base_stats.speed
        self.stats.health = self.base_stats.health + 10 * (level - 1)

class Player(Actor):
    """Player class for player specific data and methodology."""
    def __init__(self, *args):
        super().__init__(*args)
        self.exp = 0

    def get_exp_next_level(self):
        """Returns total exp required for the next level"""
        return int(100 * pow(self.level, 1.9))

    def check_levelup(self):
        return self.exp > self.get_exp_next_level()

    def levelup(self):
        while self.exp > self.get_exp_next_level():
            self.level += 1
            self.set_level(self.level)


class Monster(Actor):
    """Monster class for monster specific data and methodology."""
    def __init__(self, *args):
        super().__init__(*args)

if __name__ == '__main__':
    actor = Actor(health=100)
    actor.add_status_effect("healing", 3)
    actor.add_status_effect("damaging", 2)
    for i in range(4):
        print(actor.status_effects, actor.hp)
        actor.turn()
