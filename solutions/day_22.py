# Advent of Code 2018 - Day 22
# Solution by Oliver Dunkley (https://dunkley.me)

import networkx


def get_el(depth, target, limit):
    el = [[0 for x in range(limit[0] + 1)] for y in range(limit[1] + 1)]
    for y in range(limit[1] + 1):
        for x in range(limit[0] + 1):
            if y == 0 and x == 0:
               el[y][x] = (0 + depth) % 20183
            elif y == 0:
                el[y][x] = ((x * 16807) + depth) % 20183
            elif x == 0:
                el[y][x] = ((y * 48271) + depth) % 20183
            elif x == target[0] and y == target[1]:
                el[y][x] = (0 + depth) % 20183
            else:
                el[y][x] = (el[y][x-1] * el[y-1][x] + depth) % 20183
    return el


def part_1(input):
    inp = list(input)
    depth = int(inp[0].split(' ')[1])
    target = (int(inp[1].split(' ')[1].split(',')[0]), int(inp[1].split(' ')[1].split(',')[1]))
    el = get_el(depth, target, target)
    return sum([sum([el[y][x] % 3 for x in range(target[0] + 1)]) for y in range(target[1] + 1)])


def part_2(input):
    inp = list(input)
    depth = int(inp[0].split(' ')[1])
    target = (int(inp[1].split(' ')[1].split(',')[0]), int(inp[1].split(' ')[1].split(',')[1]))
    limit = (target[0] + 100, target[1] + 100)
    el = get_el(depth, target, limit)
    type_to_item = {0: ('T', 'C'), 1: ('C', 'N'), 2: ('T', 'N')}
    graph = networkx.Graph()
    for y in range(limit[1] + 1):
        for x in range(limit[0] + 1):
            items = type_to_item[el[y][x] % 3]
            graph.add_edge((x, y, items[0]), (x, y, items[1]), weight=7)
            for i, j in ((0, 1), (1, 0), (0, -1), (-1, 0)):
                if 0 <= x + i <= limit[0] and 0 <= y + j <= limit[1]:
                    items_2 = type_to_item[el[y + j][x + i] % 3]
                    items_both = [it for it in items if it in items_2]
                    for it in items_both:
                        graph.add_edge((x, y, it), (x + i, y + j, it))
    return networkx.dijkstra_path_length(graph, (0, 0, 'T'), (target[0], target[1], 'T'))


if __name__ == "__main__":
    with open("../input/day_22.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
