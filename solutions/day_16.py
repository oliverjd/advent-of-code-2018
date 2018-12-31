# Advent of Code 2018 - Day 16
# Solution by Oliver Dunkley (https://dunkley.me)

from hopcroftkarp import HopcroftKarp


def otherwise_equal(before, after, C):
    check = [0, 1, 2, 3]
    check.remove(C)
    for i in check:
        if before[i] != after[i]:
            return False
    return True


def get_possible_opcodes(before, instruction, after):
    possible = []

    A = instruction[1]
    B = instruction[2]
    C = instruction[3]

    if before[A] + before[B] == after[C] and otherwise_equal(before, after, C):
        possible.append('addr')
    if before[A] + B == after[C] and otherwise_equal(before, after, C):
        possible.append('addi')
    if before[A] * before[B] == after[C] and otherwise_equal(before, after, C):
        possible.append('mulr')
    if before[A] * B == after[C] and otherwise_equal(before, after, C):
        possible.append('muli')
    if before[A] & before[B] == after[C] and otherwise_equal(before, after, C):
        possible.append('banr')
    if before[A] & B == after[C] and otherwise_equal(before, after, C):
        possible.append('bani')
    if before[A] | before[B] == after[C] and otherwise_equal(before, after, C):
        possible.append('borr')
    if before[A] | B == after[C] and otherwise_equal(before, after, C):
        possible.append('bori')
    if before[A] == after[C] and otherwise_equal(before, after, C):
        possible.append('setr')
    if A == after[C] and otherwise_equal(before, after, C):
        possible.append('seti')
    if (A > before[B] and after[C] == 1 or A <= before[B] and after[C] == 0) and otherwise_equal(before, after, C):
        possible.append('gtir')
    if (before[A] > B and after[C] == 1 or before[A] <= B and after[C] == 0) and otherwise_equal(before, after, C):
        possible.append('gtri')
    if (before[A] > before[B] and after[C] == 1 or before[A] <= before[B] and after[C] == 0) and otherwise_equal(before, after, C):
        possible.append('gtrr')
    if (A == before[B] and after[C] == 1 or A != before[B] and after[C] == 0) and otherwise_equal(before, after, C):
        possible.append('eqir')
    if (before[A] == B and after[C] == 1 or before[A] != B and after[C] == 0) and otherwise_equal(before, after, C):
        possible.append('eqri')
    if (before[A] == before[B] and after[C] == 1 or before[A] != before[B] and after[C] == 0) and otherwise_equal(before, after, C):
        possible.append('eqrr')

    return possible


def part_1(input):
    possible_opcodes = {i: set() for i in range(16)}
    three_or_more = 0
    before = []
    instruction = []
    blank_lines = 0
    for row in input:
        if 'Before' in row:
            before = list([int(x) for x in row.split(':')[1].strip().strip('[').strip(']').split(',')])
        elif 'After' in row:
            after = list([int(x) for x in row.split(':')[1].strip().strip('[').strip(']').split(',')])
            possible = get_possible_opcodes(before, instruction, after)
            if len(possible) >= 3:
                three_or_more += 1
            possible_opcodes[instruction[0]].update(possible)
            blank_lines = 0
        else:
            if row.strip():
                instruction = [int(x) for x in row.split(' ')]
            else:
                blank_lines += 1
                if blank_lines > 1:
                    break

    return three_or_more


def operate(reg, op, A, B, C):
    if op == 'addr':
        reg[C] = reg[A] + reg[B]
    elif op == 'addi':
        reg[C] = reg[A] + B
    elif op == 'mulr':
        reg[C] = reg[A] * reg[B]
    elif op == 'muli':
        reg[C] = reg[A] * B
    elif op == 'banr':
        reg[C] = reg[A] & reg[B]
    elif op == 'bani':
        reg[C] = reg[A] & B
    elif op == 'borr':
        reg[C] = reg[A] | reg[B]
    elif op == 'bori':
        reg[C] = reg[A] | B
    elif op == 'setr':
        reg[C] = reg[A]
    elif op == 'seti':
        reg[C] = A
    elif op == 'gtir':
        reg[C] = int(A > reg[B])
    elif op == 'gtri':
        reg[C] = int(reg[A] > B)
    elif op == 'gtrr':
        reg[C] = int(reg[A] > reg[B])
    elif op == 'eqir':
        reg[C] = int(A == reg[B])
    elif op == 'eqri':
        reg[C] = int(reg[A] == B)
    elif op == 'eqrr':
        reg[C] = int(reg[A] == reg[B])
    else:
        raise Exception
    return reg


def part_2(input):
    possible_opcodes = {i: set() for i in range(16)}
    before = []
    instruction = []
    blank_lines = 0
    for row in input:
        if 'Before' in row:
            before = list([int(x) for x in row.split(':')[1].strip().strip('[').strip(']').split(',')])
        elif 'After' in row:
            after = list([int(x) for x in row.split(':')[1].strip().strip('[').strip(']').split(',')])
            possible = get_possible_opcodes(before, instruction, after)
            possible_opcodes[instruction[0]].update(possible)
            blank_lines = 0
        else:
            if row.strip():
                instruction = [int(x) for x in row.split(' ')]
            else:
                blank_lines += 1
                if blank_lines > 1:
                    break

    match = HopcroftKarp(possible_opcodes).maximum_matching()
    opcodes = {a: b for a, b in match.items() if type(a) == int}

    instructions = []
    for row in input:
        if row.strip():
            instructions.append([int(x) for x in row.strip().split(' ')])

    registers = [0, 0, 0, 0]
    for ins in instructions:
        registers = operate(registers, opcodes[ins[0]], ins[1], ins[2], ins[3])

    return registers[0]


if __name__ == "__main__":
    with open("../input/day_16.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
