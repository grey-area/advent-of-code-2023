from pathlib import Path
import re
from itertools import cycle


class Node(dict):
    def __init__(self, left, right):
        self["L"] = left
        self["R"] = right


class Map:
    def __init__(self, filename):
        text = Path(filename).read_text()
        instructions_text, graph_text = text.split("\n\n")

        self.instructions = cycle(instructions_text)
        self.graph = self.parse_graph(graph_text)

    @staticmethod
    def parse_graph(text):
        pattern = re.compile(r"(\w+) = \((\w+), (\w+)\)")

        graph = {}
        for line in text.splitlines():
            try:
                node_name, left, right = pattern.match(line).groups()
            except AttributeError:
                print(line)
                raise AttributeError
            graph[node_name] = Node(left, right)
        return graph

    def step(self, node):
        instruction = next(self.instructions)
        node = self.graph[node][instruction]
        return node

    def run(self):
        node = "AAA"
        steps = 0
        while node != "ZZZ":
            node = self.step(node)
            steps += 1
        return steps


if __name__ == "__main__":
    graph = Map("input.txt")
    steps = graph.run()
    print(steps)