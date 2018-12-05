# Advent of Code 2018 - Day 5
# Solution by Oliver Dunkley (https://dunkley.me)

import string


def pair_unit(char):
    return char.lower() if char.isupper() else char.upper()


def react_polymer(polymer):
    stack = []
    for char in polymer:
        if len(stack) > 0 and stack[-1] == pair_unit(char):
            stack.pop()
        else:
            stack.append(char)
    return stack


def part_1(polymer):
    return len(polymer)


def part_2(polymer):
    alphabet = string.ascii_lowercase[:26]
    lens = []
    for letter in alphabet:
        new_polymer = list(filter(lambda x: x not in (letter, letter.upper()), polymer))
        lens.append(len(react_polymer(new_polymer)))
    return min(lens)


if __name__ == "__main__":
    with open("../input/day_05.txt") as f:
        reacted_polymer = react_polymer(f.readline().strip())
        print(part_1(reacted_polymer))
        print(part_2(reacted_polymer))
