from enum import Enum
import time

Direction = Enum('Direction', ['RIGHT', 'LEFT', 'DOWN', 'UP'])

#
# Process input
#
with open('day 16/input.txt', 'r') as file:
    grid = file.read()
width = grid.find('\n') + 1
height = (len(grid) + 1) // width

def to_tile(pos):
    return (pos // width, pos % width)

def to_index(tile):
    row, col = tile
    return row * width + col

def is_tile_valid(tile):
    row, col = tile
    if 0 <= col < width-1 and 0 <= row < height: return True
    else: return False

def get_next_directions(tile, direction: Direction):
    next_directions_lookup = {
        Direction.RIGHT: {
            '.': [ Direction.RIGHT ],
            '-': [ Direction.RIGHT ],
            '/': [ Direction.UP ],
            '\\': [ Direction.DOWN ],
            '|': [ Direction.DOWN, Direction.UP ]
        },
        Direction.LEFT: {
            '.': [ Direction.LEFT ],
            '-': [ Direction.LEFT ],
            '/': [ Direction.DOWN ],
            '\\': [ Direction.UP ],
            '|': [ Direction.DOWN, Direction.UP ]
        },
        Direction.DOWN: {
            '.': [ Direction.DOWN ],
            '|': [ Direction.DOWN ],
            '/': [ Direction.LEFT ],
            '\\': [ Direction.RIGHT ],
            '-': [ Direction.RIGHT, Direction.LEFT ]
        },
        Direction.UP: {
            '.': [ Direction.UP ],
            '|': [ Direction.UP ],
            '/': [ Direction.RIGHT ],
            '\\': [ Direction.LEFT ],
            '-': [ Direction.RIGHT, Direction.LEFT ]
        }
    }

    symbol = grid[to_index(tile)]
    next_directions = next_directions_lookup[direction][symbol]
    #print(f'At {tile}, beam encounters {symbol} and changes direction from {direction} to {next_directions}')
    return next_directions

def get_next_tile(tile, direction: Direction):
    match direction:
        case Direction.RIGHT: return tile[0], tile[1]+1
        case Direction.LEFT: return tile[0], tile[1]-1
        case Direction.DOWN: return tile[0]+1, tile[1]
        case Direction.UP: return tile[0]-1, tile[1]


# Work with queue as recursion limit exceeded if written in recursive format
def get_energized_tiles(tile, direction: Direction):
    tile_queue = [ (tile, direction) ]
    visited_tile_directions = set()
    while len(tile_queue) > 0:
        tile, direction = tile_queue.pop(0)
        if not is_tile_valid(tile): continue
        if (tile, direction) in visited_tile_directions: continue
        visited_tile_directions.add((tile, direction))
        next_directions = get_next_directions(tile, direction)
        for next_direction in next_directions:
            next_tile = get_next_tile(tile, next_direction)
            tile_queue.append((next_tile, next_direction))

    return {tile_direction[0] for tile_direction in visited_tile_directions}

#
# Puzzle 1 solution
#
start_time = time.time()
energized_tiles = get_energized_tiles((0, 0), Direction.RIGHT)
print(f'Puzzle 1 solution is: {len(energized_tiles)} (in {time.time() - start_time:.3f} seconds)')

#
# Puzzle 2 solution
#
start_time = time.time()
tile_counts = []
for i in range(width-1):
    tile_counts.append(len(get_energized_tiles((0, i), Direction.DOWN)))
    tile_counts.append(len(get_energized_tiles((height-1, i), Direction.UP)))
for i in range(height):
    tile_counts.append(len(get_energized_tiles((i, 0), Direction.RIGHT)))
    tile_counts.append(len(get_energized_tiles((i, width-2), Direction.LEFT)))

print(f'Puzzle 2 solution is: {max(tile_counts)} (in {time.time() - start_time:.3f} seconds)')