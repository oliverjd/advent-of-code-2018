# Advent of Code 2018 - Day 14
# Solution by Oliver Dunkley (https://dunkley.me)


def part_1(input):
    l = [3, 7]
    current = [0, 1]
    while len(l) < input + 10:
        s = l[current[0]] + l[current[1]]
        l += [int(x) for x in str(s)]
        current[0] = (current[0] + 1 + l[current[0]]) % len(l)
        current[1] = (current[1] + 1 + l[current[1]]) % len(l)
    return ''.join([str(x) for x in l[input:input+10]])


def part_2(input):
    i_digits = [int(x) for x in str(input)]
    l = [3, 7]
    current = [0, 1]
    while True:
        s = l[current[0]] + l[current[1]]
        d = [int(x) for x in str(s)]
        l += d
        current[0] = (current[0] + 1 + l[current[0]]) % len(l)
        current[1] = (current[1] + 1 + l[current[1]]) % len(l)
        if i_digits == l[-len(i_digits):]:
            return len(l) - len(i_digits)
        if i_digits == l[-len(i_digits)-1:-1]:
            return len(l) - len(i_digits) - 1


if __name__ == "__main__":
    with open("../input/day_14.txt") as f:
        print(part_1(int(f.readline())))
        f.seek(0)
        print(part_2(f.readline()))
