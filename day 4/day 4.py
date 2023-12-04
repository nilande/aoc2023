import re

#
# Process input
#
with open('day 4/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1 & 2
#
regex = r'^Card +(\d+): (.*)\|(.*)'
cards = re.findall(regex, content, re.MULTILINE)

points = 0
cardCount = [1] * len(cards)
for card, winning, drawn in cards:
    winning = set(map(int, winning.split()))
    drawn = set(map(int, drawn.split()))
    overlap = winning & drawn
    if len(overlap) > 0: points += 2 ** (len(overlap)-1)
    for i in range(len(overlap)):
        cardCount[int(card)+i] += cardCount[int(card)-1]


print("Puzzle 1 solution is:", points)
print("Puzzle 2 solution is:", sum(cardCount))