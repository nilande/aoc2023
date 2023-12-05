import re

#
# Process input
#
with open('day 5/input.txt', 'r') as file:
    content = file.read() + '\n\n'

regex = r'^seeds: (.*)'
seeds = list(map(int, re.findall(regex, content, re.MULTILINE)[0].split()))

# Read maps into two-dimensional list of tuples
regex = r'[^\n]+map:\n(.*?)\n\n'
mapsTexts = re.findall(regex, content, re.DOTALL)

maps = []
for mapText in mapsTexts:
    maps.append([])
    for mapLine in mapText.split('\n'):
        maps[len(maps)-1].append(tuple(map(int, mapLine.split())))

#
# Puzzle 1
#
locations = []
for seed in seeds:
    for m in maps:
        for destination, source, length in m:
            if seed >= source and seed < (source + length):
                seed = seed - source + destination
                break
    locations.append(seed)

print("Puzzle 1 solution is:", min(locations))

#
# Puzzle 2 - attempt 1 to flatten the list of maps
#

# Function that flattens several maps into one map
def flatten(m, maps):
    if len(maps) > 1:
        maps = [flatten(maps[0], maps[1:])]
    
    # Now that we have two arrays of maps, let's compound them
    result = []
    #for t1 in m:
        #for t2 in maps[0]:
            # Check for overlap between the transformations and add them together

    # Check for transformations in m or maps[0] without overlap

    return m

#
# Puzzle 2 - Brute force approach
#

STEP = 777
minlocation = 2 ** 32
minseedrange = ()
for i in range(len(seeds) // 2):
    seedStart = seeds[i*2]
    seedEnd = seedStart + seeds[i*2+1]

    for seed in range(seedStart, seedEnd, STEP):
        location = seed

        for m in maps:
            for destination, source, length in m:
                if location >= source and location < (source + length):
                    location = location - source + destination
                    break
        if minlocation > location:
            minseedrange = (seedStart, seed, seedEnd)
            minlocation = location
            #print("Coarse scan - lowest location so far found is:", minlocation, "with seed range:", minseedrange)

# Zoom in from coarse scan
for seed in range(max(minseedrange[0], minseedrange[1]-2*STEP), min(minseedrange[2], minseedrange[1]+2*STEP)):
    location = seed

    for m in maps:
        for destination, source, length in m:
            if location >= source and location < (source + length):
                location = location - source + destination
                break
    if minlocation > location:
        minseedrange = (seedStart, seed, seedEnd)
        minlocation = location
        #print("Fine scan - lowest location so far found is:", minlocation, "with seed range:", minseedrange)

print("Puzzle 2 solution is:", minlocation)
