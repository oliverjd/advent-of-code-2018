# Advent of Code 2018 - Day 9
# Solution by Oliver Dunkley (https://dunkley.me)

import re
from collections import deque


def game(players, last_marble):
    scores = [0 for _ in range(players)]
    board = deque([0])
    for marble in range(1, last_marble + 1):
        if marble % 23 != 0:
            board.rotate(-1)
            board.append(marble)
        else:
            board.rotate(7)
            scores[marble % players] += marble + board.pop()
            board.rotate(-1)
    return max(scores)


def part_1(players, last_marble):
    return game(players, last_marble)


def part_2(players, last_marble):
    return game(players, last_marble * 100)


if __name__ == "__main__":
    with open("../input/day_09.txt") as f:
        players, last_marble = [int(x) for x in re.findall(r"([0-9]+)", f.readline())]
        print(part_1(players, last_marble))
        f.seek(0)
        print(part_2(players, last_marble))
