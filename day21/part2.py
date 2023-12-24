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

    def __init__(self, filename, start):
        self.garden_plots = set()
        self.start = start

        lines = Path(filename).read_text().splitlines()
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                p = Point(y, x)
                if char != "#":
                    self.garden_plots.add(p)

        self.compute_reachability_dict()

    def step_single_point(self, point):
        reachable = set()
        for direction in self.directions:
            new_point = point + direction
            if new_point in self.garden_plots:
                reachable.add(new_point)
        return reachable

    def step(self, reachable):
        new_reachable = set()
        for point in reachable:
            new_reachable.update(self.step_single_point(point))
        return new_reachable

    def compute_reachability_dict(self):
        newly_reachable = {self.start}
        i = 0
        reachable_even_odd = [set(), set()]

        self.reachability_dict = {0: 1}
        while True:
            i += 1
            newly_reachable = self.step(newly_reachable) - reachable_even_odd[i % 2]
            reachable_even_odd[i % 2] |= newly_reachable
            num_reachable = len(reachable_even_odd[i % 2])

            if len(self.reachability_dict) < 2 or num_reachable != self.reachability_dict[i - 2]:
                self.reachability_dict[i] = num_reachable
            else:
                break

    def num_reachable(self, steps):
        if steps in self.reachability_dict:
            return self.reachability_dict[steps]
        else:
            max_idx = len(self.reachability_dict)
            idx_offset = (steps - max_idx) % 2
            return self.reachability_dict[max_idx - 2 + idx_offset]


if __name__ == "__main__":
    start_points = {
        "centre": Point(65, 65),
        "left": Point(65, 0),
        "right": Point(65, 130),
        "top": Point(0, 65),
        "bottom": Point(130, 65),
        "top_left": Point(0, 0),
        "top_right": Point(0, 130),
        "bottom_left": Point(130, 0),
        "bottom_right": Point(130, 130)
    }

    maps = {name: Map("input.txt", start) for name, start in list(start_points.items())}

    total_steps = 26501365
    total = 0

    # center
    total += maps["centre"].num_reachable(total_steps)

    # top, left, right, bottom
    steps = total_steps - 66
    while steps >= 0:
        total += maps["top"].num_reachable(steps)
        total += maps["bottom"].num_reachable(steps)
        total += maps["left"].num_reachable(steps)
        total += maps["right"].num_reachable(steps)
        steps -= 131

    # top_left, top_right, bottom_left, bottom_right
    steps = total_steps - 66 - 66
    n = 1
    while steps >= 0:
        total += n * maps["top_left"].num_reachable(steps)
        total += n * maps["top_right"].num_reachable(steps)
        total += n * maps["bottom_left"].num_reachable(steps)
        total += n * maps["bottom_right"].num_reachable(steps)
        steps -= 131
        n += 1

    print(total)