# Advent of Code 2018 - Day 23
# Solution by Oliver Dunkley (https://dunkley.me)

import re
import z3


def part_1(input):
    bots = []
    for line in input:
        x, y, z, r = (int(x) for x in re.match(r"pos=<([-0-9]+),([-0-9]+),([-0-9]+)>, r=([-0-9]+)", line.strip()).groups())
        bots.append((x, y, z, r))
    strongest = sorted(bots, key=lambda x: x[3], reverse=True)[0]
    in_range = [bot for bot in bots if abs(bot[0] - strongest[0]) + abs(bot[1] - strongest[1])
                + abs(bot[2] - strongest[2]) <= strongest[3]]
    return len(in_range)


def zabs(x):
    return z3.If(x >= 0, x, -x)


def part_2(input):
    bots = []
    for line in input:
        x, y, z, r = (int(x) for x in re.match(r"pos=<([-0-9]+),([-0-9]+),([-0-9]+)>, r=([-0-9]+)", line.strip()).groups())
        bots.append((x, y, z, r))

    (x, y, z) = (z3.Int('x'), z3.Int('y'), z3.Int('z'))
    in_ranges = [z3.Int('in_range_' + str(i)) for i in range(len(bots))]
    range_count = z3.Int('sum')
    o = z3.Optimize()
    for i in range(len(bots)):
        xi, yi, zi, ri = bots[i]
        o.add(in_ranges[i] == z3.If(zabs(x - xi) + zabs(y - yi) + zabs(z - zi) <= ri, 1, 0))
    o.add(range_count == sum(in_ranges))
    dist_from_zero = z3.Int('dist')
    o.add(dist_from_zero == zabs(x) + zabs(y) + zabs(z))
    h1 = o.maximize(range_count)
    h2 = o.minimize(dist_from_zero)
    o.check()

    return o.lower(h2)


if __name__ == "__main__":
    with open("../input/day_23.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
