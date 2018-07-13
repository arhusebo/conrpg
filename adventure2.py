import random
import maps.mapgen
import conio as io
from status import STATUS
from listener import get_key
from functools import partial
from textwrap import dedent
from maps.mapobj import VARIANT, Warp, Tile2, Room, Chart
from maps.directions import NORTH, EAST, SOUTH, WEST, DIRECTIONS


class ROOM_PRESETS:
    default = dedent("""
        wwwwwww
        wooooow
        wooooow
        wooooow
        wooooow
        wooooow
        wwwwwww
        """.strip('\n'))
    boss = default
    treasure = default
    unexplored = dedent("""
        wwwwwww
        wuuuuuw
        wuuuuuw
        wuuuuuw
        wuuuuuw
        wuuuuuw
        wwwwwww
        """.strip('\n'))
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
    
    if room.coords() in room.parent.treasures:
        room.add_treasure()
        
    if room.coords() in room.parent.monsters:
        room.add_monster()
    
    return room

def warp_generator(room):
    if room.coords() in room.parent.explored:
        preset = room.parent.explored.get(room.coords())
    elif room.symbol in {VARIANT.ROOM, VARIANT.BOSS, VARIANT.TREASURE}:
        preset = ROOM_PRESETS.unexplored
    else: # Placeholder room
        preset = ROOM_PRESETS.wall
    
    # Get width and height of preset
    width = preset.index('\n')
    height = preset.count('\n')
    
    # Make children
    room.fill(width=height, height=width, child_constructor=Warp)
    
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
                'u' : VARIANT.UNEXPLORED,
            }.get(c, VARIANT.WALL)
    
    return room

def connect_bordering_tiles(room):
    #This only connects connections, no need to connect unconnected neighbours
    for d in room.connections:
        connection = room.neighbours[d]
        dx, dy = d
        e = room.edge_index(d)
        e_o = connection.edge_index(-d) #opposite
        
        # checks if connected room is positioned horizontally
        if dx:
            for j in range(room.height()):
                tile = room[j][e]
                tile_o = connection[j][e_o]
                
                if tile.symbol == tile_o.symbol == VARIANT.WALKABLE:
                    tile.neighbours[d] = tile_o
                    tile.connections.add(d)
        
        # checks if connected room positioned vertically
        else:
            for i in range(room.width()):
                tile = room[e][i]
                tile_o = connection[e_o][i]
                
                if tile.symbol == tile_o.symbol == VARIANT.WALKABLE:
                    tile.neighbours[d] = tile_o
                    tile.connections.add(d)
                    

class View:
    def __init__(self, n9):
        self.center_room = n9[1][1]
        
        width = self.center_room .width()
        height = self.center_room .height()
        self.index = [[None for i in range(3*width)] for j in range(3*height)]
        for i in range(len(self.index)):
            for j in range(len(self.index[0])):
                #charlie foxtrot
                self.index[j][i] = n9 [j//height][i//width] [j%height][i%width]
        
    def __str__(self):
        string = []
        for row in self.index:
            for tile in row:
                string.append(tile.symbol)
            string.append('\n')
        return ''.join(string)
    
    def render(self, player_tile):
        o = 2 #offset
        string = [[] for _ in range(o+7+o)]
        for i, row in enumerate(self.index[7-o:14+o]):
            for tile in row[7-o:14+o]:
                string[i].append(tile.symbol)
        
        for coords, treasure in self.center_room.treasure.items():
            tx, ty = coords
            string[ty+o][tx+o] = treasure
            
        for coords, monster in self.center_room.monster.items():
            mx, my = coords
            string[my+o][mx+o] = monster
        
        x, y = player_tile.coords()
        string[y+o][x+o] = "{}"
                
        return '\n'.join((''.join(l) for l in string))



class Adventure:
    def __init__(self, game):
        self.game = game

    def build_dungeon(self):
        #Make empty dungeon
        self.dungeon = Chart(x=0, y=0, parent=None)
        #Fill dungeon with empty children
        self.dungeon.fill(width=20, height=10, child_constructor=Room)
        #Choose a seed (at border)
        self.seed = maps.mapgen.border_entry2(self.dungeon)
        #Make rooms starting from seed
        maps.mapgen.dungeon_generator2(self.dungeon, self.seed)
        #Add treasures and monsters
        self.dungeon.add_treasures()
        self.dungeon.add_monsters()
        
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
        
        self.view = View(n9) # create an index containing all the tiles in the rooms in n9
    
    def available_tile(self):
        for row in self.current_room:
            for tile in row:
                if isinstance(tile, Tile2) and tile.symbol == VARIANT.WALKABLE:
                    return tile

    def move_player(self, direction):
        if direction in self.player_tile.connections:
            next_tile = self.player_tile.neighbours[direction]
            if isinstance(next_tile, Warp):
                coords = next_tile.coords() #save tile coords
                x, y = self.current_room.coords()
                self.build_room(x+direction.x, y+direction.y)
                #move player to new room
                self.player_tile = self.current_room[coords[1]][coords[0]]
            else:
                self.player_tile = self.player_tile.neighbours[direction]
        
        c = self.player_tile.coords()
        if c in self.current_room.treasure:
            io.acknowledge("You found a treasure!")
            self.game.loot()
            self.current_room.treasure.pop(c)
            self.dungeon.treasures.pop(self.current_room.coords())
            
        if c in self.current_room.monster:
            io.acknowledge("You encountered a monster. Prepare to fight!")
            self.game.battle()
            self.current_room.monster.pop(c)
            self.dungeon.monsters.pop(self.current_room.coords())
        
        return STATUS.SUCCESS

def adventure(game):
    io.msg("Delving into the deeps", duration=1)
    
    adv = Adventure(game)
    adv_rnd = io.AdventureRenderer(adv)
    adv.build_dungeon()
    adv.build_room(adv.seed.x, adv.seed.y)
    adv.player_tile = adv.available_tile() #initial room
    
    dungeoning = True
    while dungeoning:
        io.cls()
        print(adv.view.render(adv.player_tile))
        
        key = get_key()
        dungeoning = {
            'w': partial(adv.move_player, NORTH),
            'd': partial(adv.move_player, EAST),
            's': partial(adv.move_player, SOUTH),
            'a': partial(adv.move_player, WEST),
            'ESC': STATUS.ESCAPE,
        }.get(key, lambda: None)()
    
    io.msg("Returning to town...", duration=1)
    
    return STATUS.SUCCESS

if __name__ == '__main__':
    adventure()