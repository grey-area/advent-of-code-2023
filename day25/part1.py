from pathlib import Path
from collections import defaultdict
import graphviz


class Graph:
    def __init__(self, filename):
        self.graph = defaultdict(set)

        for line in Path(filename).read_text().splitlines():
            self.parse_line(line)

    def parse_line(self, line):
        lhs, rhs = line.split(": ")
        rhs = rhs.split()

        for child in rhs:
            self.graph[lhs].add(child)
            self.graph[child].add(lhs)

    def save_visualization(self):
        dot = graphviz.Graph(engine="neato", format="png", strict=True)
        for node in self.graph:
            dot.node(node)
            for child in self.graph[node]:
                dot.edge(node, child)
        dot.render("graph", view=True)

    def remove_edge(self, node, child):
        self.graph[node].remove(child)
        self.graph[child].remove(node)

    def dfs(self, node, visited):
        component = set()
        stack = [node]

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                component.add(node)
                stack.extend(self.graph[node] - visited)

        return component

    def compute_connected_components(self):
        visited = set()
        components = []

        for node in self.graph:
            if node not in visited:
                component = self.dfs(node, visited)
                components.append(component)

        return components


if __name__ == "__main__":
    graph = Graph("input.txt")

    # Found by visual inspection!
    graph.remove_edge("hxr", "gbc")
    graph.remove_edge("xkz", "mvv")
    graph.remove_edge("pnz", "tmt")

    components = graph.compute_connected_components()
    print(len(components[0]) * len(components[1]))