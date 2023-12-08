#!/usr/bin/env python

import math
import pathlib
import re

from rich import print


def read_docs(path):
    lines = pathlib.Path(path).read_text().splitlines()
    instructions = list(lines[0])
    map = {}
    for line in lines[2:]:
        start, left, right = re.findall(r"[A-Z\d]{3}", line)
        map[start] = (left, right)
    return instructions, map


def steps_to_first_end(instructions, map, start="AAA", part=1):
    i, n, position = 0, len(instructions), start
    while True:
        match instructions[i % n]:
            case "R":
                position = map[position][1]
            case "L":
                position = map[position][0]
        i += 1
        match part:
            case 1:
                if position == "ZZZ":
                    return i
            case 2:
                if position.endswith("Z"):
                    return i


def part2(instructions, map):
    return math.lcm(
        *[
            steps_to_first_end(instructions, map, start=start, part=2)
            for start in [node for node in map.keys() if node.endswith("A")]
        ]
    )


def main():
    instructions, map = read_docs("example1.txt")
    assert steps_to_first_end(instructions, map) == 2
    instructions, map = read_docs("example2.txt")
    assert steps_to_first_end(instructions, map) == 6
    instructions, map = read_docs("input.txt")
    assert steps_to_first_end(instructions, map) == 11309

    instructions, map = read_docs("example3.txt")
    assert part2(instructions, map) == 6
    instructions, map = read_docs("input.txt")
    assert part2(instructions, map) == 13740108158591

    print("All tests passed.")


if __name__ == "__main__":
    main()
