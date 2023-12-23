import time
from collections import deque

#
# Classes
#
class Map:
    def __init__(self, map_string: str):
        self.width = map_string.find('\n') + 1
        self.height = (len(map_string) + 1) // self.width
        self.map_string = map_string

        self.paths = set()
        self.slopes = { '^': set(), '>': set(), 'v': set(), '<': set()}
        self.paths_incl_slopes = set()
        self.start = None
        for i, tile in enumerate(map_string):
            match tile:
                case '.':
                    self.paths.add(i)
                    self.paths_incl_slopes.add(i)
                    if self.start is None: self.start = i
                    self.finish = i
                case '^' | '>' | 'v' | '<':
                    self.slopes[tile].add(i)
                    self.paths_incl_slopes.add(i)

    def build_junction_graph(self, ignore_one_way = False):
        self.junctions = { tile: dict() for tile in self.paths if len(self.get_possible_moves(tile, ignore_one_way=True)) > 2 }
        self.junctions[self.start] = dict()
        self.junctions[self.finish] = dict()
        for junction in self.junctions:
            directions = self.get_possible_moves(junction, ignore_one_way=ignore_one_way)
            for direction in directions:
                tail = set([junction])
                queue = deque([(direction, junction)])
                while len(queue) > 0:
                    position, last_position = queue.popleft()
                    if position in self.junctions.keys():
                        self.junctions[junction][position] = (len(tail), tail)
                        break
                    for move in self.get_possible_moves(position, tail, ignore_one_way): queue.append((move, tail.add(position)))
    
    def get_junctions(self):
        return set(self.junctions.keys())
    
    def get_junction_graph(self):
        return self.junctions

    def get_start(self):
        return self.start
    
    def is_finished(self, pos: int):
        return pos == self.finish

    def get_possible_moves(self, pos: int, tail = set(), ignore_one_way = False):
        if ignore_one_way: return {pos - self.width, pos - 1, pos + 1, pos + self.width} & self.paths_incl_slopes - tail
        up = pos - self.width
        left = pos - 1
        right = pos + 1
        down = pos + self.width
        possible_moves = {up, left, right, down} & self.paths
        if up in self.slopes['^']: possible_moves.add(up)
        if left in self.slopes['<']: possible_moves.add(left)
        if right in self.slopes['>']: possible_moves.add(right)
        if down in self.slopes['v']: possible_moves.add(down)
        possible_moves -= tail
        return list(possible_moves)

    def get_colored_farm_map_string(self, positions: set):
        sorted_positions = sorted(list(positions), reverse=True)
        colored_farm_map_string = self.map_string
        for index in sorted_positions: colored_farm_map_string = colored_farm_map_string[:index] + '\033[91m' + colored_farm_map_string[index:index+1] + '\033[0m' + colored_farm_map_string[index+1:]
        return colored_farm_map_string


#
# Process input
#
with open('day 23/input.txt', 'r') as file:
    snow_island_map = Map(file.read())

#
# Puzzle 1, initial solution
#
# start_time = time.time()
# walk_queue = deque([ (snow_island_map.get_start(), set()) ])
# while len(walk_queue) > 0:
#     pos, tail = walk_queue.popleft()
#     tail.add(pos)
#     if snow_island_map.is_finished(pos): longest_tail = tail.copy()
#     moves = snow_island_map.get_possible_moves(pos, tail)
#     for move in moves: walk_queue.append((move, tail.copy() if len(moves) > 1 else tail))
# print(f'\n{snow_island_map.get_colored_farm_map_string(longest_tail)}\n')
# print(f'Puzzle 1 solution is: {len(longest_tail)-1} (in {time.time() - start_time:.3f} seconds)')

#
# Puzzle 1, junction version
#
snow_island_map.build_junction_graph()
junctions = snow_island_map.get_junctions()
junction_graph = snow_island_map.get_junction_graph()

start_time = time.time()
walk_queue = [ (snow_island_map.get_start(), [], 0) ]
while len(walk_queue) > 0:
    walk_queue.sort(key=lambda x: x[2])
    pos, tail, step_count = walk_queue.pop(0)
    tail.append(pos)
    if snow_island_map.is_finished(pos): longest_junction_tail = tail
    moves = set(junction_graph[pos].keys()) - set(tail)
    for move in moves: walk_queue.append((move, tail.copy() if len(moves) > 1 else tail, step_count + junction_graph[pos][move][0]))

longest_tail = set()
for i, junction in enumerate(longest_junction_tail[:-1]):
    longest_tail |= junction_graph[junction][longest_junction_tail[i+1]][1]

print(f'\n{snow_island_map.get_colored_farm_map_string(longest_tail)}\n')
print(f'Puzzle 1 solution is: {len(longest_tail)} (in {time.time() - start_time:.3f} seconds)')

#
# Puzzle 2
#
def assemble_longest_tail(longest_junction_tail: list):
    longest_tail = set()
    for i, junction in enumerate(longest_junction_tail[:-1]):
        longest_tail |= junction_graph[junction][longest_junction_tail[i+1]][1]
    return longest_tail

snow_island_map.build_junction_graph(ignore_one_way=True)
junctions = snow_island_map.get_junctions()
junction_graph = snow_island_map.get_junction_graph()

start_time = time.time()
walk_queue = deque([ (snow_island_map.get_start(), [], 0) ])
longest_step_count = 0
while len(walk_queue) > 0:
    pos, tail, step_count = walk_queue.popleft()
    tail.append(pos)
    if snow_island_map.is_finished(pos) and step_count > longest_step_count:
        longest_junction_tail = tail
        longest_step_count = step_count
        longest_tail = assemble_longest_tail(longest_junction_tail)
        print(f'\n{snow_island_map.get_colored_farm_map_string(longest_tail)}')
        print(f'Improved solution of {step_count} steps (queue length {len(walk_queue)}), continuing search... (after {time.time() - start_time:.3f} seconds)')
    moves = set(junction_graph[pos].keys()) - set(tail)
    for move in moves: walk_queue.append((move, tail.copy() if len(moves) > 1 else tail, step_count + junction_graph[pos][move][0]))

print(f'Search completed, Puzzle 2 solution is: {len(longest_tail)} (in {time.time() - start_time:.3f} seconds)')
