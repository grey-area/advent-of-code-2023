from pathlib import Path
import re
import numpy as np
from itertools import combinations


class Hail:
    def __init__(self, position, velocity):
        self.p = position
        self.v = velocity

    def ray_intersection_times(h1, h2):
        b = h2.p - h1.p
        A = np.stack([h1.v, -h2.v]).T
        try:
            ts = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            ts = np.array([np.nan, np.nan])
        return ts

    def rays_intersect_in_future_in_bounds(h1, h2):
        t1, t2 = Hail.ray_intersection_times(h1, h2)
        if t1 < 0 or t2 < 0 or np.isnan(t1) or np.isnan(t2):
            return False

        new_p1 = h1.p + t1 * h1.v
        new_p2 = h2.p + t2 * h2.v
        new_ps = np.stack([new_p1, new_p2])

        return np.logical_and(new_ps >= 200000000000000, new_ps <= 400000000000000).all()

class Storm:
    def __init__(self, filename):
        lines = Path(filename).read_text().splitlines()
        self.hail = [Storm.parse_line(line) for line in lines]

    @staticmethod
    def parse_line(line):
        match = re.match(r"(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)", line)
        x, y, z, vx, vy, vz = map(int, match.groups())
        position = np.array([x, y])
        velocity = np.array([vx, vy])
        return Hail(position, velocity)

    def num_pairs_intersecting(self):
        return sum(Hail.rays_intersect_in_future_in_bounds(h1, h2) for h1, h2 in combinations(self.hail, 2))


if __name__ == "__main__":
    storm = Storm("input.txt")
    print(storm.num_pairs_intersecting())