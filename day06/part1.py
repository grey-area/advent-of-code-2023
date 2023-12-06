from pathlib import Path
import re
from math import ceil, floor
from functools import reduce
from operator import mul


def product(iterable):
    return reduce(mul, iterable, 1)


class Race:
    def __init__(self, time, max_distance):
        self.time = time
        self.max_distance = max_distance

    def compute_times_to_match_previous_record(self):
        sqrt_term = self.time**2 - 4 * self.max_distance
        time1 = (self.time + sqrt_term**0.5) / 2
        time2 = (self.time - sqrt_term**0.5) / 2
        return time1, time2

    def compute_number_ways_of_winning(self):
        time1, time2 = self.compute_times_to_match_previous_record()
        min_time, max_time = min(time1, time2), max(time1, time2)
        times_between = floor(max_time) - ceil(min_time) + 1
        if max_time.is_integer():
            times_between -= 1
        if min_time.is_integer():
            times_between -= 1
        return times_between


def parse_numbers(line):
    return [int(x) for x in re.findall(r"\d+", line)]


def parse_input(filename):
    lines = Path(filename).read_text().splitlines()
    times = parse_numbers(lines[0])
    max_distances = parse_numbers(lines[1])

    return [Race(time, max_distance) for time, max_distance in zip(times, max_distances)]


if __name__ == "__main__":
    races = parse_input("input.txt")

    answer = product(race.compute_number_ways_of_winning() for race in races)
    print(answer)