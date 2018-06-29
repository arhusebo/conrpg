import random
import maps.mapgen
from textwrap import dedent
from maps.mapobj import VARIANT, Tile2, Room, Chart
from maps.directions import NORTH, EAST, SOUTH, WEST, DIRECTIONS


if __name__ == "__main__":
    blank_chart = Chart(x=0, y=0, parent=None)
    blank_chart.fill(width=20, height=10, child_constructor=Room)
    seed = maps.mapgen.border_entry2(blank_chart)
    dungeon = maps.mapgen.dungeon_generator2(blank_chart, seed)
    print(dungeon)

class RoomGen:
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
            wwwowww
            wooooow
            wooooow
            ooooooo
            wooooow
            wooooow
            wwwowww
            """.strip('\n')),
        "basic_2":
            dedent("""
            wwwowww
            wowowow
            wooooow
            ooooooo
            woowoow
            wooooow
            wwwowww
            """.strip('\n')),
        "basic_3":
            dedent("""
            wwwowww
            wooooow
            woowoow
            ooooooo
            wowowow
            wooooow
            wwwowww
            """.strip('\n')),
        "basic_4":
            dedent("""
            wwwowww
            wooooow
            wooooow
            ooowooo
            wooooow
            wooooow
            wwwowww
            """.strip('\n')),
        "basic_5":
            dedent("""
            wwwowww
            wooooow
            woowoow
            ooooooo
            woowoow
            wooooow
            wwwowww
            """.strip('\n'))
    }

    def __init__(self, room, preset):
        self.preset = RoomGen.presets.get(preset, RoomGen.default)
        width = self.preset.index('\n')
        height = self.preset.count('\n')+1
        
        room.fill(width=height, height=width, child_constructor=Tile2)
        
        for i, string in enumerate(self.preset.splitlines()):
            for j, c in enumerate(string):
                tile = room[j][i]
                tile.symbol = {
                    'w' : VARIANT.WALL,
                    'o' : VARIANT.WALKABLE,
                }.get(c, VARIANT.WALL)

class Adventure:
    def __init__(self):
        self.player_dx = 0
        self.player_dy = 0

    def generate_map(self):
        self.width = 20
        self.height = 10
        self.rooms = [None]*self.width*self.height
        seed = maps.mapgen.border_entry(self.width, self.height)
        self.map = maps.mapgen.dungeon_generator(self.width, self.height, seed)
        # add entry room
        self.current_x = self.map.entry.x # per dungeon basis
        self.current_y = self.map.entry.y # per dungeon basis
        self.change_room(0,0) # set initial room
        self.player_x = int(self.get_current_room().width/2) # per room basis
        self.player_y = int(self.get_current_room().height/2) # per room basis

    def create_room(self, x, y):
        variant = self.map[y][x].variant
        if variant == 'O':
            preset = random.choice(['basic_1',
                                    'basic_2',
                                    'basic_3',
                                    'basic_4',
                                    'basic_5'])
        else:
            preset = 'default'
        return Room(preset, self.map[y][x].connections)

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
    from conio import AdventureRenderer, cls
    from listener import get_key
    adv = Adventure()
    adv_rnd = AdventureRenderer(adv)
    adv.generate_map()
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
        cls()
        adv_rnd.draw_map()
