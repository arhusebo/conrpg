import random

class Tile:
    __slots__ = ['tile']
    def __init__(self, tile):
        self.tile = tile
    
    def __str__(self):
        return self.tile
        
class Map:
    def __init__(self, width, height):
        self.tiles = [[Tile('O') for i in range(width)] for j in range(height)]
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
        

def dungeon_generator(width, height):
    map_ = Map(width, height)
    
    # Selects a random index at a random edge
    seed_side = random.sample({'N', 'S', 'E', 'W'}, 1)[0]
    seed_index = random.randint(1, {
        'N': width, 'S': width,
        'E': height, 'W': height,
    }[seed_side]-1)
    if seed_side in {'N', 'S'}:
        y_index = 0 if seed_side == 'N' else height-1
        map_[seed_index][y_index].tile = 'X'
    else: #in {'E', 'W'}
        x_index = 0 if seed_side == 'E' else width-1
        map_[x_index][seed_index].tile = 'X'
        
    active = [seed]
    
    while active:
        pass
    
    
    return map_
    
if __name__ == "__main__":
    dungeon = dungeon_generator(20, 20)
    print(dungeon)
    
    