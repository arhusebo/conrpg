"""
TODO: Add seed-argument to generator
"""

import random

class Tile:
    __slots__ = ['tile', 'x', 'y', 'neighbours']
    def __init__(self, tile, x, y):
        self.tile = tile
        self.x, self.y = (x, y)
    
    def __str__(self):
        return self.tile
    
    def neighbour(self, map_, direction):
        y = self.y + direction[1]
        x = self.x + direction[0]
        if y<0 or x<0:
            raise IndexError
        return map_[y][x]
    
    def has_one_neighbour(self, map_):
        s = 0
        for direction in {(1,0),(-1,0),(0,1),(0,-1)}:
            try:
                n = self.neighbour(map_, direction)
                s += n.tile in 'EBTO'
            except IndexError: pass
        return s==1
    
    def is_empty(self):
        return self.tile == ' '
    
    def is_available(self):
        return self.tile == 'O'
            
        
        
class Map:
    def __init__(self, width, height):
        self.tiles = [[Tile(' ', i, j) for i in range(width)] for j in range(height)]
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
    seed_side = random.choice(('N', 'S', 'E', 'W'))
    if seed_side in {'N', 'S'}:
        y = 0 if seed_side == 'N' else height-1
        x = random.randint(1, width-1)
    else: #in {'E', 'W'}
        y = random.randint(1, height-1)
        x = 0 if seed_side == 'E' else width-1
    
    map_.entry = map_[y][x]
    map_.entry.tile = 'E'
    active = [map_.entry]
    
    max_number_of_rooms = random.randint(40, 50)
    total_number_of_rooms = 0
    while active:
        room = active.pop()
        directions = [{
            'N': ( 0, 1),
            'S': ( 0,-1),
            'E': ( 1, 0),
            'W': (-1, 0),
        }[k] for k in random.sample({'N', 'S', 'E', 'W'}, random.randint(1, 4))]
        length = random.randint(1, 3)
        
        # Tries to make a hallway in each of the direction
        # This *may* be in the direction in which it came from...
        for direction in directions:
            hall = room
            for i in range(length):
                try:
                    next_hall = hall.neighbour(map_, direction)
                except IndexError: #Out of bounds
                    break
                
                if next_hall.is_empty() and next_hall.has_one_neighbour(map_):
                    hall = next_hall
                    hall.tile = 'O'
                    total_number_of_rooms += 1
                else: #end of path
                    break
            else:
                active.append(hall)
                    
            if total_number_of_rooms > max_number_of_rooms: break
        if total_number_of_rooms > max_number_of_rooms: break
    
    hall_ends = []
    for row in map_:
        for room in row:
            if room.is_available() and room.has_one_neighbour(map_):
                room.tile = 'T'
                hall_ends.append(room)
    
    special_rooms = iter(random.sample(hall_ends, 1))
    special_rooms.__next__().tile = 'B'
    
    return map_
    
if __name__ == "__main__":
    dungeon = dungeon_generator(20, 10)
    print(dungeon)
    
    