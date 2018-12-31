# Advent of Code 2018 - Day 19
# Solution by Oliver Dunkley (https://dunkley.me)


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

def part_1(input):
    program = []
    ip_index = None
    for row in input:
        if not ip_index:
            ip_index = int(row.split(' ')[1])
        else:
            l = row.strip().split(' ')
            l[1], l[2], l[3] = int(l[1]), int(l[2]), int(l[3])
            program.append(l)

    register = [0,0,0,0,0,0]
    while True:
        ip = register[ip_index]
        if ip < 0 or ip >= len(program):
            break
        ins = program[ip]
        register = operate(register, ins[0], ins[1], ins[2], ins[3])
        register[ip_index] += 1

    return register[0]

def part_2(input):
    program = []
    ip_index = None
    for row in input:
        if not ip_index:
            ip_index = int(row.split(' ')[1])
        else:
            l = row.strip().split(' ')
            l[1], l[2], l[3] = int(l[1]), int(l[2]), int(l[3])
            program.append(l)

    register = [1,0,0,0,0,0]
    count = 0
    while True:
        count += 1
        ip = register[ip_index]
        if ip < 0 or ip >= len(program):
            break
        ins = program[ip]
        register = operate(register, ins[0], ins[1], ins[2], ins[3])
        register[ip_index] += 1
        if count > 1000:
            break

    return sum([i for i in range(1, register[5] + 1) if register[5] % i == 0])


if __name__ == "__main__":
    with open("../input/day_19.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
