#
# Process input
#
with open('day 18/input.txt', 'r') as file:
    dig_plan = file.read().splitlines()

#
# Puzzle 1
#
pos = (0,0)
area = 0
circumference = 0
for dig_plan_line in dig_plan:
    direction, distance, color = tuple(dig_plan_line.split())
    distance = int(distance)
    match direction:
        case 'R': pos = (pos[0] + distance, pos[1])
        case 'L': pos = (pos[0] - distance, pos[1])
        case 'D':
            pos = (pos[0], pos[1] + distance)
            area += pos[0] * distance
        case 'U':
            pos = (pos[0], pos[1] - distance)
            area -= pos[0] * distance
    circumference += distance

area = abs(area) + circumference//2 + 1

print(f'Puzzle 1 solution is: {area}')

#
# Puzzle 2
#
pos = (0,0)
area = 0
circumference = 0
for dig_plan_line in dig_plan:
    color = dig_plan_line.split()[2]
    direction = color[-2]
    distance = int(color[2:-2], 16)
    match direction:
        case '0': pos = (pos[0] + distance, pos[1])
        case '2': pos = (pos[0] - distance, pos[1])
        case '1':
            pos = (pos[0], pos[1] + distance)
            area += pos[0] * distance
        case '3':
            pos = (pos[0], pos[1] - distance)
            area -= pos[0] * distance
    circumference += distance

area = abs(area) + circumference//2 + 1

print(f'Puzzle 2 solution is: {area}')