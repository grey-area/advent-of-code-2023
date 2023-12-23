from pathlib import Path
from dataclasses import dataclass
from collections import defaultdict


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)


class Map:
    directions = [Point(0, 1), Point(0, -1), Point(1, 0), Point(-1, 0)]

    def __init__(self, filename):
        lines = Path(filename).read_text().splitlines()

        chars = {}
        for j, line in enumerate(lines):
            for i, char in enumerate(line):
                chars[Point(j, i)] = char

        graph = defaultdict(dict)
        for point, char in chars.items():
            if char != "#":
                for direction in self.directions:
                    new_point = point + direction
                    if new_point in chars and chars[new_point] != "#":
                        graph[point][new_point] = 1

        self.graph = self.condense_graph(graph)

        self.start = Point(0, 1)
        self.end = Point(j, i - 1)

    @staticmethod
    def condense_graph(graph):
        nodes = set(graph.keys())

        for node in nodes:
            neighbours = graph[node]
            if len(neighbours) == 2:
                neighbour1, neighbour2 = neighbours
                distance = neighbours[neighbour1] + neighbours[neighbour2]

                graph[neighbour1][neighbour2] = distance
                graph[neighbour2][neighbour1] = distance

                del graph[node]
                del graph[neighbour1][node]
                del graph[neighbour2][node]

        return graph

    # find the longest path from start to end
    def find_paths(self):
        lengths = []
        self._find_paths(self.start, set(), 0, lengths)
        return lengths

    def _find_paths(self, start, path, length, lengths):
        if start == self.end:
            lengths.append(length)
            return

        for new_point in self.graph[start]:
            if new_point not in path:
                new_length = length + self.graph[start][new_point]
                self._find_paths(new_point, path | {new_point}, new_length, lengths)

    def find_longest_path(self):
        lengths = self.find_paths()
        return max(lengths)


if __name__ == "__main__":
    map = Map("input.txt")
    print(map.find_longest_path())