global items, items_start, items_shop

items = {
    'Stick': {'value': 0, 'attack':1, 'info':'Just a stick, nothing special'},
    'Wooden Shield': {'value':0, 'defense': 1, 'info':'Simple shield made of a piece of driftwood'},
    'Health Potion': {'value':10, 'consumable': True, 'info':'Potion that restores health points'},
    'Rusted Sword': {'value':1, 'attack':3, 'info': 'Old, worn and rusted sword, probably iron'},
    'Steel Sword': {'value': 30, 'attack':8, 'info': 'Robust sword made of steel'},
    'Knight Shield': {'value':45, 'defense': 5, 'info':'Strong shield made for a knight'}
}
items_start = ['Stick', 'Wooden Shield']
items_shop = ['Steel Sword', 'Health Potion', 'Knight Shield']

class Item():
    '''Container class for holding item data'''
    def __init__(self):
        self.name = "Item"
        self.consumable = False
        self.value = 0
        self.info = "Default item"
        self.attack = 0
        self.defense = 0

    def createFromDict(self, name, item):
        '''Sets item values based on item key-value data pairs

        Parameters:
        name -- key of data pair
        item -- value dictionary of data pair
        '''
        self.name = name
        self.consumable = item.get('consumable')
        self.value = item.get('value')
        self.info = item.get('info')
        self.attack = item.get('attack')
        self.defense = item.get('defense')
