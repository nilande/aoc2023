#
# Classes
#
class SandBrick():
    def __init__(self, sand_brick_string):
        p1, p2 = sand_brick_string.split('~')
        self.x_min, self.y_min, self.z_min = map(int, p1.split(','))
        self.x_max, self.y_max, self.z_max = map(int, p2.split(','))
        self.children = {}
        self.parents = {}
        self.critical_ancestors = {}
        self.dependent_descendants = set()

    def overlaps_with(self, other: 'SandBrick'):
        if max(self.x_min, other.x_min) <= min(self.x_max, other.x_max) and \
            max(self.y_min, other.y_min) <= min(self.y_max, other.y_max): return True
        else: return False

    def update_parents(self):
        for parent in self.parents:
            parent.update_child(self, len(self.parents))

    def update_child(self, child: 'SandBrick', num_parents: int):
        self.children[child] = num_parents

    def is_possible_to_disintegrate(self):
        return False if any(num_parents == 1 for num_parents in self.children.values()) else True

    def identify_critical_parents(self):
        if len(self.parents) == 1:
            (parent, ) = self.parents
            parent.add_dependant_descendant(self)
            for child in self.children:
                child.notify_child_of_critical_ancestor(self, parent)

    def notify_child_of_critical_ancestor(self, parent: 'SandBrick', ancestor: 'SandBrick'):
        self.critical_ancestors[parent].add(ancestor)
        if all(ancestor in self.critical_ancestors[p] for p in self.parents):
            for child in self.children: child.notify_child_of_critical_ancestor(self, ancestor)
            ancestor.add_dependant_descendant(self)

    def add_dependant_descendant(self, descendant: 'SandBrick'):
        self.dependent_descendants.add(descendant)

    def count_dependant_descendants(self):
        return len(self.dependent_descendants)

    def move(self, delta_z):
        self.z_min += delta_z
        self.z_max += delta_z

    def pack(self, sand_bricks_below: list):
        possible_parents = set(x for x in sand_bricks_below if self.overlaps_with(x))
        rest_level = max(x.z_max for x in possible_parents) if len(possible_parents) > 0 else 0
        self.parents = set(x for x in possible_parents if x.z_max == rest_level)
        for p in self.parents: self.critical_ancestors[p] = set()
        self.move(rest_level + 1 - self.z_min)
        self.update_parents()



#
# Process input
#
with open('day 22/input.txt', 'r') as file:
    sand_bricks = list(map(lambda x: SandBrick(x), file.read().splitlines()))

sand_bricks.sort(key=lambda x: x.z_min)
for i, sand_brick in enumerate(sand_bricks):
    sand_brick.pack(sand_bricks[0:i])

#
# Puzzle 1
#
possible_to_disintegrate = sum(1 for s in sand_bricks if s.is_possible_to_disintegrate())
print(f'Puzzle 1 solution is: {possible_to_disintegrate}')

#
# Puzzle 2
#
for sand_brick in sand_bricks:
    sand_brick.identify_critical_parents()

dependent_descendants = 0
for sand_brick in sand_bricks:
    dependent_descendants += sand_brick.count_dependant_descendants()
print(f'Puzzle 2 solution is: {dependent_descendants}')