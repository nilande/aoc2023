import time

#
# Process input
#
with open('day 17/input.txt', 'r') as file:
    heatloss_map = file.read()
width = heatloss_map.find('\n') + 1
height = (len(heatloss_map) + 1) // width

#
# Functions
#
def to_index(tile):
    row, col, *_ = tile
    return row * width + col

def is_tile_move_valid(tile_move, max_steps):
    row, col, _, _, straight_steps = tile_move
    if straight_steps <= max_steps and 0 <= col < width-1 and 0 <= row < height: return True
    return False

def find_shortest_path(from_tile, to_tile, min_steps, max_steps):
    row, col = from_tile
    tm_down = (row, col, 1, 0, 0) # row, col, row_step, col_step, straight_steps
    tm_up = (row, col, -1, 0, 0)
    tm_right = (row, col, 0, 1, 0)
    tm_left = (row, col, 0, -1, 0)
    heat_loss = -int(heatloss_map[to_index((row, col))]) # Don't count initial grid value
    # Initialize search queue with following format - search_tile_move, prev_tile_move, heat_loss
    search_queue = [ (tm_down, tm_down, heat_loss), (tm_up, tm_up, heat_loss), (tm_right, tm_right, heat_loss), (tm_left, tm_left, heat_loss)  ]
    reached_tile_moves = dict()

    while len(search_queue) > 0:
        search_queue.sort(key = lambda x: x[2])
        search_tile_move, prev_tile_move, heat_loss = search_queue.pop(0)
        if not is_tile_move_valid(search_tile_move, max_steps): continue
        if search_tile_move in reached_tile_moves.keys(): continue
        reached_tile_moves[search_tile_move] = prev_tile_move
        heat_loss += int(heatloss_map[to_index(search_tile_move)])
        row, col, row_step, col_step, straight_steps = search_tile_move
        if (row, col) == to_tile and straight_steps >= min_steps: break
        if straight_steps >= min_steps:
            next_tile_moves = [
                (row + row_step, col + col_step, row_step, col_step, straight_steps + 1),
                (row + col_step, col - row_step, col_step, -row_step, 1),
                (row - col_step, col + row_step, -col_step, row_step, 1)
            ]
            for next_tile_move in next_tile_moves: search_queue.append((next_tile_move, search_tile_move, heat_loss))
        else: search_queue.append(((row + row_step, col + col_step, row_step, col_step, straight_steps + 1), search_tile_move, heat_loss))

    shortest_path = [ search_tile_move ]
    while (search_tile_move[0], search_tile_move[1]) != from_tile:
        search_tile_move = reached_tile_moves[search_tile_move]
        shortest_path.append((search_tile_move[0], search_tile_move[1]))
    return (shortest_path, heat_loss)

def get_colored_heatloss_map(path: list, endpoints: list):
    heatloss_map_col = heatloss_map
    path_indexes = [to_index(tile) for tile in path]
    endpoint_indexes = [to_index(tile) for tile in endpoints]
    indexes = sorted(path_indexes + endpoint_indexes, reverse=True)
    for index in indexes:
        if index in path_indexes: heatloss_map_col = heatloss_map_col[:index] + '\033[91m' + heatloss_map_col[index:index+1] + '\033[0m' + heatloss_map_col[index+1:]
        else: heatloss_map_col = heatloss_map_col[:index] + '\033[93m' + heatloss_map_col[index:index+1] + '\033[0m' + heatloss_map_col[index+1:]

    return heatloss_map_col

#
# Puzzle 1
#
start_time = time.time()
from_tile = (0, 0)
to_tile = (height-1, width-2)
shortest_path, heat_loss = find_shortest_path(from_tile, to_tile, 0, 3)
heatloss_map_col = get_colored_heatloss_map(shortest_path[1:-1], [shortest_path[0], shortest_path[-1]])
print(heatloss_map_col)
print(f'Puzzle 1 solution is: {heat_loss} (in {time.time() - start_time:.3f} seconds)')

#
# Puzzle 2
#
start_time = time.time()
from_tile = (0, 0)
to_tile = (height-1, width-2)
shortest_path, heat_loss = find_shortest_path(from_tile, to_tile, 4, 10)
heatloss_map_col = get_colored_heatloss_map(shortest_path[1:-1], [shortest_path[0], shortest_path[-1]])
print(heatloss_map_col)
print(f'Puzzle 2 solution is: {heat_loss} (in {time.time() - start_time:.3f} seconds)')
