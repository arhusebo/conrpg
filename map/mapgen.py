"""
TODO: Add seed-argument to generator
"""

import random
from mapobj import Tile, Map
        

def dungeon_generator(width, height, seed):
    map_ = Map(width, height)
    
    map_.entry(seed)
    active = [seed]
    
    max_number_of_rooms = random.randint(40, 50)
    total_number_of_rooms = 0
    while active:
        room = active.pop()
        free_directions = map_.free_directions(room)
        directions = [
            list(free_directions.values())[k] for k in
            random.sample(range(len(free_directions)), random.randint(1, len(free_directions)))
        ]
        length = random.randint(1, 3)
        
        # Tries to make a hallway in each of the direction
        # This *may* be in the direction in which it came from...
        for direction in directions:
            hall = room
            for i in range(length):
                try:
                    next_hall = map_.neighbour(hall, direction)
                except IndexError: #Out of bounds
                    pass
                
                if next_hall.is_empty() and next_hall.has_one_connection():
                    hall.connect(next_hall)
                    next_hall.connect(hall)
                    
                    hall = next_hall
                    hall.variant = 'O'
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
            if room.is_available() and room.has_one_connection():
                room.variant = 'T'
                hall_ends.append(room)
    
    special_rooms = iter(random.sample(hall_ends, 1))
    special_rooms.__next__().variant = 'B'
    
    return map_
    
def border_entry(width, height):
    # Selects a random index at a random edge
    seed_side = random.choice(('N', 'S', 'E', 'W'))
    if seed_side in {'N', 'S'}:
        y = 0 if seed_side == 'N' else height-1
        x = random.randint(1, width-1)
    else: #in {'E', 'W'}
        y = random.randint(1, height-1)
        x = 0 if seed_side == 'E' else width-1
    
    tile = Tile(x, y, variant='E')
    tile.connections.append(seed_side)
    
    return tile

if __name__ == "__main__":
    seed = border_entry(20, 10)
    dungeon = dungeon_generator(20, 10, seed)
    print(dungeon)
    
    