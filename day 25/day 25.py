import time
from collections import deque

#
# Classes
#
class Component:
    def __init__(self, init_string: str):
        self.name, connections_string = init_string.split(': ')
        self.connections = { x: None for x in connections_string.split(' ') } if len(connections_string) > 0 else {}

    def __repr__(self):
        return self.name

    def get_name(self):
        return self.name
    
    def add_connections(self, components: list):
        for connection in self.connections:
            self.connections[connection] = components[connection]
            components[connection].add_connection(self) # Add reverse connection

    def add_connection(self, other: 'Component'):
        self.connections[other.get_name()] = other

    def get_connections(self):
        return self.connections
    
    def remove_connection(self, other: 'Component'):
        print(f'Removing connection between {self} and {other}')
        del self.connections[other.get_name()]
        del other.connections[self.get_name()]

    def get_all_paths(self):
        queue = deque([ (self, []) ])
        explored = set()
        paths = []

        while len(queue) > 0:
            current, path = queue.popleft()
            if current in explored: continue
            path.append(current)
            explored.add(current)
            if len(path) > 1: paths.append(path)
            connections = current.get_connections().values()
            for connection in connections:
                queue.append((connection, path.copy()))
        return paths

#
# Process input
#
with open('day 25/input.txt') as file:
    components = { c.get_name(): c for c in map(lambda x: Component(x), file.read().splitlines()) }

# Add component connections and missing components
for component in list(components.values()):
    for connection in component.get_connections():
        if not connection in components.keys(): components[connection] = Component(f'{connection}: ')
    component.add_connections(components)

#
# Puzzle 1
#
start_time = time.time()
pair_count = {}
for c in components.values():
    paths = c.get_all_paths()
    for path in paths:
        for i in range(len(path)-1):
            p1 = path[i].get_name()
            p2 = path[i+1].get_name()
            if p1 < p2: pair_name = f'{p1}-{p2}'
            else: pair_name = f'{p2}-{p1}'
            pair_count.setdefault(pair_name, 0)
            pair_count[pair_name] += 1

# Identify 3 most used edges in graph and remove them
pair_count = [(tuple(k.split('-')), v) for k, v in sorted(pair_count.items(), key=lambda x: x[1], reverse=True)]
for pair, count in pair_count[:3]:
    p1_name, p2_name = pair
    p1 = components[p1_name]
    p2 = components[p2_name]
    p1.remove_connection(p2)

# Calculate the number of components in each group
num_paths1 = len(next(iter(components.values())).get_all_paths()) + 1
num_paths2 = len(components) - num_paths1
print(f'Puzzle 1 solution is: {num_paths1 * num_paths2}')