import re

#
# Process input
#
with open('day 2/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#
limits = {
    "red": 12,
    "green": 13,
    "blue": 14
}

regex = r'^Game (\d+): (.*)'
games = re.findall(regex, content, re.MULTILINE)

acc = 0

for gid, game in games:
    valid = True
    reveals = game.split('; ')
    for reveal in reveals:
        colors = reveal.split(', ')
        for color in colors:
            num, col = color.split(' ')
            if limits[col] < int(num): valid = False

    if valid: acc += int(gid)

print("Puzzle 1 solution is:", acc)

#
# Puzzle 2
#
acc = 0

for gid, game in games:
    fewest = {
        "red": 0,
        "green": 0,
        "blue": 0
    }


    reveals = game.split('; ')
    for reveal in reveals:
        colors = reveal.split(', ')
        for color in colors:
            num, col = color.split(' ')
            if fewest[col] < int(num): fewest[col] = int(num)
    
    acc += fewest['red'] * fewest['green'] * fewest['blue']

print("Puzzle 2 solution is:", acc)