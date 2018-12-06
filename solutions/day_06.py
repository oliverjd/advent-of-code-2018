# Advent of Code 2018 - Day 6
# Solution by Oliver Dunkley (https://dunkley.me)


def part_1(input):
    """ Finds the L1 Voronoi diagram by growing every point on the grid until no more points are grown. It's not fast,
    but it works. """

    Xs = []
    Ys = []
    for line in input:
        x, y = [int(c) for c in line.split(',')]
        Xs.append(x)
        Ys.append(y)

    grid = [[None for _ in range(max(Ys) + 1)] for _ in range(max(Xs) + 1)]
    iteration_grid = [[0 for _ in range(max(Ys) + 1)] for _ in range(max(Xs) + 1)]

    for i in range(len(Xs)):
        grid[Xs[i]][Ys[i]] = i

    infinite_discards = set()

    growing = True
    iteration = 1
    while growing:
        grown_this_iteration = False
        for x in range(max(Xs)+1):
            for y in range(max(Ys)+1):
                if grid[x][y] is not None and iteration_grid[x][y] != iteration:
                    if x-1 >= 0:
                        if grid[x-1][y] is None:
                            grid[x-1][y] = grid[x][y]
                            iteration_grid[x-1][y] = iteration
                            grown_this_iteration = True
                        elif grid[x-1][y] != grid[x][y]:
                            if iteration_grid[x-1][y] == iteration:
                                grid[x-1][y] = -1
                    else:
                        infinite_discards.add(grid[x][y])

                    if x+1 <= max(Xs):
                        if grid[x+1][y] is None:
                            grid[x+1][y] = grid[x][y]
                            iteration_grid[x+1][y] = iteration
                            grown_this_iteration = True
                        elif grid[x+1][y] != grid[x][y]:
                            if iteration_grid[x+1][y] == iteration:
                                grid[x+1][y] = -1
                    else:
                        infinite_discards.add(grid[x][y])

                    if y-1 >= 0:
                        if grid[x][y-1] is None:
                            grid[x][y-1] = grid[x][y]
                            iteration_grid[x][y-1] = iteration
                            grown_this_iteration = True
                        elif grid[x][y-1] != grid[x][y]:
                            if iteration_grid[x][y-1] == iteration:
                                grid[x][y-1] = -1
                    else:
                        infinite_discards.add(grid[x][y])

                    if y+1 <= max(Ys):
                        if grid[x][y+1] is None:
                            grid[x][y+1] = grid[x][y]
                            iteration_grid[x][y+1] = iteration
                            grown_this_iteration = True
                        elif grid[x][y+1] != grid[x][y]:
                            if iteration_grid[x][y+1] == iteration:
                                grid[x][y+1] = -1
                    else:
                        infinite_discards.add(grid[x][y])
        iteration += 1
        if not grown_this_iteration:
            growing = False

    counts = {i: 0 for i in range(len(Xs))}
    for x in range(max(Xs)+1):
        for y in range(max(Ys)+1):
            if grid[x][y] != -1:
                counts[grid[x][y]] += 1

    eligible_counts = [counts[i] for i in counts if i not in infinite_discards]

    return max(eligible_counts)


def part_2(input):
    Xs = []
    Ys = []
    for line in input:
        x, y = [int(c) for c in line.split(',')]
        Xs.append(x)
        Ys.append(y)
    grid = [[None for _ in range(max(Ys) + 1)] for _ in range(max(Xs) + 1)]

    for i in range(len(Xs)):
        grid[Xs[i]][Ys[i]] = [i, 0]

    count = 0
    for x in range(max(Xs) + 1):
        for y in range(max(Ys) + 1):
            s = 0
            for i in range(len(Xs)):
                s += abs(Xs[i] - x) + abs(Ys[i] - y)
            if s < 10000:
                count += 1
    return count


if __name__ == "__main__":
    with open("../input/day_06.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
