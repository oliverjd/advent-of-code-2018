# Advent of Code 2018 - Day 11
# Solution by Oliver Dunkley (https://dunkley.me)


def power_level(x, y, serial):
    rack_id = x + 10
    power = (rack_id * y + serial) * rack_id
    hundreds = int(repr(power)[-3]) if power >= 100 else 0
    return hundreds - 5


def max_of_size(size, grid):
    strip_sums = [[0 for i in range(300)] for j in range(300)]
    for j in range(300):
        s = 0
        for i in range(size):
            s += grid[i][j]
        strip_sums[0][j] = s
        for i in range(1,300-size+1):
            s += grid[i+size-1][j] - grid[i-1][j]
            strip_sums[i][j] = s

    max_s = float('-inf')
    max_x, max_y = 0, 0

    for i in range(300-size+1):
        s = 0
        for j in range(size):
            s += strip_sums[i][j]
        if s > max_s:
            max_s = s
            max_x, max_y = i, 0
        for j in range(1,300-size+1):
            s += strip_sums[i][j+size-1] - strip_sums[i][j-1]
            if s > max_s:
                max_s = s
                max_x, max_y = i, j

    return max_x, max_y, max_s


def part_1(input):
    serial = int(input.readline())
    grid = ([[power_level(x,  y, serial) for y in range(300)] for x in range(300)])
    x, y, s = max_of_size(3, grid)
    return str(x) + ',' + str(y)


def part_2(input):
    serial = int(input.readline())
    grid = ([[power_level(x,  y, serial) for y in range(300)] for x in range(300)])
    max_s = float('-inf')
    max_size, max_x, max_y = 0, 0, 0
    for size in range(1, 301):
        x, y, s = max_of_size(size, grid)
        if s > max_s:
            max_s = s
            max_x, max_y = x, y
            max_size = size
    return str(max_x) + ',' + str(max_y) + ',' + str(max_size)


if __name__ == "__main__":
    with open("../input/day_11.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
