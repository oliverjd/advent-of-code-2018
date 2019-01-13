# Advent of Code 2018 - Day 20
# Solution by Oliver Dunkley (https://dunkley.me)

import networkx


def make_door(a, b, doors):
    if a in doors:
        doors[a].append(b)
    else:
        doors[a] = [b]
    if b in doors:
        doors[b].append(a)
    else:
        doors[b] = [a]
    return b[0], b[1]


def traverse(chars, i, s, doors):
    s_ori = (s[0], s[1])
    while True:
        if chars[i] == 'N':
            s = make_door(s, (s[0], s[1] - 1), doors)
        elif chars[i] == 'E':
            s = make_door(s, (s[0] + 1, s[1]), doors)
        elif chars[i] == 'W':
            s = make_door(s, (s[0] - 1, s[1]), doors)
        elif chars[i] == 'S':
            s = make_door(s, (s[0], s[1] + 1), doors)
        elif chars[i] == '(':
            i = traverse(chars, i+1, s, doors)
        elif chars[i] == '|':
            s = s_ori
        elif chars[i] == ')':
            return i
        elif chars[i] == '$':
            return doors
        i += 1


def part_1(input):
    doors = traverse(input.readline().strip()[1:], 0, (0, 0), {})
    lengths = networkx.algorithms.shortest_path_length(networkx.Graph(doors), (0, 0))
    return max(lengths.values())


def part_2(input):
    doors = traverse(input.readline().strip()[1:], 0, (0, 0), {})
    lengths = networkx.algorithms.shortest_path_length(networkx.Graph(doors), (0, 0))
    return len([x for x in lengths.values() if x >= 1000])


if __name__ == "__main__":
    with open("../input/day_20.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
