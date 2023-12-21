import time

#
# Classes
#
class FarmMap:
    def __init__(self, farm_map_string: str):
        self.width = farm_map_string.find('\n') + 1
        self.height = (len(farm_map_string) + 1) // self.width
        self.farm_map_string = farm_map_string

        self.plots = set()
        for i, tile in enumerate(farm_map_string):
            match tile:
                case '.': self.plots.add(i)
                case 'S':
                    self.plots.add(i)
                    self.start = i
    
    def get_start(self):
        return { self.start }
    
    def get_possible_moves(self, positions: set):
        next_positions = set()
        for pos in positions:
            next_positions |= {pos - self.width, pos - 1, pos + 1, pos + self.width} & self.plots
        return next_positions
    
    def get_colored_farm_map_string(self, positions: set):
        sorted_positions = sorted(list(positions), reverse=True)
        colored_farm_map_string = self.farm_map_string
        for index in sorted_positions: colored_farm_map_string = colored_farm_map_string[:index] + '\033[91m' + colored_farm_map_string[index:index+1] + '\033[0m' + colored_farm_map_string[index+1:]
        return colored_farm_map_string


#
# Process input
#
with open('day 21/input.txt', 'r') as file:
    original_farm_map = file.read() 

#
# Puzzle 1
#
farm_map = FarmMap(original_farm_map)
positions = farm_map.get_start()
for i in range(64): positions = farm_map.get_possible_moves(positions)
print(farm_map.get_colored_farm_map_string(positions))
print(f'Puzzle 1 solution is: {len(positions)}')

#
# Puzzle 2
#
tiled_farm_map = ''
for line in original_farm_map.splitlines():
    tiled_farm_map += line * 5 + '\n'
tiled_farm_map *= 5
farm_map = FarmMap(tiled_farm_map)
positions = { len(tiled_farm_map)// 2 - 1 }

n_across_diamond_count = dict()

# 65 steps to cover center tile
for i in range(65): positions = farm_map.get_possible_moves(positions)
n_across_diamond_count[1] = len(positions)

# 131 additional steps to reach 3x3 tiles
for i in range(131): positions = farm_map.get_possible_moves(positions)
n_across_diamond_count[3] = len(positions)

# 131 additional steps to reach 5x5 tiles
for i in range(131): positions = farm_map.get_possible_moves(positions)
n_across_diamond_count[5] = len(positions)

# Some peeking discovers recurring pattern
derivative = { 3: n_across_diamond_count[3] - n_across_diamond_count[1], 5: n_across_diamond_count[5] - n_across_diamond_count[3] }
derivative_2 = { 5: derivative[5] - derivative[3] }

# Extrapolate towards final step which is divisible by 131 less 65
final_step = 26501365
n_across = 1 + 2 * (final_step - 65) // 131
for i in range(7, n_across + 1, 2):
    derivative_2[i] = derivative_2[i-2]
    derivative[i] = derivative[i-2] + derivative_2[i]
    n_across_diamond_count[i] = n_across_diamond_count[i-2] + derivative[i]

# Calculate the final answer
print(f'Puzzle 2 solution is: {n_across_diamond_count[n_across]}')