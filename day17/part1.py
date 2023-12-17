from pathlib import Path
import networkx as nx
from itertools import product
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    y: int
    x: int

    def __add__(self, other):
        return Point(self.y + other.y, self.x + other.x)

    def __neg__(self):
        return Point(-self.y, -self.x)


class Graph:
    def __init__(self, filename):
        self.edge_lengths = {}
        for y, line in enumerate(Path(filename).read_text().splitlines()):
            for x, char in enumerate(line):
                self.edge_lengths[Point(y, x)] = int(char)
        self.end_point = Point(y, x)
        self.create_graph()

    def add_edge(self, source, target):
        target_point, *_ = target
        if target_point == self.end_point:
            target = "end"

        if target_point in self.edge_lengths:
            weight = self.edge_lengths[target_point]
            self.graph.add_edge(source, target, weight=weight)

    def create_graph(self):
        self.graph = nx.DiGraph()
        dirs = {Point(0, -1), Point(0, 1), Point(-1, 0), Point(1, 0)}

        for point, count in product(self.edge_lengths.keys(), [1, 2, 3]):
            for dir in dirs:
                if count < 3:
                    self.add_edge(
                        (point, dir, count),
                        (point + dir, dir, count + 1)
                    )
                for new_dir in dirs - {dir, -dir}:
                    self.add_edge(
                        (point, dir, count),
                        (point + new_dir, new_dir, 1)
                    )

        for dir in {Point(1, 0), Point(0, 1)}:
            self.graph.add_edge("start", (dir, dir, 1), weight=self.edge_lengths[dir])

    def compute_shortest_path(self):
        return nx.shortest_path_length(self.graph, "start", "end", weight="weight")


if __name__ == "__main__":
    graph = Graph("input.txt")
    shortest_path = graph.compute_shortest_path()
    print(shortest_path)