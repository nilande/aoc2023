import re

#
# Process input
#
with open('day 7/input.txt', 'r') as file:
    hand_lines = file.read().splitlines()

#
# Puzzle 1
#

def get_hand_type(hand):
    cards = {}
    for card in list(hand):
        cards.setdefault(card, 0)
        cards[card] += 1
    counts = sorted(cards.values(), reverse=True)
    if counts[0] == 5: return 7
    elif counts[0] == 4: return 6
    elif counts[0] == 3:
        if counts[1] == 2: return 5
        else: return 4
    elif counts[0] == 2:
        if counts[1] == 2: return 3
        else: return 2
    else:
        return 1

def get_sort_value(hand):
    sort_value = re.sub(r'(\d)', r'0\1', hand)
    sort_value = sort_value.replace('T', '10')
    sort_value = sort_value.replace('J', '11')
    sort_value = sort_value.replace('Q', '12')
    sort_value = sort_value.replace('K', '13')
    sort_value = sort_value.replace('A', '14')
    return sort_value    

hands = []
for hand_line in hand_lines:
    hand, bid = hand_line.split()
    type = get_hand_type(hand)
    sort_value = get_sort_value(hand)
    hands.append([hand, int(bid), type, sort_value])

hands.sort(key = lambda x: str(x[2])+x[3])

i = 1
acc = 0
for hand in hands:
    acc += hand[1] * i
    i += 1

print("Puzzle 1 solution is:", acc)

#
# Puzzle 2
#
def get_joker_hand_type(hand):
    cards = {}
    for card in list(hand):
        cards.setdefault(card, 0)
        cards[card] += 1
    cards.setdefault('J', 0)
    jokers = cards['J']
    del cards['J']
    counts = sorted(cards.values(), reverse=True)
    if len(counts) == 0: counts = [0]
    counts[0] += jokers
    if counts[0] == 5: return 7
    elif counts[0] == 4: return 6
    elif counts[0] == 3:
        if counts[1] == 2: return 5
        else: return 4
    elif counts[0] == 2:
        if counts[1] == 2: return 3
        else: return 2
    else:
        return 1

def get_joker_sort_value(hand):
    sort_value = re.sub(r'(\d)', r'0\1', hand)
    sort_value = sort_value.replace('T', '10')
    sort_value = sort_value.replace('J', '01')
    sort_value = sort_value.replace('Q', '12')
    sort_value = sort_value.replace('K', '13')
    sort_value = sort_value.replace('A', '14')
    return sort_value    

hands = []
for hand_line in hand_lines:
    hand, bid = hand_line.split()
    type = get_joker_hand_type(hand)
    sort_value = get_joker_sort_value(hand)
    hands.append([hand, int(bid), type, sort_value])

hands.sort(key = lambda x: str(x[2])+x[3])

i = 1
acc = 0
for hand in hands:
    acc += hand[1] * i
    i += 1

print("Puzzle 2 solution is:", acc)
