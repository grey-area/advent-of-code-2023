from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict
import sys
sys.setrecursionlimit(10000)


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)


class Map:
    directions = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]
    slope_dict = {">": Point(0, 1), "<": Point(0, -1), "v": Point(1, 0), "^": Point(-1, 0)}

    def __init__(self, filename):
        lines = Path(filename).read_text().splitlines()

        chars = {}
        for j, line in enumerate(lines):
            for i, char in enumerate(line):
                chars[Point(j, i)] = char

        self.graph = defaultdict(list)
        for point, char in chars.items():
            if char in self.slope_dict:
                self.graph[point].append(point + self.slope_dict[char])
            elif char == ".":
                for direction in self.directions:
                    new_point = point + direction
                    if new_point in chars and chars[new_point] != "#":
                        self.graph[point].append(new_point)

        self.start = Point(0, 1)
        self.end = Point(j, i - 1)

    # find the longest path from start to end
    def find_paths(self):
        paths = []
        self._find_paths(self.start, set(), paths)
        return paths

    def _find_paths(self, start, path, paths):
        if start == self.end:
            paths.append(path)
            return

        for new_point in self.graph[start]:
            if new_point not in path:
                self._find_paths(new_point, path | {new_point}, paths)

    def find_longest_path(self):
        paths = self.find_paths()
        lengths = [len(path) for path in paths]
        return max(lengths)


if __name__ == "__main__":
    map = Map("input.txt")
    print(map.find_longest_path())