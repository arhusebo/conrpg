import random
import maps.mapgen
from textwrap import dedent
from maps.mapobj import VARIANT, Tile2, Room, Chart
from maps.directions import NORTH, EAST, SOUTH, WEST, DIRECTIONS, opposite


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
        x, y = connection
        if x:
            x = (x-1)//2 # 1 -> 0 and -1 -> -1
            room_array[height//2][x] = 'o'
        if y:
            y = (y-1)//2 # 1 -> 0 and -1 -> -1
            room_array[y][width//2] = 'o'
    
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
                    neighbour.connections.add(opposite(neighbour_dir))
    
    return room

class Adventure:
    def __init__(self):
        self.player_dx = 0
        self.player_dy = 0

    def build_dungeon(self):
        blank_chart = Chart(x=0, y=0, parent=None)
        blank_chart.fill(width=20, height=10, child_constructor=Room)
        self.seed = maps.mapgen.border_entry2(blank_chart)
        self.dungeon = maps.mapgen.dungeon_generator2(blank_chart, self.seed)
        
    def build_room(self, x, y):
        blank_room = self.dungeon[y][x]
        self.current_room = room_generator(blank_room)
        print(self.current_room)
        for coords, tile in self.current_room.surrounding():
            warp_generator(neighbour)

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
