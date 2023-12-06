from pathlib import Path
import re
from math import ceil, floor


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


def parse_number(line):
    line = line.replace(" ", "")
    number = re.search(r"\d+", line).group()
    return int(number)


def parse_input(filename):
    lines = Path(filename).read_text().splitlines()
    time = parse_number(lines[0])
    max_distance = parse_number(lines[1])

    return Race(time, max_distance)


if __name__ == "__main__":
    race = parse_input("input.txt")
    print(race.compute_number_ways_of_winning())