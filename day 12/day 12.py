import re, time

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

min_transitions_cache = []
max_transitions_cache = []
def build_transitions_cache_table(mask_not_op, mask_dmg, length):
    min_transitions_cache.clear()
    max_transitions_cache.clear()

    min_transitions = 0
    prev_value = 0
    mask_not_op_copy = mask_not_op
    mask_dmg_copy = mask_dmg
    i = 0
    while mask_not_op_copy != 0:
        if mask_dmg_copy & 1 == 1 and prev_value == 0:
            prev_value = 1
            min_transitions += 1
        elif mask_not_op_copy & 1 == 0 and prev_value == 1:
            prev_value = 0
            min_transitions += 1
        min_transitions_cache.append(min_transitions//2)
        mask_not_op_copy >>= 1
        mask_dmg_copy >>= 1
    while len(min_transitions_cache) < length: min_transitions_cache.append(min_transitions//2)

    max_transitions = 0
    prev_value = 0
    mask_not_op_copy = mask_not_op
    mask_dmg_copy = mask_dmg
    i = 0
    while mask_not_op_copy != 0:
        if mask_not_op_copy & 1 == 1 and prev_value == 0:
            prev_value = 1
            max_transitions += 1
        elif mask_dmg_copy & 1 == 0 and prev_value == 1:
            prev_value = 0
            max_transitions += 1
        max_transitions_cache.append((max_transitions+1)//2)
        mask_not_op_copy >>= 1
        mask_dmg_copy >>= 1
    while len(max_transitions_cache) < length: max_transitions_cache.append((max_transitions+1)//2)

def is_remaining_groups_possible(groups, length):
    min_transitions = min_transitions_cache[length-1]
    max_transitions = max_transitions_cache[length-1]
    if min_transitions <= len(groups) <= max_transitions: return True
    else: return False

def get_damaged_spring_arrangements(groups, length, mask, mask_not_op, mask_dmg):
    #if not is_remaining_groups_possible(groups, length): return 0

    min_shift = sum(groups) + len(groups) - 1
    result = 0
    for i in range(min_shift, length+1): 
        new_mask = mask | 2**groups[0]-1 << i - groups[0]
        new_mask_temp = new_mask | 2**(i-groups[0]-1)-1 if len(groups) > 1 else new_mask
        if new_mask & mask_not_op == new_mask and mask_dmg & new_mask_temp == mask_dmg:
            if len(groups) > 1:
                result += get_damaged_spring_arrangements(groups[1:], i-groups[0]-1, new_mask, mask_not_op, mask_dmg)
            else:
                result += 1
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
    build_transitions_cache_table(mask_not_op, mask_dmg, len(broken_record))
    arrangements += get_damaged_spring_arrangements(contiguous_groups, len(broken_record), 0, mask_not_op, mask_dmg)

print(f'Puzzle 1 solution is: {arrangements} (in {time.time() - start_time:.3f} seconds)')

#
# Puzzle 2
#
arrangements = 0
start_time = time.time()
for broken_record, contiguous_groups in records:
    long_broken_record = '?'.join([ broken_record ] * 3)
    long_contiguous_groups = contiguous_groups * 3
    mask_not_op, mask_dmg = get_validation_masks(long_broken_record)
    build_transitions_cache_table(mask_not_op, mask_dmg, len(long_broken_record))
    arrangements += get_damaged_spring_arrangements(long_contiguous_groups, len(long_broken_record), 0, mask_not_op, mask_dmg)

print(f'Puzzle 2 solution is: {arrangements} (in {time.time() - start_time:.3f} seconds)')
