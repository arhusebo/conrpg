from .directions import NORTH, EAST, SOUTH, WEST, DIRECTIONS

class Tile:
    __slots__ = ['x', 'y', 'variant', 'connections']
    def __init__(self, x, y, variant):
        self.variant = variant
        self.x, self.y = (x, y)
        self.connections = []

    def __str__(self):
        return self.variant

    def has_one_connection(self):
        return len(self.connections) <= 1

    def is_empty(self):
        return self.variant == ' '

    def is_available(self):
        return self.variant == 'O'

    def connect(self, n):
        dx = n.x-self.x
        dy = n.y-self.y
        direction = {
            ( 0,-1): 'N',
            ( 0, 1): 'S',
            ( 1, 0): 'E',
            (-1, 0): 'W',
        }[(dx, dy)]
        self.connections.append(direction)

class Map:
    def __init__(self, width, height):
        self.tiles = [[Tile(i, j, variant=' ') for i in range(width)] for j in range(height)]
        self.width = width
        self.height = height

    def __str__(self):
        string = []
        for row in self.tiles:
            for tile in row:
                string.append(tile.__str__())
            string.append('\n')
        return ''.join(string)

    def __getitem__(self, index):
        return self.tiles[index]

    def entry(self, tile):
        self[tile.y][tile.x] = tile
        self.entry = tile

    def neighbour(self, tile, direction):
        x = tile.x + direction[0]
        y = tile.y + direction[1]
        if x < 0 or y < 0:
            raise IndexError
        return self[y][x]

    def free_directions(self, tile):
        # Direction space
        directions = {
            'N': ( 0,-1),
            'S': ( 0, 1),
            'E': (-1, 0),
            'W': ( 1, 0),
        }

        # Remove directions with connected neighbours
        for n in tile.connections:
            del directions[n]

        # Remove Out-Of-Bounds directions
        for d_key in set(directions.keys()):
            x = tile.x+directions[d_key][0]
            y = tile.y+directions[d_key][1]
            if (0 <= x < self.width) and (0 <= y < self.height):
                continue
            del directions[d_key]

        # Feasible direction space
        return directions
    

### v2

#Hacky enum
class VARIANT:
    WALL  = '██'
    WALKABLE  = '  '
    UNEXPLORED = '▒▒'
    
    EMPTY = '*'
    ROOM  = 'O'
    ENTRY = 'E'
    BOSS  = 'B'
    TREASURE = 'T'
    
    CHART = '#'


class TREASURE:
    SILVER = '++'

class MONSTER:
    RAT = '::'


class QuadCell:
    __slots__ = ['x', 'y', 'variant', 'symbol', 'parent', 'neighbours', 'connections']
    def __init__(self, x, y, variant, symbol, parent, neighbours=dict()):
        self.x, self.y = (x, y)
        self.variant = variant
        self.symbol = symbol
        self.parent = parent
        self.neighbours = neighbours.copy()
    
    def __str__(self):
        return self.symbol

    def has_one_connection(self):
        return 1 == len(self.connections)

    def is_empty(self):
        return self.variant == VARIANT.EMPTY

    def is_room(self):
        return self.variant == VARIANT.ROOM
    
    def neighbour(self, direction):
        self.neighbours[direction]
        
    def surrounding(self):
        width = self.parent.width()
        height = self.parent.height()
        def T(d):
            n_y = self.y+d.y
            n_x = self.x+d.x
            if (0 <= n_x < width) and (0 <= n_y < height):
                return self.parent[n_y][n_x]
            else:
                return Room(x=n_x, y=n_y, parent=self.parent)
            
        n9 = [
            [T(NORTH+WEST), T(NORTH), T(NORTH+EAST)],
            [T(WEST)      , self    , T(EAST)      ],
            [T(SOUTH+WEST), T(SOUTH), T(SOUTH+EAST)],
        ]
        
        return n9
        
    
    def unconnected(self):
        return self.neighbours.keys() - self.connections
    
    def coords(self):
        return (self.x, self.y)
    
    
class Tree(QuadCell):
    __slots__ = ['children', 'connections']
    def __init__(self, connections=set(), **kwargs):
        super().__init__(**kwargs)
        self.connections = connections.copy()
        
    def __str__(self):
        from .directions import symbol
        string = []
        for row in self.children:
            for child in row:
                string.append(child.symbol)
            string.append('\n')
        return ''.join(string)
    
    def __repr__(self):
        from .directions import symbol
        string = []
        for row in self.children:
            for child in row:
                string.append(symbol(child.connections))
            string.append('\n')
        return ''.join(string)

    def __getitem__(self, y):
        return self.children[y]
    
    def fill(self, width, height, child_constructor):
        self.children = [[child_constructor(x=i, y=j, parent=self) for i in range(width)] for j in range(height)]
        self.make_child_neighbours()
    
    def edge_index(self, direction):
        dx, dy = direction
        if dx:
            return 0 if dx < 0 else self.width()-1
        else:
            return 0 if dy < 0 else self.height()-1
            
    
    def width(self):
        return len(self.children[0])
    
    def height(self):
        return len(self.children)
    
    def make_child_neighbours(self):
        width  = self.width()
        height = self.height()
        for row in self.children:
            for child in row:
                for d in DIRECTIONS:
                    ny = child.y+d.y
                    nx = child.x+d.x
                    #Disallow negative indexes
                    if (0 <= nx < width) and (0 <= ny < height):
                        child.neighbours[d] = self[ny][nx]
    
class Warp(QuadCell):
    """
    Room tile object. Is the child of Room and has no children.
    """
    def __init__(self, **kwargs):
        super().__init__(variant="Warp", symbol=VARIANT.EMPTY, **kwargs)


class Tile2(QuadCell):
    """
    Room tile object. Is the child of Room and has no children.
    """
    def __init__(self, **kwargs):
        super().__init__(variant="Tile", symbol=VARIANT.EMPTY, **kwargs)
        self.connections = set()
    

class Room(Tree):
    """
    Room tile object. Is the child of Chart and contains Tile2 as children.
    """
    __slots__ = ("monster", "treasure")
    def __init__(self, **kwargs):
        super().__init__(variant="Room", symbol=VARIANT.EMPTY, **kwargs)
        self.monster = {}
        self.treasure = {}
    
    def available_tiles(self):
        tiles = []
        for row in self.children[0+1:7-1]:
            for tile in row[0+1:7-1]:
                if tile.symbol == VARIANT.WALKABLE:
                    c = tile.coords()
                    if c in self.monster or c in self.treasure:
                        continue
                    tiles.append(c)
        return tiles
    
    
    def add_treasure(self):
        from random import choice
        self.treasure = {choice(self.available_tiles()): self.parent.treasures[self.coords()]}
    
    def add_monster(self):
        from random import choice
        self.monster = {choice(self.available_tiles()): self.parent.monsters[self.coords()]}
    
class Chart(Tree):
    """
    Chart tile object. Is the child of Overworld and contains Room as children.
    """
    __slots__ = ["monsters", "treasures", "explored"]
    def __init__(self, monsters={}, treasures={}, explored={}, **kwargs):
        super().__init__(variant="Chart", symbol=VARIANT.CHART, **kwargs)
        self.monsters = monsters.copy()
        self.treasures = treasures.copy()
        self.explored = explored.copy()
    
    def add_treasures(self):
        for row in self.children:
            for room in row:
                if room.symbol == VARIANT.TREASURE:
                    self.treasures[room.coords()] = TREASURE.SILVER
        
    def add_monsters(self):
        for row in self.children:
            for room in row:
                if room.symbol == VARIANT.ROOM or room.symbol == VARIANT.BOSS:
                    self.monsters[room.coords()] = MONSTER.RAT

class Overworld(Tree):
    pass