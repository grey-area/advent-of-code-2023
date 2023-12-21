from pathlib import Path
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)


class Map:
    directions = [Point(-1, 0), Point(0, 1), Point(1, 0), Point(0, -1)]

    def __init__(self, filename):
        self.garden_plots = set()

        for y, line in enumerate(Path(filename).read_text().splitlines()):
            for x, char in enumerate(line):
                p = Point(y, x)
                if char != "#":
                    self.garden_plots.add(p)
                if char == "S":
                    self.start = p

    def step_single_point(self, point):
        return {point + direction for direction in self.directions if point + direction in self.garden_plots}

    def step(self, reachable):
        return set.union(*[self.step_single_point(point) for point in reachable])

    def compute_reachable(self, steps):
        reachable = {self.start}
        for _ in range(steps):
            reachable = self.step(reachable)
        return reachable


if __name__ == "__main__":
    map = Map("input.txt")
    print(len(map.compute_reachable(64)))