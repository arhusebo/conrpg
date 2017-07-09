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
        damageRaw = attacker.attack + attacker.getBonusAttack()
        deviation = int(random.uniform(-damageRaw/4,damageRaw/4)+.5)
        damageRaw += deviation
        defense = defender.defense + defender.getBonusDefense()
        if defense:
            damage = int(damageRaw / (defender.defense + defender.getBonusDefense()))
        else:
            damage = damageRaw
        defender.damage(damage)
        return damage

    def playerAttack(self):
        '''Makes player attack monster for one iteration, returning final damage recieved by monster.'''
        damage = self.attack(self.player, self.monster)
        return damage

    def monsterAttack(self):
        '''Makes monster attack player for one iteration, returning final damage recieved by player.'''
        damage = self.attack(self.monster, self.player)
        return damage

    def isBattleOver(self):
        '''Returns True if either player or monster is dead.'''
        return self.player.isDead() or self.monster.isDead()

    def awardPlayerExp(self):
        '''Adds experience to the player based on monster level'''
        expGained = self.monster.level * 20
        self.player.exp += expGained
        return expGained
