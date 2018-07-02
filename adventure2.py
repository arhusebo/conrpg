import random
import maps.mapgen
from textwrap import dedent
from maps.mapobj import VARIANT, Warp, Tile2, Room, Chart
from maps.directions import NORTH, EAST, SOUTH, WEST, DIRECTIONS


class ROOM_PRESETS:
    default = dedent("""
        wwwowww
        wooooow
        wooooow
        ooooooo
        wooooow
        wooooow
        wwwowww
        """.strip('\n'))
    boss = default
    treasure = default
    wall = dedent("""
        wwwwwww
        wwwwwww
        wwwwwww
        wwwwwww
        wwwwwww
        wwwwwww
        wwwwwww
        """.strip('\n'))
    basic = {
        "basic_1":
            dedent("""
            wwwwwww
            wooooow
            wooooow
            wooooow
            wooooow
            wooooow
            wwwwwww
            """.strip('\n')),
        "basic_2":
            dedent("""
            wwwwwww
            wowowow
            wooooow
            wooooow
            woowoow
            wooooow
            wwwwwww
            """.strip('\n')),
        "basic_3":
            dedent("""
            wwwwwww
            wooooow
            woowoow
            wooooow
            wowowow
            wooooow
            wwwwwww
            """.strip('\n')),
        "basic_4":
            dedent("""
            wwwwwww
            wooooow
            wooooow
            woowoow
            wooooow
            wooooow
            wwwwwww
            """.strip('\n')),
        "basic_5":
            dedent("""
            wwwwwww
            wooooow
            woowoow
            wooooow
            woowoow
            wooooow
            wwwwwww
            """.strip('\n'))
    }

def room_generator(room):
    if room.coords() in room.parent.explored:
        preset = room.parent.explored.get(room.coords())
    else:
        # Double assignment
        preset = room.parent.explored[room.coords()] =\
            ROOM_PRESETS.basic.get(random.choice(tuple(ROOM_PRESETS.basic.keys())))
    
    # Get width and height of preset
    width = preset.index('\n')
    height = preset.count('\n')
    
    # Make children
    room.fill(width=height, height=width, child_constructor=Tile2)
    
    # Turn the room-string into an array for easier manipulation
    room_array = [[c for c in line] for line in preset.splitlines()]
    
    # Block void rooms
    for connection in room.connections:
        e = room.edge_index(connection)
        x, y = connection
        if x:
            room_array[height//2][e] = 'o'
        if y:
            room_array[e][width//2] = 'o'
    
    # Specify room symbols
    for j in range(height):
        for i in range(width):
            c = room_array[j][i]
            tile = room[j][i]
            tile.symbol = {
                'w' : VARIANT.WALL,
                'o' : VARIANT.WALKABLE,
            }.get(c, VARIANT.WALL)
    
    # Connect walkable tiles
    for j in range(height):
        for i in range(width):
            tile = room[j][i]
            if tile.symbol == VARIANT.WALL:
                continue
            for neighbour_dir, neighbour in tile.neighbours.items():
                if neighbour.symbol == VARIANT.WALKABLE:
                    tile.connections.add(neighbour_dir)
                    neighbour.connections.add(-neighbour_dir)
    
    return room

def warp_generator(room):
    if room.coords() in room.parent.explored:
        preset = room.parent.explored.get(room.coords())
    elif room.symbol == VARIANT.ROOM:
        preset = ROOM_PRESETS.default
    else: # Placeholder room
        preset = ROOM_PRESETS.wall
    
    # Get width and height of preset
    width = preset.index('\n')
    height = preset.count('\n')
    
    # Make children
    room.fill(width=height, height=width, child_constructor=Tile2)
    
    # Turn the room-string into an array for easier manipulation
    room_array = [[c for c in line] for line in preset.splitlines()]
    
    # Block void rooms
    for connection in room.connections:
        e = room.edge_index(connection)
        x, y = connection
        if x:
            room_array[height//2][e] = 'o'
        if y:
            room_array[e][width//2] = 'o'
    
    # Specify room symbols
    for j in range(height):
        for i in range(width):
            c = room_array[j][i]
            tile = room[j][i]
            tile.symbol = {
                'w' : VARIANT.WALL,
                'o' : VARIANT.WALKABLE,
            }.get(c, VARIANT.WALL)
    
    return room

def connect_bordering_tiles(room):
    for d in room.connections:
        connection = room.neighbours[d]
        dx, dy = d
        e = room.edge_index(d)
        e_o = connection.edge_index(-d) #opposite
        
        if dx:
            for j in range(room.height()):
                tile = room[j][e]
                tile_o = connection[j][e_o]
                
                if tile.symbol == tile_o.symbol == VARIANT.WALKABLE:
                    tile.neighbours[d] = tile_o
                    tile.connections.add(d)
        
        else:
            for i in range(room.width()):
                tile = room[e][i]
                tile_o = connection[e_o][i]
                
                if tile.symbol == tile_o.symbol == VARIANT.WALKABLE:
                    tile.neighbours[d] = tile_o
                    tile.connections.add(d)
                    

class Adventure:
    def __init__(self):
        self.player_dx = 0
        self.player_dy = 0

    def build_dungeon(self):
        self.dungeon = Chart(x=0, y=0, parent=None)
        self.dungeon.fill(width=20, height=10, child_constructor=Room)
        self.seed = maps.mapgen.border_entry2(self.dungeon)
        maps.mapgen.dungeon_generator2(self.dungeon, self.seed)
        
    def build_room(self, x, y):
        self.current_room = self.dungeon[y][x]
        n9 = self.current_room.surrounding() # 3x3 double list, current_room in center
        for row in n9:
            for room in row:
                if room == self.current_room:
                    room_generator(room)
                else:
                    warp_generator(room)
                    
        # We connect the bordering tiles in the current_room to the connected neighbouring (warp) rooms
        connect_bordering_tiles(self.current_room)
        
        print(repr(self.current_room))
        
        create_view(n9) # create an index containing all the tiles in the rooms in n9
        

    def create_room(self, x, y):
        variant = self.map[y][x].variant
        if variant == 'O':
            preset = random.choice(RoomGen.basic.keys())
        else:
            preset = 'default'
        return RoomGen(preset, self.map[y][x].connections)

    def set_room(self, x, y, room):
        self.rooms[self.width*y+x] = room

    def get_room(self, x, y):
        return self.rooms[self.width*y+x]

    def get_current_room(self):
        return self.current_room

    # player control functions
    def change_room(self, dx, dy):
        new_x = self.current_x+dx
        new_y = self.current_y+dy
        if not self.get_room(new_x, new_y):
            room = self.create_room(new_x, new_y)
            self.set_room(new_x, new_y, room)
        self.current_x = new_x
        self.current_y = new_y
        self.current_room = self.get_room(self.current_x, self.current_y)
        if dx<0:
            self.player_x = self.current_room.width-2
        elif dx>0:
            self.player_x = 1
        if dy<0:
            self.player_y = self.current_room.height-2
        elif dy>0:
            self.player_y = 1

    def get_player_neighbour(self, direction):
        dir = Adventure.directions.get(direction)
        if (direction=='N' and self.player_y>0) or\
            (direction=='S' and self.player_y<self.get_current_room().height) or\
            (direction=='E' and self.player_x<self.get_current_room().width) or\
            (direction=='W' and self.player_x>0):
            return self.get_current_room().neighbour(self.get_current_room().tiles[self.player_y][self.player_x], dir)
        else:
            return None

    def set_player_movement(self, direction):
        destination = self.get_player_neighbour(direction)
        if destination.variant == 'f':
            self.player_dx, self.player_dy = tuple(Adventure.directions.get(direction))
        elif destination.variant == 'd':
            door = destination
            doors = self.current_room.doors
            if door.x == 0:
                self.change_room(-1,0)
            elif door.x == self.current_room.width-1:
                self.change_room(1,0)
            elif door.y == 0:
                self.change_room(0,-1)
            elif door.y == self.current_room.height-1:
                self.change_room(0,1)

    def update(self):
        # update positions
        self.player_x += self.player_dx
        self.player_y += self.player_dy
        # reset deltas
        self.player_dx = 0
        self.player_dy = 0

if __name__ == '__main__':
    import conio as io
    from listener import get_key
    adv = Adventure()
    adv_rnd = io.AdventureRenderer(adv)
    adv.build_dungeon()
    adv.build_room(adv.seed.x, adv.seed.y)
    while(True):
        adv_rnd.draw_room()
        key = get_key()
        if key == 'w':
            adv.set_player_movement('N')
        elif key == 's':
            adv.set_player_movement('S')
        elif key == 'a':
            adv.set_player_movement('W')
        elif key == 'd':
            adv.set_player_movement('E')
        adv.update()
        io.cls()
        adv_rnd.draw_map()
