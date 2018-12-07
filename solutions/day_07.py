# Advent of Code 2018 - Day 7
# Solution by Oliver Dunkley (https://dunkley.me)

import re
import string


class Node:
    def __init__(self, value):
        self.value = value
        self.time_left = None
        self.next = set()
        self.previous = set()


def construct_graph(input):
    alphabet = list(string.ascii_uppercase)
    weights = {alphabet[i]: 61 + i for i in range(len(alphabet))}
    graph = dict()
    for before, after in [re.match('.+ ([A-Z]).+ ([A-Z]) ', line).groups() for line in input]:
        if after not in graph:
            graph[after] = Node(after)
            graph[after].time_left = weights[after]
        if before not in graph:
            graph[before] = Node(before)
            graph[before].time_left = weights[before]
        graph[before].next.add(graph[after])
        graph[after].previous.add(graph[before])
    return graph


def part_1(input):
    graph = construct_graph(input)
    final_order = []
    while len(graph) > 0:
        task_list = set([letter for letter, node in graph.items() if len(node.previous) == 0])
        step_to_choose = sorted(task_list)[0]
        final_order.append(step_to_choose)
        for letter, node in graph.items():
            node.next.discard(graph[step_to_choose])
            node.previous.discard(graph[step_to_choose])
        del graph[step_to_choose]
    return ''.join(final_order)


def part_2(input):
    graph = construct_graph(input)
    seconds = 0
    while len(graph) > 0:
        task_list = sorted(set([letter for letter, node in graph.items() if len(node.previous) == 0]))
        workers = 5
        for task in task_list[:workers]:
            if graph[task].time_left > 0:
                graph[task].time_left -= 1
            if graph[task].time_left == 0:
                for letter, node in graph.items():
                    node.next.discard(graph[task])
                    node.previous.discard(graph[task])
                del graph[task]
        seconds += 1
    return seconds


if __name__ == "__main__":
    with open("../input/day_07.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
