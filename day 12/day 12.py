import re, time, functools

def process_record(row):
    cols = row.split()
    return (cols[0], list(map(int, cols[1].split(','))))

def get_validation_masks(broken_record):
    mask_not_op = 0
    mask_dmg = 0
    for spring in broken_record:
        mask_not_op <<= 1
        mask_dmg <<= 1
        match spring:
            case '#':
                mask_not_op |= 1
                mask_dmg |= 1
            case '?':
                mask_not_op |= 1
    return (mask_not_op, mask_dmg)

@functools.cache
def get_damaged_spring_arrangements(groups, length, mask_not_op, mask_dmg):
    min_shift = sum(groups) + len(groups) - 1
    result = 0
    for i in range(min_shift, length+1): 
        mask = 2**groups[0]-1 << i - groups[0]
        mask_dmg_temp = mask_dmg & (2**(length-i+groups[0]+1)-1 << i-groups[0]-1) if len(groups) > 1 else mask_dmg & 2**length-1
        if mask & mask_not_op == mask and mask_dmg_temp & mask == mask_dmg_temp:
            if len(groups) > 1: result += get_damaged_spring_arrangements(tuple(groups[1:]), i-groups[0]-1, mask_not_op, mask_dmg)
            else: result += 1
    return result

#
# Process input
#
with open('day 12/input.txt', 'r') as file:
    records = list(map(lambda x: process_record(x), file.read().splitlines()))

#
# Puzzle 1
#
arrangements = 0
start_time = time.time()
for broken_record, contiguous_groups in records:
    mask_not_op, mask_dmg = get_validation_masks(broken_record)
    arrangements += get_damaged_spring_arrangements(tuple(contiguous_groups), len(broken_record), mask_not_op, mask_dmg)

print(f'Puzzle 1 solution is: {arrangements} (in {time.time() - start_time:.3f} seconds)')

#
# Puzzle 2
#
arrangements = 0
start_time = time.time()
for broken_record, contiguous_groups in records:
    long_broken_record = '?'.join([ broken_record ] * 5)
    long_contiguous_groups = contiguous_groups * 5
    mask_not_op, mask_dmg = get_validation_masks(long_broken_record)
    arrangements += get_damaged_spring_arrangements(tuple(long_contiguous_groups), len(long_broken_record), mask_not_op, mask_dmg)

print(f'Puzzle 2 solution is: {arrangements} (in {time.time() - start_time:.3f} seconds)')
