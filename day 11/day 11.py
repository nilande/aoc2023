import re

#
# Process input
#
with open('day 11/input.txt', 'r') as file:
    image = file.read()
width = image.find('\n') + 1
height = (len(image) + 1) // width

def get_empty_rows():
    empty_rows = []
    for row in range(height):
        if all(image[i] == '.' for i in range(row * width, (row+1) * width - 1)): empty_rows.append(row)
    return empty_rows

def get_emtpy_cols():
    empty_cols = []
    for col in range(width-1):
        if all(image[i] == '.' for i in range(col, len(image), width)): empty_cols.append(col)
    return empty_cols

empty_rows = get_empty_rows()
empty_cols = get_emtpy_cols()

def to_tile(pos):
    return (pos // width, pos % width)

def get_distance(tile1, tile2, scale):
    extra_rows = len([x for x in empty_rows if tile1[0] < x < tile2[0]])
    extra_cols = len([x for x in empty_cols if tile1[1] < x < tile2[1] or tile1[1] > x > tile2[1]])
    return tile2[0] - tile1[0] + abs(tile2[1] - tile1[1]) + (extra_rows + extra_cols) * scale

galaxies = list(map(lambda x: to_tile(x.start()), re.finditer(r'#', image)))

#
# Puzzle 1
#
acc = 0
for i in range(len(galaxies)-1):
    for j in range(i+1, len(galaxies)):
        acc += get_distance(galaxies[i], galaxies[j], 1)

print(f'Puzzle 1 solution is: {acc}')

#
# Puzzle 2
#
acc = 0
for i in range(len(galaxies)-1):
    for j in range(i+1, len(galaxies)):
        acc += get_distance(galaxies[i], galaxies[j], 1000000 - 1)

print(f'Puzzle 2 solution is: {acc}')