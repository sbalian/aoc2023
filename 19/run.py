#!/usr/bin/env python

import dataclasses
import pathlib
import re

from rich import print as rprint

WORKFLOW_PATTERN = re.compile(
    r"^([a-z]+){(([xmas][<>]\d+:[a-zAR]+,)+)([a-zAR]+)}$"
)
RULE_PATTERN = re.compile(
    r"^(?P<category>[xmas])(?P<operation>[<>])(?P<rating>\d+):"
    r"(?P<destination>[a-zAR]+)$"
)
PART_PATTERN = re.compile(
    r"^{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}$"
)


@dataclasses.dataclass
class Rule:
    category: str
    operation: str
    rating: int
    destination: str

    @classmethod
    def from_string(cls, string: str):
        match = RULE_PATTERN.match(string)
        assert match is not None
        group_dict = match.groupdict()
        rating = int(group_dict["rating"])
        return cls(
            group_dict["category"],
            group_dict["operation"],
            rating,
            group_dict["destination"],
        )

    def evaluate(self, value) -> bool:
        return eval(f"{value} {self.operation} {self.rating}")


@dataclasses.dataclass
class Workflow:
    name: str
    rules: list[Rule]
    final_destination: str

    @classmethod
    def from_string(cls, string: str):
        match = WORKFLOW_PATTERN.match(string)
        assert match is not None
        groups = match.groups()
        rules = [
            Rule.from_string(rule_string)
            for rule_string in groups[1].split(",")[:-1]
        ]
        return cls(groups[0], rules, groups[-1])


@dataclasses.dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    @classmethod
    def from_string(cls, string: str):
        match = PART_PATTERN.match(string)
        assert match is not None
        group_dict = match.groupdict()
        [x, m, a, s] = [int(group_dict[category]) for category in "xmas"]
        return cls(x, m, a, s)

    def process(self, workflow: Workflow) -> str:
        for rule in workflow.rules:
            if rule.evaluate(getattr(self, rule.category)):
                return rule.destination
        return workflow.final_destination

    def add_ratings(self) -> int:
        return self.x + self.m + self.a + self.s


def read_workflows_and_parts(
    path: pathlib.Path,
) -> tuple[dict[str, Workflow], list[Part]]:
    workflows_lines, part_lines = pathlib.Path(path).read_text().split("\n\n")
    workflows = {}
    for line in workflows_lines.split("\n"):
        workflow = Workflow.from_string(line)
        workflows[workflow.name] = workflow
    parts = []
    for line in part_lines.split("\n"):
        parts.append(Part.from_string(line))
    return workflows, parts


def part1(path):
    workflows, parts = read_workflows_and_parts(path)
    ratings = []
    for part in parts:
        next_destination = "in"
        while next_destination not in "RA":
            next_destination = part.process(workflows[next_destination])
            if next_destination == "A":
                ratings.append(part.add_ratings())
    return sum(ratings)


def main():
    assert part1("example.txt") == 19114
    assert part1("input.txt") == 319062
    rprint("All tests passed.")


if __name__ == "__main__":
    main()
