from pathlib import Path
import re


class Map:
    def __init__(self, text):
        self.parse_map(text)

    def parse_map(self, text):
        lines = text.splitlines()
        for line in lines:
            match = re.search(r"(\d+)\s+(\d+)\s+(\d+)", line)
            destination_start, source_start, length = match.groups()
            self.source_start = int(source_start)
            self.destination_start = int(destination_start)
            self.source_end = self.source_start + int(length) - 1

    def __contains__(self, index):
        return self.source_start <= index <= self.source_end

    def __call__(self, index):
        offset = index - self.source_start
        return self.destination_start + offset


# recursive binary search to find last element that satisfies condition
def binary_search(low, high, condition):
    if low > high:
        return None

    mid = low + (high - low) // 2

    if condition(mid):
        # If the condition is satisfied at mid, check the right half
        result = binary_search(mid + 1, high, condition)
        if result is not None:
            return result
        else:
            return mid
    else:
        # If the condition is not satisfied at mid, check the left half
        return binary_search(low, mid - 1, condition)


class MapCollection:
    def __init__(self, text):
        self.maps = [Map(line) for line in text.splitlines()[1:]]

    def get_map(self, index):
        for map in self.maps:
            if index in map:
                return map
        return None

    '''
    This function takes a value range and maps it to a list of ranges using
    the relevant maps in the map collection. Binary search is used to find
    the edges of the result ranges.
    '''
    def __call__(self, value_range, result_ranges):
        start_value = value_range.start

        start_map = self.get_map(start_value)
        if not start_map:
            mapped_start_value = start_value
        else:
            mapped_start_value = start_map(start_value)

        end_value = binary_search(
            start_value + 1,
            value_range.stop,
            lambda x: self.get_map(x) == start_map
        )

        if end_value is not None:
            result_ranges.append(range(mapped_start_value, mapped_start_value + end_value - start_value))
            next_range = range(end_value + 1, value_range.stop)
            return self(next_range, result_ranges)
        else:
            result_ranges.append(range(mapped_start_value, mapped_start_value + value_range.stop - start_value))
            return result_ranges


def parse_seeds(text):
    seed_numbers = [int(x) for x in re.findall(r"\d+", text)]
    pairs = zip(seed_numbers[::2], seed_numbers[1::2])
    ranges = [range(start, start + num) for start, num in pairs]
    return ranges


def parse_input(filename):
    sections = Path(filename).read_text().split("\n\n")
    seeds = parse_seeds(sections[0])
    map_collections = [MapCollection(text) for text in sections[1:]]
    return seeds, map_collections


if __name__ == "__main__":
    value_ranges, map_collections = parse_input("input.txt")

    for map_collection in map_collections:
        new_value_ranges = []
        for value_range in value_ranges:
            new_value_ranges.extend(map_collection(value_range, result_ranges=[]))
        value_ranges = new_value_ranges

    min_value = min(value.start for value in value_ranges)
    print(min_value)