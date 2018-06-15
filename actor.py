class Actor():
    '''Base Actor class, not meant to be used on its own, but rather inherited from.'''
    def __init__(self):
        self.name = "Actor"
        self.level = 1
        self.gold =  0
        self.inventory = []
        self.inventorySlots = 0

        self.base_hp = 1
        self.base_attack = 0
        self.base_defense = 0
        self.hpMax = self.base_hp
        self.hp = self.base_hp
        self.attack = self.base_attack
        self.defense = self.base_defense

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
        self.hp = min(self.hpMax, self.hp + amount)

    def damage(self, amount):
        '''Damages the actor by given amount.'''
        self.hp = min(0, self.hp - amount)

    def getBonusAttack(self):
        '''Returns bonus attack value based on inventory items.'''
        bonusAttack = sum(item.attack for item in self.inventory if item.attack)
        return bonusAttack

    def getBonusDefense(self):
        '''Returns bonus defense value based on inventory items.'''
        bonusDefense = sum(item.defense for item in self.inventory if item.defense)
        return bonusDefense

    def isDead(self):
        '''Returns True if actor is dead.'''
        return self.hp == 0

    def getInventoryItemNames(self):
        '''Returns a list containing names of alle the items in the inventory'''
        names = [item.name for name in self.inventory]
        return names

    def setAttributes(self, level):
        '''Sets actor level and updates stats accordingly'''
        self.attack = self.base_attack + level - 1
        self.defense = self.base_defense + level - 1
        self.hpMax = self.base_hp + 10 * (level - 1)
        self.hp = self.hpMax

class Player(Actor):
    '''Player class for player specific data and methodology.'''
    def __init__(self):
        super().__init__()
        self.exp = 0

    def getExpNextLevel(self):
        '''Returns required experience for leveling up.'''
        return int(100 * pow(self.level, 1.9))

    def checkLevelup(self):
        '''Returns True if player has levelled up based on experience.'''
        return self.exp > self.getExpNextLevel()
    
    def levelup(self):
        '''Sets actor level and increases their attributes'''
        while self.exp > self.getExpNextLevel():
            self.level += 1
            self.setAttributes(self.level)

    def removeGold(self, amount):
        '''Removes given amount. Returns False if there is insufficient gold available.'''
        if self.gold < amount:
            return False
        self.gold -= amount
        return True

class Monster(Actor):
    '''Monster class for monster specific data and methodology.'''
    def __init__(self, name, **kwargs):
        super().__init__()
        self.name = name

        self.base_hp = kwargs.get('hp', 1)
        self.base_attack = kwargs.get('attack', 0)

        self.hpMax = self.base_hp
        self.hp = self.hpMax
        self.attack = self.base_attack

        self.levelMin = kwargs.get('levelMin', 0)
        self.levelMax = kwargs.get('levelMax', 0)
