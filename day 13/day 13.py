def get_pattern_dimensions(pattern):
    height = len(pattern.splitlines())
    width = pattern.find('\n')
    return height, width

def find_reflection(indexes, length, ignore=-1):
    for i in range(length-1):
        if i+1 == ignore: continue
        j = i
        k = i+1
        while k in next((x for x in indexes if j in x), None):
            j -= 1
            k += 1
            if j < 0 or k > length-1:
                return i+1
    return 0

def get_reflection_value(pattern, ignore_row=-1, ignore_col=-1):
    rows =  {}
    cols = {}
    height, width = get_pattern_dimensions(pattern)
    i = 0
    for row in pattern.splitlines():
        rows.setdefault(row, []).append(i)
        i += 1

    for i in range(width):
        col = pattern[i:len(pattern):width+1]
        cols.setdefault(col, []).append(i)

    return find_reflection(rows.values(), height, ignore_row), find_reflection(cols.values(), width, ignore_col)

# Bruteforce
def get_smudged_reflection_value(pattern):
    row, col = get_reflection_value(pattern) # Baseline, should be ignored
    height, width = get_pattern_dimensions(pattern)

    for i in range(height):
        for j in range(width):
            pattern_copy = pattern
            match pattern_copy[i*(width+1)+j]:
                case '.': pattern_copy = pattern_copy[:i*(width+1)+j] + '#' + pattern_copy[i*(width+1)+j+1:]
                case '#': pattern_copy = pattern_copy[:i*(width+1)+j] + '.' + pattern_copy[i*(width+1)+j+1:]
            new_row, new_col = get_reflection_value(pattern_copy, row, col)
            if new_row != 0 or new_col != 0:
                return new_row, new_col
    print(pattern+"\n\n")
    return 0, 0


#
# Process input
#
with open('day 13/input.txt', 'r') as file:
    patterns = file.read().split('\n\n')

#
# Puzzle 1
#
acc = 0
for pattern in patterns:
    row, col = get_reflection_value(pattern)
    acc += row * 100 + col

print(f'Puzzle 1 solution is: {acc}')

#
# Puzzle 2
#
acc = 0
for pattern in patterns:
    row, col = get_smudged_reflection_value(pattern)
    acc += row * 100 + col

print(f'Puzzle 2 solution is: {acc}')