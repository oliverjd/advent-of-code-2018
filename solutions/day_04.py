# Advent of Code 2018 - Day 4
# Solution by Oliver Dunkley (https://dunkley.me)

import re
import datetime


def get_guard_times(input):
    sorted_input = sorted(input, key=lambda x: datetime.datetime.strptime(re.match('\[(.+)\]', x).groups()[0],
                                                                          '%Y-%m-%d %H:%M'))
    guard_times = {}
    current_guard = 0
    current_start = 0
    for line in sorted_input:
        mins = int(re.match('.+([0-9].)\]', line).groups()[0])
        if 'begins' in line:
            id = int(re.match('.+\#([0-9]+)', line).groups()[0])
            current_guard = id
            if current_guard not in guard_times:
                guard_times[current_guard] = [0 for _ in range(60)]
        elif 'falls' in line:
            current_start = mins
        elif 'wakes' in line:
            for i in range(current_start, mins):
                guard_times[current_guard][i] += 1
    return guard_times


def part_1(guard_times):
    guard_sums = {guard: sum(guard_times[guard]) for guard in guard_times}
    max_id = max(guard_sums, key=guard_sums.get)
    max_min = guard_times[max_id].index(max(guard_times[max_id]))
    return max_id * max_min


def part_2(guard_times):
    max_id = 0
    max_mins_asleep = 0
    max_min = 0
    for guard in guard_times:
        max_this_guard_mins = max(guard_times[guard])
        if max_this_guard_mins > max_mins_asleep:
            max_min = guard_times[guard].index(max_this_guard_mins)
            max_mins_asleep = max_this_guard_mins
            max_id = guard
    return max_id * max_min


if __name__ == "__main__":
    with open("../input/day_04.txt") as f:
        guard_times = get_guard_times(f)
        print(part_1(guard_times))
        print(part_2(guard_times))
