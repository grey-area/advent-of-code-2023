from pathlib import Path
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)

    def __mul__(self, other):
        return Point(self.y * other, self.x * other)


class Map:
    def __init__(self, filename):
        self.corners = self.get_corners(filename)

    @staticmethod
    def get_corners(filename):
        lines = Path(filename).read_text().splitlines()

        position = Point(0, 0)
        directions = {
            "U": Point(-1, 0),
            "D": Point(1, 0),
            "L": Point(0, -1),
            "R": Point(0, 1),
        }

        corners = []
        for line in lines:
            direction_text, distance = Map.parse_line(line)
            direction = directions[direction_text]
            position += direction * distance
            corners.append(position)

        return corners

    @staticmethod
    def parse_line(line):
        match = re.match(r"([UDLR]) (\d+) \((#[0-9a-f]{6})\)", line)
        direction_text, distance, _ = match.groups()
        return direction_text, int(distance)

    def compute_area(self):
        signed_twice_area = 0
        perimeter = 0

        # Shoelace formula for area,
        # then add the missing part of the perimeter.
        for corner1, corner2 in zip(self.corners, self.corners[1:]):
            signed_twice_area += (corner2.x - corner1.x) * (corner2.y + corner1.y)
            perimeter += abs(corner1.x - corner2.x) + abs(corner2.y - corner1.y)
        perimeter += abs(self.corners[0].x - self.corners[-1].x) + abs(self.corners[0].y - self.corners[-1].y)
        area = abs(signed_twice_area // 2) + (perimeter // 2 + 1)

        return area


if __name__ == "__main__":
    map = Map("input.txt")
    area = map.compute_area()
    print(area)