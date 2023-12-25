from pathlib import Path
import re
import numpy as np
from z3 import Int, Solver # cheating


class Hail:
    def __init__(self, position, velocity):
        self.p = position
        self.v = velocity

    def intersect(h1, h2):
        num = h2.p - h1.p
        denom = h1.v - h2.v
        # remove cases where num and denom are both 0
        mask = np.logical_and(num == 0, denom == 0)

        ts = num[~mask] // denom[~mask]
        # check all ts are the same
        return np.all(ts == ts[0])


class Storm:
    def __init__(self, filename):
        lines = Path(filename).read_text().splitlines()
        self.hail = [Storm.parse_line(line) for line in lines]

    @staticmethod
    def parse_line(line):
        match = re.match(r"(-?\d+),\s+(-?\d+),\s+(-?\d+)\s+@\s+(-?\d+),\s+(-?\d+),\s+(-?\d+)", line)
        x, y, z, vx, vy, vz = map(int, match.groups())
        position = np.array([x, y, z])
        velocity = np.array([vx, vy, vz])
        return Hail(position, velocity)


if __name__ == "__main__":
    storm = Storm("input.txt")

    x = Int("x")
    y = Int("y")
    z = Int("z")
    vx = Int("vx")
    vy = Int("vy")
    vz = Int("vz")
    ts = [Int(f"t{i}") for i in range(3)]

    solver = Solver()
    for t, hail in zip(ts, storm.hail):
        solver.add(x + vx * t == hail.p[0] + hail.v[0] * t)
        solver.add(y + vy * t == hail.p[1] + hail.v[1] * t)
        solver.add(z + vz * t == hail.p[2] + hail.v[2] * t)
    solver.check()
    model = solver.model()

    # Now check that the stone intersects all of the hailstones
    p = np.array([model[x].as_long(), model[y].as_long(), model[z].as_long()])
    v = np.array([model[vx].as_long(), model[vy].as_long(), model[vz].as_long()])
    stone = Hail(p, v)

    if not all(Hail.intersect(stone, hail) for hail in storm.hail):
        raise Exception("Stone does not intersect all hailstones")

    print(model[x].as_long() + model[y].as_long() + model[z].as_long())