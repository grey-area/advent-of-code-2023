from pathlib import Path
import numpy as np


'''
Note: my part 2 solution also works on part 1, leaving this here for posterity
'''


class ConditionRecord:
    def __init__(self, line):
        condition, groups_text = line.split(" ")
        self.condition = self.compute_condition_array(condition)
        self.groups = [int(x) for x in groups_text.split(",")]

    @staticmethod
    def compute_condition_array(condition):
        condition_array = np.zeros(len(condition), dtype=np.int8)
        for i, c in enumerate(condition):
            if c == "#":
                condition_array[i] = 1
            elif c == "?":
                condition_array[i] = -1
        return condition_array

    def step(self, condition_so_far, remaining_groups):
        comparison_condition = self.condition[:len(condition_so_far)]

        compatible = np.logical_or(
            condition_so_far == comparison_condition,
            comparison_condition == -1
        ).all()

        if not compatible:
            return 0
        elif len(condition_so_far) == len(self.condition):
            return 1

        last_potential_start_idx = len(self.condition) - (sum(remaining_groups) + len(remaining_groups) - 1)
        potential_start_idc = range(len(condition_so_far), last_potential_start_idx + 1)

        if len(remaining_groups) == 0:
            this_group = 0
        else:
            this_group, remaining_groups = remaining_groups[0], remaining_groups[1:]

        configurations = 0
        for start_idx in potential_start_idc:
            condition_append = [0] * (start_idx - len(condition_so_far)) + [1] * this_group
            if len(remaining_groups) > 0:
                condition_append += [0]
            condition_append = np.array(condition_append)
            new_condition_so_far = np.concatenate((condition_so_far, condition_append))

            if len(remaining_groups) == 0:
                condition_append = np.array([0] * (len(self.condition) - len(new_condition_so_far)))
                new_condition_so_far = np.concatenate((new_condition_so_far, condition_append))

            configurations += self.step(
                new_condition_so_far,
                remaining_groups
            )
        return configurations

    def solve(self):
        return self.step(np.array([]), self.groups)


def parse_input(filename):
    lines = Path(filename).read_text().splitlines()
    condition_records = [ConditionRecord(line) for line in lines]
    return condition_records


if __name__ == "__main__":
    condition_records = parse_input("input.txt")
    num_configurations = sum([condition_record.solve() for condition_record in condition_records])
    print(num_configurations)