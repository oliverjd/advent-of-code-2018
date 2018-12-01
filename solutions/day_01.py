# Advent of Code 2018 - Day 1
# Solution by Oliver Dunkley (https://dunkley.me)


def part_1(input):
    return sum([int(x) for x in input])


def part_2(input):
    freq = 0
    seen = {freq}
    deltas = list(input)
    while True:
        for x in deltas:
            freq += int(x)
            if freq in seen:
                return freq
            seen.add(freq)


if __name__ == "__main__":
    with open("../input/day_01.txt") as f:
        print(part_1(f))
    with open("../input/day_01.txt") as f:
        print(part_2(f))
