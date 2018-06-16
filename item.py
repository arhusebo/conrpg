class Item():
    """Container class for holding item data"""
    def __init__(self, name, **kwargs):
        self.name = name
        self.consumable = kwargs.get('consumable', False)
        self.value = kwargs.get('value', 0)
        self.info = kwargs.get('info', "")
        self.attack = kwargs.get('attack', 0)
        self.defense = kwargs.get('defense', 0)
        self.restore_values = kwargs.get('restore', None)
