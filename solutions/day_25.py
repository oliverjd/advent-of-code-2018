# Advent of Code 2018 - Day 25
# Solution by Oliver Dunkley (https://dunkley.me)

from scipy import spatial


def part_1(input):
    coords = []
    for line in input:
        coords.append([int(x) for x in line.strip().split(',')])

    tree = spatial.KDTree(coords)
    pairs = tree.query_pairs(3, p=1)

    single_points = set([i for i in range(len(coords))]).difference(
        set((x[0] for x in pairs)) | set((x[1] for x in pairs)))

    groups = []
    while len(pairs) > 0:
        this_pair = pairs.pop()
        this_group = [this_pair]
        this_elements = set((this_pair[0], this_pair[1]))
        while True:
            added = False
            for pair in pairs:
                if (pair[0] in this_elements or pair[1] in this_elements) and pair not in this_group:
                    added = True
                    new_pair = pair
                    this_group.append(new_pair)
                    this_elements.update(new_pair)
            if not added:
                break
        for pair in this_group:
            pairs.discard(pair)

        groups.append(this_group)

    return len(groups) + len(single_points)


def part_2(input):
    pass


if __name__ == "__main__":
    with open("../input/day_25.txt") as f:
        print(part_1(f))
