import re, math, functools

#
# Process input
#
with open('day 8/input.txt', 'r') as file:
    content = file.read()

instructions = list(content.splitlines()[0])
regex = r'^(...) = \((...), (...)\)'
matches = re.findall(regex, content, re.MULTILINE)

node_map = {}
for node, left, right in matches:
    node_map[node] = (left, right)

# # Optimization to create a flat map based on the instructions
flat_node_map = {}
flat_step_size = len(instructions)
for key in node_map.keys():
    node = key
    for instruction in instructions:
        match instruction:
            case 'L':
                node = node_map[node][0]
            case 'R':
                node = node_map[node][1]
    flat_node_map[key] = node

#
# Puzzle 1
#
node = 'AAA'
steps = 0
while node != 'ZZZ':
    node = flat_node_map[node]
    steps += flat_step_size

print(f'Puzzle 1 solution is: {steps}')

#
# Puzzle 2
#
nodes = [key for key in node_map.keys() if key.endswith('A')]
node_steps = []
for node in nodes:
    steps = 0
    while not node.endswith('Z'):
        node = flat_node_map[node]
        steps += 1
    node_steps.append(steps)

print(f'Puzzle 2 solution is: {functools.reduce(math.lcm, node_steps) * len(instructions)}')
