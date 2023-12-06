import re

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
def race(time, record):
    ways_to_beat_record = 0
    for press in range(1, time):
        distance = (time - press) * press
        if distance > record: ways_to_beat_record += 1
    return ways_to_beat_record

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
