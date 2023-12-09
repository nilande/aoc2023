import functools

#
# Process input
#
with open('day 9/input.txt', 'r') as file:
    lines = file.read().splitlines()

histories = []
for line in lines: histories.append(list(map(int, line.split())))

#
# Puzzle 1
#
def predict(history):
    if all(h == 0 for h in history): return 0
    derivation = [history[i+1] - history[i] for i in range(len(history)-1)]
    return(predict(derivation)+history[-1])

predictions = map(predict, histories)

print(f'Puzzle 1 solution is: {functools.reduce(lambda a, b: a + b, predictions)}')

#
# Puzzle 2
#
# Reverse the lists to predict backwards :-)
back_predictions = map(predict, [h[::-1] for h in histories])

print(f'Puzzle 2 solution is: {functools.reduce(lambda a, b: a + b, back_predictions)}')