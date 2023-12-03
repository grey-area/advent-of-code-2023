from pathlib import Path
import re
from itertools import product


class Engine:
    def __init__(self, schematic_filename):
        schematic_lines = Path(schematic_filename).read_text().splitlines()
        self.find_numbers(schematic_lines)
        self.find_gears(schematic_lines)

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

    def find_gears(self, schematic_lines):
        self.gear_grid = set()

        for j, schematic_line in enumerate(schematic_lines):
            for match in re.finditer(r"\*", schematic_line):
                i = match.start()
                self.gear_grid.add((i, j))

    def find_sum_of_gear_ratios(self):
        gear_ratios = []

        for i, j in self.gear_grid:
            adjacent_number_ids = set()
            for i2, j2 in product([i - 1, i, i + 1], [j - 1, j, j + 1]):
                if (i2, j2) in self.number_grid:
                    adjacent_number_ids.add(self.number_grid[(i2, j2)])

            if len(adjacent_number_ids) != 2:
                continue
            adjacent_numbers = [self.number_map[number_id] for number_id in adjacent_number_ids]
            gear_ratios.append(adjacent_numbers[0] * adjacent_numbers[1])

        return sum(gear_ratios)


if __name__ == "__main__":
    engine = Engine("input.txt")
    print(engine.find_sum_of_gear_ratios())