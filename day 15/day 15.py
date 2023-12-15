def get_hash(string):
    hash = 0
    for char in string:
        hash = (hash + ord(char)) * 17 % 256
    return hash

def insert_lens(box, label, focal_length):
    lens_id = next((lens_id for lens_id, lens in enumerate(box) if lens[0] == label), None)
    if lens_id is not None: box[lens_id] = tuple([label, focal_length])
    else: box.append(tuple([label, focal_length]))

def remove_lens(box, label):
    lens_id = next((lens_id for lens_id, lens in enumerate(box) if lens[0] == label), None)
    if lens_id is not None: box.pop(lens_id)

def parse_step(step, boxes):
    if step[-1] == '-':
        label = step[:-1]
        box_no = get_hash(label)
        remove_lens(boxes[box_no], label)
    else:
        label = step[:step.find('=')]
        focal_length = int(step[len(label)+1:])
        box_no = get_hash(label)
        insert_lens(boxes[box_no], label, focal_length)

#
# Process input
#
with open('day 15/input.txt', 'r') as file:
    sequence = file.readline().strip()

#
# Puzzle 1
#
acc = 0
for step in sequence.split(','):
    acc += get_hash(step)

print(f'Puzzle 1 solution is: {acc}')

#
# Puzzle 2
#
boxes = [[] for x in range(256)]
for step in sequence.split(','):
    parse_step(step, boxes)

acc = 0
for box_no in range(256):
    for lens_no in range(len(boxes[box_no])):
        acc += (box_no + 1) * (lens_no + 1) * boxes[box_no][lens_no][1]

print(f'Puzzle 2 solution is: {acc}')