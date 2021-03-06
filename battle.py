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
        set of outcomes and final damage recieved by defender
        '''
        outcomes = set()
        damage_points = 0
        hit_roll = random.random()
        if attacker.get_stats().accuracy <= hit_roll:
            outcomes.add("miss")
        #elif attacker.get_stats().accuracy * (1-defender.get_stats().evasion) < hit_roll:
        #    outcomes.add("dodge")
        else:
            damage_raw = attacker.get_stats().attack
            deviation = int(random.uniform(-damage_raw/4,damage_raw/4)+.5)
            damage_raw += deviation
            defence = defender.get_stats().defense
            if defence:
                damage_points = int(damage_raw / (defender.get_stats().defense))
            else:
                damage_points = damage_raw
            defender.damage(damage_points)
            outcomes.add("hit")
            if defender.hp<=0:
                outcomes.add("kill")
        return outcomes, damage_points

    def player_attack(self):
        '''Makes player attack monster for one iteration, returning set of outcomes and final damage recieved by monster'''
        result = self.attack(self.player, self.monster)
        return result

    def monster_attack(self):
        '''Makes monster attack player for one iteration, returning set of outcomes and final damage recieved by player'''
        result = self.attack(self.monster, self.player)
        return result

    def turn(self):
        # set default turn outcome values
        player_outcome = set(), 0
        monster_outcome = set(), 0

        player_turn = self.player.get_stats().speed > self.monster.get_stats().speed
        if player_turn:
            player_outcome = self.player_attack()
            if not self.is_battle_over(): monster_outcome = self.monster_attack()
        else:
            monster_outcome = self.monster_attack()
            if not self.is_battle_over(): player_outcome = self.player_attack()
        return player_turn, player_outcome, monster_outcome


    def is_battle_over(self):
        return self.player.hp<=0 or self.monster.hp<=0

    def award_player_exp(self):
        exp_gained = self.monster.level * 20
        self.player.exp += exp_gained
        return exp_gained
