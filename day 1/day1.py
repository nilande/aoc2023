import re

#
# Process input
#
with open('day 1/input.txt', 'r') as file:
    content = file.read()

#
# Puzzle 1
#
acc = 0

for line in content.splitlines():
    digits = list(filter(str.isdigit, line))
    acc += int(digits[0])*10 + int(digits[-1])

print("Puzzle 1 solution is", acc)

#
# Puzzle 2
#
substitutions = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}

# Find the first digits using regex
regex = r'^.*?(' + '|'.join(substitutions.keys()) + r'|\d)'
first_digits = ''.join(re.findall(regex, content, re.MULTILINE))

# Find the last digits using greedier regex :-)
regex = r'^.*(' + '|'.join(substitutions.keys()) + r'|\d)'
last_digits = ''.join(re.findall(regex, content, re.MULTILINE))

# Finally, substitute the written out numbers with digit counterparts
for key, value in substitutions.items():
    first_digits = first_digits.replace(key, value)
    last_digits = last_digits.replace(key, value)

acc = 0
for char in first_digits:
    acc += int(char) * 10

for char in last_digits:
    acc += int(char)

print("Puzzle 2 solution is", acc)
