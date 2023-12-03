from pathlib import Path
import re
from itertools import product


class Engine:
    def __init__(self, schematic_filename):
        schematic_lines = Path(schematic_filename).read_text().splitlines()
        self.find_numbers(schematic_lines)
        self.find_symbols(schematic_lines)

    def find_numbers(self, schematic_lines):
        self.number_grid = {}
        self.number_map = {}

        for j, schematic_line in enumerate(schematic_lines):
            for match in re.finditer(r'\d+', schematic_line):
                number = int(match.group())
                number_id = len(self.number_map) + 1
                self.number_map[number_id] = number
                for i in range(match.start(), match.end()):
                    self.number_grid[(i, j)] = number_id

    def find_symbols(self, schematic_lines):
        self.symbol_grid = {}

        for j, schematic_line in enumerate(schematic_lines):
            for match in re.finditer(r"[^\d\.]", schematic_line):
                symbol = match.group()
                i = match.start()
                self.symbol_grid[(i, j)] = symbol

    def find_sum_of_adjacent_numbers(self):
        adjacent_number_ids = set()

        for i, j in self.symbol_grid.keys():
            for i2, j2 in product([i - 1, i, i + 1], [j - 1, j, j + 1]):
                if (i2, j2) in self.number_grid:
                    adjacent_number_ids.add(self.number_grid[(i2, j2)])

        adjacent_numbers = [self.number_map[number_id] for number_id in adjacent_number_ids]
        return sum(adjacent_numbers)


if __name__ == "__main__":
    engine = Engine("input.txt")
    print(engine.find_sum_of_adjacent_numbers())