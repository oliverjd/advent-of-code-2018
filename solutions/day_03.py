# Advent of Code 2018 - Day 3
# Solution by Oliver Dunkley (https://dunkley.me)

import re


def make_grid(input):
    ids = [[[] for i in range(1000)] for j in range(1000)]
    id_vals = set()
    for line in input:
        id, x, y, w, h = (int(x) for x in re.match('\#([0-9]+).\@.([0-9]+).([0-9]+)..([0-9]+)x([0-9]+)', line).groups())
        for a in range(x, x + w):
            for b in range(y, y + h):
                ids[a][b].append(id)
                id_vals.add(id)
    return ids, id_vals


def part_1(ids):
    return sum([len(ids[x][y]) >= 2 for x in range(1000) for y in range(1000)])


def part_2(ids, id_vals):
    for x in range(1000):
        for y in range(1000):
            if len(ids[x][y]) > 1:
                for id in ids[x][y]:
                    id_vals.discard(id)
    return list(id_vals)[0]


if __name__ == "__main__":
    with open("../input/day_03.txt") as f:
        ids, id_vals = make_grid(f)
        print(part_1(ids))
        print(part_2(ids, id_vals))
