# Advent of Code 2018 - Day 8
# Solution by Oliver Dunkley (https://dunkley.me)


class Node:
    def __init__(self):
        self.children = []
        self.metadata = []
        self.value = 0


def add_node(i, nums, sum_meta):
    """ Recursive function to create node and add it to the tree as a child of its parent, along with its children. """
    num_children = nums[i]
    num_meta = nums[i+1]
    new_i = i + 2
    new_sum_meta = sum_meta
    new_node = Node()
    for c in range(num_children):
        child, new_i, sum_meta_add = add_node(new_i, nums, sum_meta)
        new_node.children.append(child)
        new_sum_meta += sum_meta_add
    new_node.metadata = nums[new_i:new_i + num_meta]
    if len(new_node.children) == 0:
        new_node.value = sum(new_node.metadata)
    else:
        new_node.value = sum([new_node.children[meta - 1].value for meta in new_node.metadata
                              if 0 < meta <= len(new_node.children)])
    return new_node, new_i + num_meta, new_sum_meta + sum(new_node.metadata)


def part_1(sum_meta):
    return sum_meta


def part_2(root):
    return root.value


if __name__ == "__main__":
    with open("../input/day_08.txt") as f:
        nums = [int(x) for x in f.readline().split(' ')]
        root, _, sum_meta = add_node(0, nums, 0)
        print(part_1(sum_meta))
        print(part_2(root))
