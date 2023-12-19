from pathlib import Path
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Part:
    id: int
    x: int
    m: int
    a: int
    s: int

    def score(self):
        return self.x + self.m + self.a + self.s


@dataclass
class Rule:
    condition: str
    outcome: str


class Workflow:
    def __init__(self, rule_text):
        rule_texts = rule_text.split(",")
        self.rules = [self.parse_rule(rule_text) for rule_text in rule_texts]

    @staticmethod
    def parse_rule(rule_text):
        if ":" in rule_text:
            condition_text, outcome = rule_text.split(":")
        else:
            condition_text = "True"
            outcome = rule_text

        return Rule(condition_text, outcome)

    def __call__(self, part):
        x, m, a, s = part.x, part.m, part.a, part.s

        for rule in self.rules:
            if eval(rule.condition):
                return rule.outcome


class WorkflowCollection:
    def __init__(self, workflow_text):
        workflow_texts = workflow_text.splitlines()
        self.workflows = dict(self.parse_workflow(workflow_text) for workflow_text in workflow_texts)

    @staticmethod
    def parse_workflow(workflow_text):
        match = re.match(r"([a-zA-Z]+){(.*)}", workflow_text)
        name, workflow_text = match.groups()
        return name, Workflow(workflow_text)

    def __call__(self, part, workflow_name="in"):
        workflow = self.workflows[workflow_name]
        result = workflow(part)
        if result == "A":
            return True
        elif result == "R":
            return False
        else:
            return self(part, workflow_name=result)


def parse_part(part_text, i):
    numbers = re.findall(r"\d+", part_text)
    return Part(i, *map(int, numbers))


def parse_input(filename):
    text = Path(filename).read_text()
    workflow_text, part_text = text.split("\n\n")

    workflows = WorkflowCollection(workflow_text)

    part_texts = part_text.splitlines()
    parts = [parse_part(part_text, i) for i, part_text in enumerate(part_texts)]

    return workflows, parts


if __name__ == "__main__":
    workflows, parts = parse_input("input.txt")
    accepted_parts = [part for part in parts if workflows(part)]
    sum_of_scores = sum(part.score() for part in accepted_parts)
    print(sum_of_scores)