# Advent of Code 2018 - Day 18
# Solution by Oliver Dunkley (https://dunkley.me)


def iterate(grid):
    new_grid = [''] * len(grid)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            adjacent = []
            if y > 0:
                adjacent += grid[y-1][x]
            if x > 0:
                adjacent += grid[y][x-1]
            if y < len(grid) - 1:
                adjacent += grid[y+1][x]
            if x < len(grid) - 1:
                adjacent += grid[y][x+1]
            if y > 0 and x > 0:
                adjacent += grid[y-1][x-1]
            if y < len(grid) - 1 and x < len(grid) - 1:
                adjacent += grid[y+1][x+1]
            if y < len(grid) - 1 and x > 0:
                adjacent += grid[y+1][x-1]
            if x < len(grid) - 1 and y > 0:
                adjacent += grid[y-1][x+1]
            if grid[y][x] == '.' and sum([1 for x in adjacent if x == '|']) >= 3:
                    new_grid[y] += '|'
            elif grid[y][x] == '|' and sum([1 for x in adjacent if x == '#']) >= 3:
                    new_grid[y] += '#'
            elif grid[y][x] == '#' and (sum([1 for x in adjacent if x == '#']) < 1 or sum([1 for x in adjacent if x == '|']) < 1):
                new_grid[y] += '.'
            else:
                new_grid[y] += grid[y][x]
    return new_grid


def part_1(input):
    grid = list(input)
    for i in range(10):
        grid = iterate(grid)
    wood_sum = 0
    lumberyard_sum = 0
    for row in grid:
        wood_sum += sum([1 for x in row if x == '|'])
        lumberyard_sum += sum([1 for x in row if x == '#'])
    return wood_sum * lumberyard_sum


def part_2(input):
    grid = list(input)
    num = 1000
    seen = dict()
    seen_at = dict()
    for i in range(1, num + 1):
        grid = iterate(grid)
        wood_sum = 0
        lumberyard_sum = 0
        for row in grid:
            wood_sum += sum([1 for x in row if x == '|'])
            lumberyard_sum += sum([1 for x in row if x == '#'])
        ans = wood_sum * lumberyard_sum
        if ans in seen:
            print("seen", ans, "at", i, "and before at", seen[ans], 'diff =', i - seen[ans])
        seen[ans] = i
        seen_at[i] = ans
    # the first repeat in the final pattern is from i=569 to i=597 - that gives us the value at 100000... as follows:
    return seen_at[569 + ((1000000000-569) % 28)]


if __name__ == "__main__":
    with open("../input/day_18.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
