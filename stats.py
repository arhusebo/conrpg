class Stats:
    '''Base Actor Stats data class'''
    def __init__(self,
                health=0.0,
                attack=0.0,
                defense=0.0,
                accuracy=0.0,
                evasion=0.0,
                speed=0.0):
        self.health = health
        self.attack = attack
        self.defense = defense
        self.accuracy = accuracy
        self.evasion = evasion
        self.speed = speed

    def __add__(self, other):
        health = self.health + other.health
        attack = self.attack + other.attack
        defense = self.defense + other.defense
        accuracy = self.accuracy + other.accuracy
        evasion = self.evasion + other.evasion
        speed = self.speed + other.speed
        return Stats(health, attack, defense, accuracy, evasion, speed)

if __name__ == '__main__':
    stats = Stats()
    print(stats)
