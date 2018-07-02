#Directions
#from collections import namedtuple
#Direction = namedtuple("Direction", ['x', 'y'])
class Direction:
    __slots__ = ('x', 'y')
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
    
    def __str__(self):
        return f"({self.x}, {self.y})"
    
    __repr__ = __str__
    
    def __add__(self, other):
        return Direction(x = self.x + other.x, y = self.y + other.y)
    
    def __neg__(self):
        return Direction(x = -self.x, y = -self.y)
    
    def __iter__(self):
        yield self.x
        yield self.y
        
    # Overload hash and equality for key lookups
    def __hash__(self):
        return hash((self.x, self.y))
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    
NORTH = Direction(x =  0, y = -1)
EAST  = Direction(x =  1, y =  0)
SOUTH = Direction(x =  0, y =  1)
WEST  = Direction(x = -1, y =  0)
DIRECTIONS = {NORTH, EAST, SOUTH, WEST}

def symbol(dirs):
    return {
        (0,0,0,0) : ' ',
        (0,0,0,1) : '╡',
        (0,0,1,0) : '╥',
        (0,0,1,1) : '╗',
        (0,1,0,0) : '╞',
        (0,1,0,1) : '═',
        (0,1,1,0) : '╔',
        (0,1,1,1) : '╦',
        (1,0,0,0) : '╨',
        (1,0,0,1) : '╝',
        (1,0,1,0) : '║',
        (1,0,1,1) : '╣',
        (1,1,0,0) : '╚',
        (1,1,0,1) : '╩',
        (1,1,1,0) : '╠',
        (1,1,1,1) : '╬',
    }.get((NORTH in dirs, EAST in dirs, SOUTH in dirs, WEST in dirs), '?')