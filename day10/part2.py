from pathlib import Path
import re
from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class Coordinate:
    x: int
    y: int

    def __add__(self, other):
        return Coordinate(self.x + other.x, self.y + other.y)

    def __neg__(self):
        return Coordinate(-self.x, -self.y)


class Node:
    connection_types = {"|", "-", "L", "J", "7", "F"}
    connection_dict = {
        "|": {Coordinate(0, 1), Coordinate(0, -1)},
        "-": {Coordinate(1, 0), Coordinate(-1, 0)},
        "L": {Coordinate(1, 0), Coordinate(0, -1)},
        "J": {Coordinate(-1, 0), Coordinate(0, -1)},
        "7": {Coordinate(-1, 0), Coordinate(0, 1)},
        "F": {Coordinate(1, 0), Coordinate(0, 1)},
        ".": set(),
        "S": set()
    }

    def __init__(self, type):
        self.set_connection_type(type)

    def set_connection_type(self, connection_type):
        self.type = connection_type
        self.connections = self.connection_dict[connection_type]


class Map:
    def __init__(self, map_file):
        map_lines = Path(map_file).read_text().splitlines()
        self.start_coordinates = self.find_start_coordinates(map_lines)
        self.map = self.create_map(map_lines)
        self.set_start_type()
        self.loop_coordinates = self.find_loop()
        self.height = len(map_lines)

    @staticmethod
    def find_start_coordinates(map_lines):
        for y, line in enumerate(map_lines):
            match = re.search("S", line)
            if match:
                return Coordinate(match.start(), y)

    @staticmethod
    def create_map(map_lines):
        map = {}
        for y, line in enumerate(map_lines):
            for x, char in enumerate(line):
                map[Coordinate(x, y)] = Node(char)
        return map

    def set_start_type(self):
        for connection_type in Node.connection_types:
            connects_to_all = True

            for connection in Node.connection_dict[connection_type]:
                coordinates = self.start_coordinates + connection
                node = self.map[coordinates]
                if -connection not in node.connections:
                    connects_to_all = False
                    break
            if connects_to_all:
                self.map[self.start_coordinates].set_connection_type(connection_type)
                break

    def find_loop(self):
        coordinates = self.start_coordinates
        connections = self.map[coordinates].connections

        loop_coordinates = set()
        while True:
            loop_coordinates.add(coordinates)
            # if connections has more than one element, pick one, otherwise just use the only element
            connection = next(iter(connections))
            coordinates += connection
            connections = self.map[coordinates].connections - {-connection}
            if coordinates == self.start_coordinates:
                break
        return loop_coordinates

    def count_interior_points_on_line(self, y):
        interior_points = 0
        inside = False
        coordinates = Coordinate(0, y)

        while coordinates in self.map:
            node = self.map[coordinates]
            if coordinates in self.loop_coordinates:
                if node.type in {"|", "7", "F"}:
                    inside = not inside
            elif inside:
                interior_points += 1
            coordinates += Coordinate(1, 0)

        return interior_points

    def count_interior_points(self):
        return sum(self.count_interior_points_on_line(y) for y in range(self.height))


if __name__ == "__main__":
    map = Map("input.txt")
    interior_points = map.count_interior_points()
    print(interior_points)