# Advent of Code 2018 - Day 24
# Solution by Oliver Dunkley (https://dunkley.me)

import re


class Group(object):
    def __init__(self, units, hp, weak, immune, damage, attack_type, initiative, side, id):
        self.units = units
        self.hp = hp
        self.weak = weak
        self.immune = immune
        self.damage = damage
        self.attack_type = attack_type
        self.initiative = initiative
        self.target_by = None
        self.side = side
        self.id = id

    def effective_power(self):
        return self.units * self.damage


def calculate_damage(attack, defense):
    if not defense:
        return 0
    ep = attack.effective_power()
    if attack.attack_type in defense.immune:
        return 0
    elif attack.attack_type in defense.weak:
        return ep*2
    else:
        return ep


def parse_line(line, side, id, boost):
    (units, hp, damage, initiative) = [int(x) for x in re.match(
        r"(\d+) units each with (\d+) hit points .+ that does (\d+) .+ at initiative (\d+)", line).groups()]
    weak_re = re.match(r".+weak to ([a-z, ]+)", line)
    weak = [x.strip() for x in weak_re.groups()[0].split(',')] if weak_re else []
    immune_re = re.match(r".+immune to ([a-z, ]+)", line)
    immune = [x.strip() for x in immune_re.groups()[0].split(',')] if immune_re else []
    attack_type = re.match(r".+ that does \d+ ([a-z]+)", line).groups()[0]
    boosted_damage = damage if side == 1 else damage + boost
    return Group(units, hp, weak, immune, boosted_damage, attack_type, initiative, side, id)


def choose_target(group, opposing_side):
    target = None
    for g in opposing_side:
        if calculate_damage(group, g) > 0:
            if calculate_damage(group, g) > calculate_damage(group, target):
                if not g.target_by:
                    target = g
            elif calculate_damage(group, g) == calculate_damage(group, target):
                if g.effective_power() > target.effective_power():
                    if not g.target_by:
                        target = g
                elif g.effective_power() == target.effective_power():
                    if g.initiative > target.initiative:
                        if not g.target_by:
                            target = g

    if target:
        target.target_by = group
    return target


side_map = {0: 'immune', 1: 'infection'}


def fight_round(groups):
    targets = {}
    for side in (0, 1):
        for group in sorted(sorted(groups[side], key=lambda x: x.initiative, reverse=True),
                            key=lambda x: x.effective_power(), reverse=True):
            # print('ep:', group.effective_power(), ", init:", group.initiative)
            targets[group] = choose_target(group, groups[1-side])

    for attack in sorted(list(targets), key=lambda x: x.initiative, reverse=True):
        defense = targets[attack]
        if defense:
            damage = calculate_damage(attack, defense)
            defense.units -= int(damage/defense.hp)
            defense.units = max(defense.units, 0)
            defense.target_by = None

    for side in (0, 1):
        for group in groups[side]:
            if group.units == 0:
                groups[side].remove(group)


def construct_groups(input, boost=0):
    side, id = 0, 1
    groups = [[], []]
    inp = list(input)
    for line in inp[1:]:
        if line.strip() == '':
            side = 1
            id = 1
        elif line.strip() == "Infection:":
            continue
        else:
            groups[side].append(parse_line(line.strip(), side, id, boost))
            id += 1
    return groups


def part_1(input):
    groups = construct_groups(input)

    round = 0
    winner = None
    while not winner:
        fight_round(groups)
        round += 1
        for side in (0, 1):
            if len(groups[side]) == 0:
                winner = groups[1-side]

    return sum(x.units for x in winner)


def part_2(input):
    linput = list(input)
    boost = 1
    winning_side = 1
    while winning_side != 0:
        groups = construct_groups(linput, boost)
        round = 0
        winner = None
        while not winner:
            fight_round(groups)
            round += 1
            for side in (0, 1):
                if len(groups[side]) == 0:
                    winner = groups[1-side]
                    winning_side = 1 - side
            if round > 10000:  # stop if a round goes on forever (i.e. ties)
                break
        boost += 1

    return sum(x.units for x in winner)


if __name__ == "__main__":
    with open("../input/day_24.txt") as f:
        print(part_1(f))
        f.seek(0)
        print(part_2(f))
