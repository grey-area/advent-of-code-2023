from pathlib import Path
import re
from itertools import product
from math import lcm


class Node(dict):
    def __init__(self, left, right):
        self["L"] = left
        self["R"] = right


class Ghost:
    def __init__(self, graph, instructions, start_node):
        self.instructions = instructions
        self.instructions_index = 0
        self.graph = graph
        self.start_node = start_node

    @property
    def instruction(self):
        return self.instructions[self.instructions_index]

    def step(self, node):
        node = self.graph[node][self.instruction]
        self.instructions_index = (self.instructions_index + 1) % len(self.instructions)
        return node

    def run(self):
        node = self.start_node
        steps = 0

        state_history = set()
        visit_times = {}
        while (node, self.instructions_index) not in state_history:
            state_history.add((node, self.instructions_index))
            if node not in visit_times:
                visit_times[node] = steps
            node = self.step(node)
            steps += 1
        return visit_times


class Map:
    def __init__(self, filename):
        text = Path(filename).read_text()
        instructions_text, graph_text = text.split("\n\n")
        self.graph = self.parse_graph(graph_text)

        self.start_nodes = [node for node in self.graph.keys() if node.endswith("A")]
        self.end_nodes = [node for node in self.graph.keys() if node.endswith("Z")]

        self.ghosts = {}
        for start_node in self.start_nodes:
            self.ghosts[start_node] = Ghost(
                self.graph, instructions_text, start_node
            )

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

    def run(self):
        end_state_times = {}
        for start_node, graph in self.ghosts.items():
            visit_times = graph.run()
            end_state_times[start_node] = [time for node, time in visit_times.items() if node in self.end_nodes]

        # Find the set of end states that has the lowest least common multiple
        # of the times it takes to reach them
        possible_end_states = product(*end_state_times.values())
        possible_end_times = [lcm(*times) for times in possible_end_states]
        return min(possible_end_times)


if __name__ == "__main__":
    graph = Map("input.txt")
    end_time = graph.run()
    print(end_time)