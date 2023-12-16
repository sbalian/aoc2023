#!/usr/bin/env python

import pathlib

from rich import print


def hash(string):
    current_value = 0
    for character in string:
        current_value += ord(character)
        current_value *= 17
        current_value %= 256
    return current_value


def part1(path):
    return sum(
        hash(step) for step in pathlib.Path(path).read_text().split(",")
    )


def main():
    assert part1("example.txt") == 1320
    assert part1("input.txt") == 510273
    print("All tests passed.")


if __name__ == "__main__":
    main()
