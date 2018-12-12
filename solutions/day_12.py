# Advent of Code 2018 - Day 12
# Solution by Oliver Dunkley (https://dunkley.me)

import re


def part_1(input):
    initial_state = re.match(".+: (.+)", input.readline()).groups()[0]
    next(input)
    rules = {}
    for line in input:
        rule, _, to = line.strip().split(' ')
        rules[rule] = to
    iters = 20
    state = '.' * iters + initial_state + '.' * iters
    for i in range(iters):
        new_state = ''
        for j in range(len(state)-4):
            new_state += rules[state[j:j+5]]
        state = '.' * 2 + new_state + '.' * 2
    return sum([i - iters for i in range(len(state)) if state[i] == '#'])


def part_2(input):
    """ I like this question. Simple pattern spotting enables you to deduce the answer for an impractically large
    number of iterations. """
    initial_state = re.match(".+: (.+)", input.readline()).groups()[0]
    next(input)
    rules = {}
    for line in input:
        rule, _, to = line.strip().split(' ')
        rules[rule] = to
    iters = 150
    state = '.' * iters + initial_state + '.' * iters
    for i in range(iters):
        new_state = ''
        for j in range(len(state)-4):
            new_state += rules[state[j:j+5]]
        state = '.' * 2 + new_state + '.' * 2
    s = sum([i - iters for i in range(len(state)) if state[i] == '#'])
    return s + (50000000000 - iters) * sum([1 for i in range(len(state)) if state[i] == '#'])


if __name__ == "__main__":
    with open("../input/day_12.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
