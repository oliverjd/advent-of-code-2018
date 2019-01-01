# Advent of Code 2018 - Day 17
# Solution by Oliver Dunkley (https://dunkley.me)


def make_grid(coords):
    max_x = max([c['x'][1] for c in coords]) + 1
    max_y = max([c['y'][1] for c in coords])
    min_y = min([c['y'][0] for c in coords]) - 1
    min_x = min([c['x'][0] for c in coords]) - 1
    grid = [['.' for x in range(min_x, max_x + 1)] for y in range(min_y, max_y + 1)]
    grid[0][500 - min_x] = '+'
    for c in coords:
        for y in range(c['y'][0], c['y'][1] + 1):
            for x in range(c['x'][0], c['x'][1] + 1):
                grid[y - min_y][x - min_x] = '#'
    return grid


def spill_to_wall(grid, pipe_stack, x, y, fill, left=True):
    x_add = -1 if left else +1
    hit_end = False
    end_x = 0
    while not hit_end:
        if x < 0:
            fill = False
            break
        if grid[y][x + x_add] in ('.', '|'):
            if grid[y+1][x] in ('#', '~'):
                if grid[y][x + x_add] == '.':
                    if x > 0:
                        grid[y][x + x_add] = '|'
                        pipe_stack.append([x + x_add, y])
            if grid[y+1][x + x_add] in ('.', '|'):
                fill = False
                break
            else:
                if grid[y][x + x_add] == '.':
                    if x > 0:
                        grid[y][x + x_add] = '|'
                        pipe_stack.append([x + x_add, y])
        else:
            end_x = x
            hit_end = True
        x += x_add
    return fill, end_x


def iterate_grid(grid):
    pipe_stack = []
    for x in range(len(grid[0])):
        if grid[0][x] == '+':
            pipe_stack.append([x, 0])

    while len(pipe_stack) > 0:
        x, y = pipe_stack.pop()
        if (y > 0 and grid[y-1][x] == '|') and (y < len(grid)-1 and grid[y+1][x] == '|'):
            continue
        while True:
            if y >= len(grid) - 1:
                break
            if grid[y + 1][x] == '.':
                y += 1
                grid[y][x] = '|'
                pipe_stack.append([x, y])
            else:
                fill = True
                original_x = x
                fill, left_x = spill_to_wall(grid, pipe_stack, x, y, fill, left=True)
                x = original_x
                fill, right_x = spill_to_wall(grid, pipe_stack, x, y, fill, left=False)

                if fill:
                    for i in range(left_x, right_x + 1):
                        grid[y][i] = '~'
                break
    return grid


def count_wet(grid, static=False):
    wet = ('~', '|')
    if static:
        wet = '~'
    count = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x] in wet:
                count += 1
    return count


def part_1(input):
    coords = []
    for row in input:
        r = [x.strip().split('=') for x in row.strip().split(',')]
        new_coord = {}
        for coord in r:
            start_stop = [int(x) for x in coord[1].split('..')]
            if len(start_stop) == 1:
                new_coord[coord[0]] = [start_stop[0]]*2
            else:
                new_coord[coord[0]] = start_stop
        coords.append(new_coord)
    grid = make_grid(coords)
    new_grid = iterate_grid(grid)
    return count_wet(new_grid)


def part_2(input):
    coords = []
    for row in input:
        r = [x.strip().split('=') for x in row.strip().split(',')]
        new_coord = {}
        for coord in r:
            start_stop = [int(x) for x in coord[1].split('..')]
            if len(start_stop) == 1:
                new_coord[coord[0]] = [start_stop[0]]*2
            else:
                new_coord[coord[0]] = start_stop
        coords.append(new_coord)
    grid = make_grid(coords)
    new_grid = iterate_grid(grid)
    return count_wet(new_grid, static=True)


if __name__ == "__main__":
    with open("../input/day_17.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
