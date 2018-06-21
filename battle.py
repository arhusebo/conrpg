import random

class Battle():
    '''Instantiable class containing data and methodology for controlling a battle.'''
    def __init__(self, player, monster):
        self.player = player
        self.monster = monster

    def attack(self, attacker, defender):
        '''Makes attacker attack the defender for one iteration.

        Parameters:
        attacker -- attacking Actor
        defender -- defending Actor

        Returns:
        final damage recieved by defender
        '''
        damage_raw = attacker.attack + attacker.get_bonus_attack()
        deviation = int(random.uniform(-damage_raw/4,damage_raw/4)+.5)
        damage_raw += deviation
        defence = defender.defence + defender.get_bonus_defence()
        if defence:
            damage_points = int(damage_raw / (defender.defence + defender.get_bonus_defence()))
        else:
            damage_points = damage_raw
        defender.damage(damage_points)
        return damage_points

    def player_attack(self):
        '''Makes player attack monster for one iteration, returning final damage recieved by monster.'''
        damage = self.attack(self.player, self.monster)
        return damage

    def monster_attack(self):
        '''Makes monster attack player for one iteration, returning final damage recieved by player.'''
        damage = self.attack(self.monster, self.player)
        return damage

    def is_battle_over(self):
        return self.player.is_dead() or self.monster.is_dead()

    def award_player_exp(self):
        exp_gained = self.monster.level * 20
        self.player.exp += exp_gained
        return exp_gained
