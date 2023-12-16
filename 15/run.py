#!/usr/bin/env python

import collections
import pathlib

from rich import print


def hash(string):
    current_value = 0
    for character in string:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


def read_steps(path):
    return pathlib.Path(path).read_text().split(",")


def part1(steps):
    return sum(hash(step) for step in steps)


def part2(steps):
    boxes = collections.defaultdict(list)
    focal_lengths = {}

    for step in steps:
        match step.endswith("-"):
            case True:
                lens = step[:-1]
                box = hash(lens)
                if lens in boxes[box]:
                    boxes[box].remove(lens)
            case _:  # =
                lens = step[:-2]
                focal_length = int(step[-1])
                box = hash(lens)
                if lens not in boxes[box]:
                    boxes[box].append(lens)
                    focal_lengths[(lens, box)] = focal_length
                else:
                    focal_lengths[(lens, box)] = focal_length

    lenses = {}
    for box, lenses_ in boxes.items():
        for i, lens in enumerate(lenses_):
            lenses[lens] = (box, i + 1)

    focusing_power = 0
    for lens in lenses:
        box, slot = lenses[lens]
        focusing_power += (1 + box) * (slot) * focal_lengths[(lens, box)]

    return focusing_power


def main():
    steps = read_steps("example.txt")
    assert part1(steps) == 1320
    assert part2(steps) == 145

    steps = read_steps("input.txt")
    assert part1(steps) == 510273
    assert part2(steps) == 212449
    print("All tests passed.")


if __name__ == "__main__":
    main()
