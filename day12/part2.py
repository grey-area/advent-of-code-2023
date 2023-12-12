from pathlib import Path
from functools import cache


class ConditionRecord:
    def __init__(self, line):
        condition, groups_text = line.split(" ")

        # Fold out five times
        self.condition = "?".join([condition] * 5)
        groups_text = ",".join([groups_text] * 5)

        self.groups = tuple(int(x) for x in groups_text.split(","))

    @staticmethod
    @cache
    def count_configurations(condition, groups):
        # No groups left, no broken springs left
        if len(groups) == 0 and "#" not in condition:
            return 1
        # No groups left, but broken springs left
        if len(groups) == 0 and "#" in condition:
            return 0
        # Not enough springs left to account for all groups
        if len(condition) < sum(groups) + len(groups) - 1:
            return 0

        head, tail = condition[0], condition[1:]

        configurations = 0
        # If we have an operational spring, can skip along
        if head == ".":
            configurations = ConditionRecord.count_configurations(tail, groups)
        else:
            # Count the configurations where this spring is operational
            if head == "?":
                configurations += ConditionRecord.count_configurations(tail, groups)

            # If we have a broken spring (? or #), it must be the start of a group
            group_head, group_tail = groups[0], groups[1:]
            condition_head, condition_tail = condition[:group_head], condition[group_head:]
            # If there are no operational springs in the group,
            # and the next spring if there is one is not a broken spring,
            # count configurations where this group is accounted for
            if "." not in condition_head and condition_tail[:1] != "#":
                configurations += ConditionRecord.count_configurations(condition_tail[1:], group_tail)

        return configurations

    def solve(self):
        return self.count_configurations(self.condition, self.groups)


def parse_input(filename):
    lines = Path(filename).read_text().splitlines()
    condition_records = [ConditionRecord(line) for line in lines]
    return condition_records


if __name__ == "__main__":
    condition_records = parse_input("input.txt")
    num_configurations = sum([condition_record.solve() for condition_record in condition_records])
    print(num_configurations)