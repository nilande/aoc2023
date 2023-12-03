import re

#
# Process input
#
with open('day 3/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#
regex = r'\d+'
matches = re.finditer(regex, content)

acc = 0
for match in matches:
    # Determine match position
    l, r = match.span()
    row = l // 141
    
    # Calculate bounding boxes
    lc = max(0, l % 141 - 1)
    rc = min(140, r % 141 + 1)
    tr = max(0, row - 1)
    br = min(139, row + 1)

    # Build a string covering the bounding box
    matchstring = ''
    for r in range(tr, br + 1):
        matchstring += content[r * 141 + lc:r * 141 + rc] + '\n'

    # Find all symbols within bounding box
    symRegex = r'[^.\d\n]'
    symbols = re.findall(symRegex, matchstring)
    
    if len(symbols) > 0: acc += int(match.group())

print("Puzzle 1 solution is:", acc)

#
# Puzzle 2
#
regex = r'\d+'
matches = re.finditer(regex, content)

starValues = {}
for match in matches:
    # Determine match position
    l, r = match.span()
    row = l // 141
    
    # Calculate bounding boxes
    lc = max(0, l % 141 - 1)
    rc = min(140, r % 141 + 1)
    tr = max(0, row - 1)
    br = min(139, row + 1)

    # Look for stars in the bounding box
    starRegex = re.compile('\\*')
    for r in range(tr, br + 1):
        stars = starRegex.finditer(content, r * 141 + lc, r * 141 + rc)
        for star in stars:
            starValues.setdefault(star.start(), []).append(match.group())

# These lines are only needed for enriching and pretty printing the content
# Uncomment if you want the output to display the gears in red text
#starKeys = sorted(starValues.keys(), reverse=True)
#for key in starKeys:
#    if len(starValues[key]) == 2:
#        content = content[:key] + '\033[91m' + content[key:key+1] + '\033[0m' + content[key+1:]
#
#for line in content.splitlines():
#    print(line)

acc = 0
for val in starValues.values():
    if len(val) == 2: acc += int(val[0]) * int(val[1])

print("Puzzle 2 solution is:", acc)