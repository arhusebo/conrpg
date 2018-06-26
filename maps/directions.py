#Directions
from collections import namedtuple
Direction = namedtuple("Direction", ['x', 'y'])
NORTH = Direction(x =  0, y = -1)
EAST  = Direction(x = -1, y =  0)
SOUTH = Direction(x =  0, y =  1)
WEST  = Direction(x =  1, y =  0)
DIRECTIONS = {NORTH, EAST, SOUTH, WEST}

def opposite(direction):
    return {
        NORTH : SOUTH,
        SOUTH : NORTH,
        EAST  : WEST,
        WEST  : EAST,
    }[direction]
      
def symbol(dirs):
    #East and west are reversed ??
    return {
        (0,0,0,0) : ' ',
        (0,0,0,1) : '╞',
        (0,0,1,0) : '╥',
        (0,0,1,1) : '╔',
        (0,1,0,0) : '╡',
        (0,1,0,1) : '═',
        (0,1,1,0) : '╗',
        (0,1,1,1) : '╦',
        (1,0,0,0) : '╨',
        (1,0,0,1) : '╚',
        (1,0,1,0) : '║',
        (1,0,1,1) : '╠',
        (1,1,0,0) : '╝',
        (1,1,0,1) : '╩',
        (1,1,1,0) : '╣',
        (1,1,1,1) : '╬',
    }.get((NORTH in dirs, EAST in dirs, SOUTH in dirs, WEST in dirs), '?')