class Actor():
    '''Base Actor class, not meant to be used on its own, but rather inherited from.'''
    def __init__(self):
        self.name = "Actor"
        self.level = 1
        self.gold = 0
        self.hpMax = 1
        self.hp = 1
        self.attack = 0
        self.defense = 0
        self.inventory = []
        self.inventorySlots = 0

        self.base_hp = 1
        self.base_attack = 0
        self.base_defense = 0

    def addItem(self, item):
        '''Tries to add item to actor inventory based on available inventory slots.

        Parameters:
        name -- name of item being added
        item -- dictionary containing key-value pairs of attributes

        Returns:
        True if added successfully, False otherwise
        '''
        if len(self.inventory) < self.inventorySlots:
            self.inventory.append(item)
            return True
        return False

    def heal(self, amount):
        '''Heals the actor by given amount, not exceeding max actor HP.'''
        self.hp += amount
        if self.hp >= self.hpMax:
            self.hp = self.hpMax

    def damage(self, amount):
        '''Damages the actor by given amount.'''
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0

    def getBonusAttack(self):
        '''Returns bonus attack value based on inventory items.'''
        bonusAttack = 0
        for item in self.inventory:
            if item.attack:
                bonusAttack += item.attack
        return bonusAttack

    def getBonusDefense(self):
        '''Returns bonus defense value based on inventory items.'''
        bonusDefense = 0
        for item in self.inventory:
            if item.defense:
                bonusDefense += item.defense
        return bonusDefense

    def isDead(self):
        '''Returns True if actor is dead.'''
        if self.hp == 0:
            return True
        return False

    def getInventoryItemNames(self):
        '''Returns a list containing names of alle the items in the inventory'''
        names = []
        for item in self.inventory:
            names.append(item.name)
        return names

    def setLevel(self, level):
        '''Sets actor level and updates stats accordingly'''
        self.level = level
        self.attack = self.base_attack + level-1
        self.defense = self.base_defense + level-1
        self.hpMax = self.base_hp + 10 * (level-1)
        self.hp = self.hpMax

class Player(Actor):
    '''Player class for player specific data and methodology.'''
    def __init__(self):
        Actor.__init__(self)
        self.exp = 0

    def getExpNextLevel(self):
        '''Returns required experience for leveling up.'''
        return int(100 * pow(self.level, 1.9))

    def checkLevel(self):
        '''Sets actor level and returns True if player has levelled up based on experience.'''
        oldLevel = self.level
        while self.exp > self.getExpNextLevel():
            self.setLevel(self.level+1)
        if self.level > oldLevel:
            return True
        return False

    def removeGold(self, amount):
        '''Removes given amount. Returns False if there is insufficient gold available.'''
        if self.gold < amount:
            return False
        self.gold -= amount
        return True

class Monster(Actor):
    '''Monster class for monster specific data and methodology.'''
    def __init__(self, name, type):
        Actor.__init__(self)
        self.name = name

        self.base_hp = type.get('hp')
        self.base_attack = type.get('attack')

        self.hpMax = self.base_hp
        self.hp = self.hpMax
        self.attack = self.base_attack

        self.levelRange = type.get('level')
        self.setLevel(self.levelRange[0])
