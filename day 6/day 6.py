import re, math

#
# Process input
#
with open('day 6/input.txt', 'r') as file:
    content = file.read()

regex = r'^Time:(.*)'
times = list(map(int, re.findall(regex, content, re.MULTILINE)[0].split()))

regex = r'^Distance:(.*)'
distances = list(map(int, re.findall(regex, content, re.MULTILINE)[0].split()))

#
# Puzzle 1
#
# def race(time, record):
#     ways_to_beat_record = 0
#     for press in range(1, time):
#         distance = (time - press) * press
#         if distance > record: ways_to_beat_record += 1
#     return ways_to_beat_record
def race(time, record):
    # Optimization for the quadratic equation
    first = (time - math.sqrt(time ** 2 - 4 * record)) / 2
    first = math.ceil(first) if first != int(first) else int(first) + 1
    last = (time + math.sqrt(time ** 2 - 4 * record)) / 2
    last = math.floor(last) if last != int(last) else int(last) - 1
    return last - first + 1

acc = 1
for i in range(len(times)):
    acc *= race(times[i], distances[i])

print("Puzzle 1 solution is:", acc)

#
# Puzzle 2
#
regex = r'^Time:(.*)'
time = int(re.findall(regex, content, re.MULTILINE)[0].replace(' ', ''))

regex = r'^Distance:(.*)'
distance = int(re.findall(regex, content, re.MULTILINE)[0].replace(' ', ''))

print("Puzzle 2 solution is:", race(time, distance))
