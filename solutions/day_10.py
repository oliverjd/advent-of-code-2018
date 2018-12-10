# Advent of Code 2018 - Day 10
# Solution by Oliver Dunkley (https://dunkley.me)

import numpy as np
import matplotlib.pyplot as plt
import re

""" Mostly done by trial and error... I'm sure you could programmatically find the time by iterating until the mean 
absolute error between each point is smallest, but I just did it by eye. """

def part_1(input):
    x_list = []
    y_list = []
    xdot_list = []
    ydot_list = []
    for line in input:
        x, y, x_dot, y_dot = [int(x) for x in re.findall(
            r"\<\ *(\-?[0-9]+)\,\ *(\-?[0-9]+)\> .+\<(\ *\-?[0-9]+)\,\ *(\-?[0-9]+)\>", line)[0]]
        x_list.append(x)
        y_list.append(y)
        xdot_list.append(x_dot)
        ydot_list.append(y_dot)
    points = np.column_stack([x_list, y_list])
    accels = np.column_stack([xdot_list, ydot_list])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_ylim([100,200])
    ax.set_xlim([100,300])
    linel, = ax.plot(points.T[0], points.T[1], ls='', marker='o')
    points += 10831*accels
    linel.set_data(points.T[0], points.T[1])
    plt.gca().invert_yaxis()
    plt.show()


def part_2(input):
    return 10831


if __name__ == "__main__":
    with open("../input/day_10.txt") as f:
        print(part_1(f))
        print(part_2(f))
