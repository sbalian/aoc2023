#!/usr/bin/env python

import pathlib
import re

from rich import print


def read_docs(path):
    lines = pathlib.Path(path).read_text().splitlines()
    instructions = list(lines[0])
    map = {}
    for line in lines[2:]:
        k, v1, v2 = re.findall(r"[A-Z]{3}", line)
        map[k] = (v1, v2)
    return instructions, map


def part1(instructions, map):
    i = 0
    n = len(instructions)
    position = "AAA"
    while True:
        instruction = instructions[i % n]
        if instruction == "R":
            position = map[position][1]
        else:
            position = map[position][0]
        i += 1
        if position == "ZZZ":
            return i


def main():
    instructions, map = read_docs("example1.txt")
    assert part1(instructions, map) == 2
    instructions, map = read_docs("example2.txt")
    assert part1(instructions, map) == 6
    instructions, map = read_docs("input.txt")
    assert part1(instructions, map) == 11309

    print("All tests passed.")


if __name__ == "__main__":
    main()
