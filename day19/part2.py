from pathlib import Path
import re
from dataclasses import dataclass
from collections import defaultdict
from copy import deepcopy


@dataclass
class Range:
    min: float
    max: float

    def __contains__(self, item):
        return self.min <= item <= self.max

    def __and__(self, other):
        return Range(max(self.min, other.min), min(self.max, other.max))

    def __neg__(self):
        if self.min == float("-inf") and self.max != float("inf"):
            return Range(self.max + 1, float("inf"))
        elif self.min != float("-inf") and self.max == float("inf"):
            return Range(float("-inf"), self.min - 1)
        else:
            raise ValueError("Cannot negate range")

    def __len__(self):
        return int(self.max - self.min + 1)


@dataclass
class Rule:
    attribute: str
    range: Range
    outcome: str


class Workflow:
    def __init__(self, rule_text):
        rule_texts = rule_text.split(",")
        self.rules = [self.parse_rule(rule_text) for rule_text in rule_texts]

    @staticmethod
    def parse_rule(rule_text):
        if ":" in rule_text:
            condition_text, outcome = rule_text.split(":")
            match = re.match(r"([xmas])([<>])(\d+)", condition_text)
            attribute, operator, value = match.groups()
            value = float(value)
            if operator == "<":
                range = Range(float("-inf"), value - 1)
            elif operator == ">":
                range = Range(value + 1, float("inf"))

        else:
            attribute = "a"
            range = Range(float("-inf"), float("inf"))
            outcome = rule_text

        return Rule(attribute, range, outcome)


class WorkflowCollection:
    def __init__(self, workflow_text):
        workflow_texts = workflow_text.splitlines()
        self.workflows = dict(self.parse_workflow(workflow_text) for workflow_text in workflow_texts)

    @staticmethod
    def parse_workflow(workflow_text):
        match = re.match(r"([a-zA-Z]+){(.*)}", workflow_text)
        name, workflow_text = match.groups()
        return name, Workflow(workflow_text)

    def compute_backwards_maps(self):
        backwards_maps = defaultdict(set)
        for name, workflow in self.workflows.items():
            for i, rule in enumerate(workflow.rules):
                outcome = rule.outcome
                backwards_maps[outcome].add((name, i))
        return backwards_maps

    def compute_passthrough_rules(self):
        passthrough_rules_dict = {}

        for name, workflow in self.workflows.items():
            rules = {
                "x": Range(float("-inf"), float("inf")),
                "m": Range(float("-inf"), float("inf")),
                "a": Range(float("-inf"), float("inf")),
                "s": Range(float("-inf"), float("inf"))
            }

            passthough_rules = [deepcopy(rules)]
            for rule in workflow.rules[:-1]:
                rules[rule.attribute] &= -rule.range
                passthough_rules.append(deepcopy(rules))
            passthrough_rules_dict[name] = passthough_rules
        return passthrough_rules_dict

    def trace_back(self, outcome, backwards_maps, passthrough_rules_dict, starting_rule):
        reachable_by = backwards_maps[outcome]

        result_rules = []

        for workflow_name, rule_index in reachable_by:
            rules = deepcopy(passthrough_rules_dict[workflow_name][rule_index])

            for attribute, range in starting_rule.items():
                rules[attribute] &= range

            workflow = self.workflows[workflow_name]
            rule = workflow.rules[rule_index]
            rules[rule.attribute] &= rule.range

            if workflow_name == "in":
                result_rules.append(rules)
            else:
                result_rules.extend(self.trace_back(workflow_name, backwards_maps, passthrough_rules_dict, rules))

        return result_rules


    def find_num_combinations(self):
        backwards_maps = self.compute_backwards_maps()
        passthrough_rules_dict = self.compute_passthrough_rules()

        starting_rule = {
            "x": Range(1, 4000),
            "m": Range(1, 4000),
            "a": Range(1, 4000),
            "s": Range(1, 4000)
        }

        num_combinations = 0
        result_rules = self.trace_back("A", backwards_maps, passthrough_rules_dict, starting_rule)
        for result_rule in result_rules:
            num_combinations += len(result_rule["x"]) * len(result_rule["m"]) * len(result_rule["a"]) * len(result_rule["s"])
        return num_combinations


def parse_input(filename):
    text = Path(filename).read_text()
    workflow_text, _ = text.split("\n\n")

    workflows = WorkflowCollection(workflow_text)

    return workflows



if __name__ == "__main__":
    workflows = parse_input("input.txt")
    num_combinations = workflows.find_num_combinations()
    print(num_combinations)