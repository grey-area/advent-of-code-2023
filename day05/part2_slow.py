from pathlib import Path
import re
from itertools import chain


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


class MapCollection:
    def __init__(self, text):
        self.maps = [Map(line) for line in text.splitlines()[1:]]

    def __call__(self, index):
        for map in self.maps:
            if index in map:
                return map(index)
        return index


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
    seed_ranges, map_collections = parse_input("input.txt")

    min_location = float("inf")
    total = sum(len(x) for x in seed_ranges)
    for i, seed in enumerate(chain(*seed_ranges)):
        value = seed

        for map_collection in map_collections:
            value = map_collection(value)
        min_location = min(min_location, value)
        if i % 100000 == 0:
            print(i / total)

    print(min_location)