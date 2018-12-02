# Advent of Code 2018 - Day 2
# Solution by Oliver Dunkley (https://dunkley.me)


def part_1(input):
    count_2 = 0
    count_3 = 0
    for x in input:
        chars = {}
        for c in x:
            if c in chars:
                chars[c] += 1
            else:
                chars[c] = 1
        count_2 += int(any([chars[i] == 2 for i in chars]))
        count_3 += int(any([chars[i] == 3 for i in chars]))
    return count_2 * count_3


def part_2(input):
    seen = set()
    for x in input:
        seen_this_word = set()
        for i in range(len(x)):
            seen_this_word.add(x[0:i] + x[i+1:])
        if list(seen.intersection(seen_this_word)):
            return list(seen.intersection(seen_this_word))[0]
        seen.update(seen_this_word)


if __name__ == "__main__":
    with open("../input/day_02.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
