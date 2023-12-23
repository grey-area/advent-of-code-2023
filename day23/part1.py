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

        self.map = defaultdict(list)
        for point, char in chars.items():
            if char in self.slope_dict:
                self.map[point].append(point + self.slope_dict[char])
            elif char == ".":
                for direction in self.directions:
                    new_point = point + direction
                    if new_point in chars and chars[new_point] != "#":
                        self.map[point].append(new_point)

    # find the longest path from start to end
    def find_paths(self, start, end):
        paths = []
        self._find_paths(start, end, set(), paths)
        return paths

    def _find_paths(self, start, end, path, paths):
        if start == end:
            paths.append(path)
            return

        for new_point in self.map[start]:
            if new_point not in path:
                self._find_paths(new_point, end, path | {new_point}, paths)


if __name__ == "__main__":
    map = Map("input.txt")
    #paths = map.find_paths(Point(0, 1), Point(22, 21))
    paths = map.find_paths(Point(0, 1), Point(140, 139))
    lengths = [len(path) for path in paths]
    print(max(lengths))