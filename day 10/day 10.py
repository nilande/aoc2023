import re

#
# Process input
#
with open('day 10/input.txt', 'r') as file:
    sketch = file.read()
width = sketch.find('\n') + 1
height = (len(sketch) + 1) // width

def to_tile(pos):
    return (pos // width, pos % width)

def to_index(tile):
    row, col = tile
    return row * width + col

def is_tile_valid(tile):
    row, col = tile
    if 0 <= col < width-1 and 0 <= row < height: return True
    else: return False

def get_neighbors(tile):
    row, col = tile
    match sketch[to_index(tile)]:
        case 'S': connections = [(row, col+1), (row, col-1), (row+1, col), (row-1, col)]
        case '|': connections = [(row+1, col), (row-1, col)]
        case '-': connections = [(row, col+1), (row, col-1)]
        case 'L': connections = [(row, col+1), (row-1, col)]
        case 'J': connections = [(row, col-1), (row-1, col)]
        case '7': connections = [(row, col-1), (row+1, col)]
        case 'F': connections = [(row, col+1), (row+1, col)]
        case _: return set()
    connections = [tile for tile in connections if is_tile_valid(tile)]
    return set(connections)

def colored_pipe_sketch(pipe, inside_tiles):
    sketch_col = sketch
    pipe_indexes = [to_index(tile) for tile in pipe]
    inside_indexes = [to_index(tile) for tile in inside_tiles]
    indexes = sorted(pipe_indexes + inside_indexes, reverse=True)
    for index in indexes:
        if index in pipe_indexes: sketch_col = sketch_col[:index] + '\033[91m' + sketch_col[index:index+1] + '\033[0m' + sketch_col[index+1:]
        else: sketch_col = sketch_col[:index] + '\033[93m' + sketch_col[index:index+1] + '\033[0m' + sketch_col[index+1:]

    return sketch_col

#
# Puzzle 1
#
start = to_tile(sketch.find('S'))
pipe = {start}
pipe_steps = {start: 0}
steps = 0
search_queue = get_neighbors(start)

while len(search_queue) > 0:
    steps += 1
    next_search_queue = []
    for search_tile in search_queue:
        neighbors = get_neighbors(search_tile)
        # Verify that any neighbor is part of the pipe, mainly needed for start tile
        if pipe & neighbors:
            pipe.add(search_tile)
            pipe_steps[search_tile] = steps
            next_search_queue = next_search_queue + list(neighbors-pipe)
    search_queue = next_search_queue

#
# Puzzle 2
#

# Use the output from below to determine the shape of the start tile
neighbors = get_neighbors(start)
for neighbor in neighbors:
    next_neighbors = get_neighbors(neighbor)
    if {start} & next_neighbors:
        print(f'Start tile: {start} is neighbor with: {neighbor}')

inside_tiles = set()
for row in range(height):
    inside = False
    for col in range(width-1):
        tile = (row, col)
        if tile in pipe:
            match sketch[to_index(tile)]:
                case 'L': inside = not inside
                case 'J': inside = not inside
                case '|': inside = not inside
                case 'S': inside = not inside # Validate whether S should be included depending on its shape
        else:
            if inside: inside_tiles.add(tile)

print(colored_pipe_sketch(pipe, inside_tiles))
print(f'Puzzle 1 solution is: {max(pipe_steps.values())}')
print(f'Puzzle 2 solution is: {len(inside_tiles)}')