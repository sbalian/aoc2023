#!/usr/bin/env python

import collections
import concurrent.futures
import dataclasses
import functools
import math
import pathlib

from rich import print


@dataclasses.dataclass(frozen=True)
class Range:
    start: int
    end: int

    def __lt__(self, other):
        return self.start < other.start

    def __contains__(self, number):
        return self.start <= number <= self.end


@dataclasses.dataclass
class Map:
    ranges: list[Range] = dataclasses.field(init=False, default_factory=list)
    deltas: list[int] = dataclasses.field(init=False, default_factory=list)

    def add(self, source_start, dest_start, range_length):
        self.ranges.append(
            Range(source_start, source_start + range_length - 1)
        )
        self.deltas.append(dest_start - source_start)

    def get_single(self, source):
        for range_, delta in zip(self.ranges, self.deltas):
            if source in range_:
                return source + delta
        return source


def parse_almanac(path):
    maps = collections.defaultdict(Map)
    lines = pathlib.Path(path).read_text().splitlines()
    seeds = [int(seed) for seed in lines[0][7:].split()]
    current_map = None
    for line in lines[2:]:
        split_line = line.split()
        if split_line != []:
            if not split_line[0].isdigit():
                current_map = split_line[0]
            else:
                dest = int(split_line[0])
                source = int(split_line[1])
                range_ = int(split_line[2])
                maps[current_map].add(source, dest, range_)
    return seeds, dict(maps)


def min_location(seeds, maps):
    min_ = math.inf
    for seed in seeds:
        soil = maps["seed-to-soil"].get_single(seed)
        fertilizer = maps["soil-to-fertilizer"].get_single(soil)
        water = maps["fertilizer-to-water"].get_single(fertilizer)
        light = maps["water-to-light"].get_single(water)
        temperature = maps["light-to-temperature"].get_single(light)
        humidity = maps["temperature-to-humidity"].get_single(temperature)
        location = maps["humidity-to-location"].get_single(humidity)
        if location < min_:
            min_ = location
    return min_


def seed_ranges(seeds):
    ranges = []
    for i in range(0, len(seeds), 2):
        ranges.append(range(seeds[i], seeds[i] + seeds[i + 1]))
    return ranges


def min_location_parallel(seed_ranges, maps):
    min_location_ = functools.partial(min_location, maps=maps)
    with concurrent.futures.ProcessPoolExecutor(max_workers=20) as executor:
        return min(executor.map(min_location_, seed_ranges))


def main():
    seeds, maps = parse_almanac("example.txt")
    assert min_location(seeds, maps) == 35
    assert min_location_parallel(seed_ranges(seeds), maps) == 46
    seeds, maps = parse_almanac("input.txt")
    assert min_location(seeds, maps) == 178159714
    # TODO brute force takes two hours running in parallel!
    assert min_location_parallel(seed_ranges(seeds), maps) == 100165128
    print("All tests passed.")


if __name__ == "__main__":
    main()
