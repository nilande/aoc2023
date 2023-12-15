import time, functools

def get_pattern_dimensions(pattern):
    height = len(pattern.splitlines())
    width = pattern.find('\n')
    return height, width

def get_pattern_columns(pattern):
    width, height = get_pattern_dimensions(pattern)
    columns = []
    for i in range(width):
        columns.append(pattern[i:len(pattern):width+1])
    return columns

def get_pattern_from_columns(columns):
    pattern = ''
    for i in range(len(columns[0])):
        for j in range(len(columns)):
            pattern += columns[j][i]
        pattern += '\n'
    return pattern[:-1]

def get_pattern_rows(pattern):
    return pattern.splitlines()

def get_pattern_from_rows(rows):
    return '\n'.join(rows)

def get_shifted_vectors(vectors, left = True):
    shifted_vectors = []
    for vector in vectors:
        new_vector = '#'.join([''.join(sorted(group, reverse=left)) for group in vector.split('#')])
        shifted_vectors.append(new_vector)
    return shifted_vectors

def get_vectors_load(vectors):
    acc = 0
    for vector in vectors:
        for i in range(1, len(vector)+1):
            if vector[len(vector)-i] == 'O': acc += i 
    return acc

# Bruteforce through caching
@functools.cache
def get_cycled_pattern(pattern):
    # North
    vectors = get_pattern_columns(pattern)
    vectors = get_shifted_vectors(vectors, True)
    pattern = get_pattern_from_columns(vectors)

    # West
    vectors = get_pattern_rows(pattern)
    vectors = get_shifted_vectors(vectors, True)
    pattern = get_pattern_from_rows(vectors)

    # South
    vectors = get_pattern_columns(pattern)
    vectors = get_shifted_vectors(vectors, False)
    pattern = get_pattern_from_columns(vectors)

    # East
    vectors = get_pattern_rows(pattern)
    vectors = get_shifted_vectors(vectors, False)
    pattern = get_pattern_from_rows(vectors)

    return pattern

#
# Process input
#
with open('day 14/input.txt', 'r') as file:
    pattern = file.read()
    
#
# Puzzle 1
#
columns = get_pattern_columns(pattern)
shifted_columns = get_shifted_vectors(columns, True)
print(f'Puzzle 1 solution is: {get_vectors_load(shifted_columns)}')

#
# Puzzle 2
#
start_time = time.time()
for i in range(1000000000):
    pattern = get_cycled_pattern(pattern)
    
columns = get_pattern_columns(pattern)
print(f'Puzzle 2 solution is: {get_vectors_load(columns)} (in {time.time() - start_time:.3f} seconds)')