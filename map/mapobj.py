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
            (-1, 0): 'E',
            ( 1, 0): 'W',
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