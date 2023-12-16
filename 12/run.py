#!/usr/bin/env python

import pathlib
import re

from rich import print


def read_records(path):
    return pathlib.Path(path).read_text().splitlines()


def num_arrangements(record):
    record, target_counts = record.split()
    target_counts = tuple(int(char) for char in target_counts.split(","))
    n = len(record)
    unknown = [i for i in range(n) if record[i] == "?"]
    pattern = re.compile("#+")
    valid = 0
    for i in range(2 ** len(unknown)):
        template = list(record)
        for j, val in enumerate(str(bin(i))[2:].zfill(len(unknown))):
            match val:
                case "0":
                    template[unknown[j]] = "."
                case "1":
                    template[unknown[j]] = "#"
        if (
            tuple(len(x) for x in pattern.findall("".join(template)))
            == target_counts
        ):
            valid += 1
    return valid


def part1(records):
    return sum(num_arrangements(record) for record in records)


def main():
    records = read_records("example.txt")
    assert part1(records) == 21
    records = read_records("input.txt")
    assert part1(records) == 7344
    print("All tests passed.")


if __name__ == "__main__":
    main()
