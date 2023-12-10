#!/usr/bin/env python

import collections
import dataclasses
import math
import pathlib

from rich import print

INF = 10000000000


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
    ranges: list[tuple[Range, int]] = dataclasses.field(
        init=False, default_factory=list
    )

    def add(self, source_start, dest_start, range_length):
        self.ranges.append(
            (
                Range(source_start, source_start + range_length - 1),
                dest_start - source_start,
            ),
        )

    def get_single(self, source):
        for range_, delta in self.ranges:
            if source in range_:
                return source + delta
        return source

    def sort(self):
        self.ranges.sort(key=lambda x: x[0])

    def complete(self):
        self.sort()
        new_ranges = []
        if self.ranges[0][0].start != 0:
            new_ranges.append((Range(0, self.ranges[0][0].start - 1), 0))
        for i in range(len(self.ranges) - 1):
            start = self.ranges[i][0].end + 1
            end = self.ranges[i + 1][0].start - 1
            if (start - end) == 1:
                continue
            new_ranges.append((Range(start, end), 0))
        new_ranges.append((Range(self.ranges[-1][0].end + 1, INF), 0))
        self.ranges.extend(new_ranges)
        self.sort()

    def get_ranges(self, source_range):
        start = source_range.start
        end = source_range.end
        first_range_index = 0
        for range_, _ in self.ranges:
            if start in range_:
                break
            first_range_index += 1

        last_range_index = 0
        for range_, _ in self.ranges:
            if end in range_:
                break
            last_range_index += 1

        if first_range_index == last_range_index:
            range_, delta = self.ranges[first_range_index]
            return [Range(start + delta, end + delta)]

        range_, delta = self.ranges[first_range_index]
        ranges = [Range(start + delta, range_.end + delta)]

        range_, delta = self.ranges[last_range_index]
        ranges.append(Range(range_.start + delta, end + delta))

        for i in range(first_range_index + 1, last_range_index):
            range_, delta = self.ranges[i]
            ranges.append(Range(range_.start + delta, range_.end + delta))
        return ranges


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
    for map in maps:
        maps[map].complete()
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


def min_location_for_range(seed_range, maps):
    soil = maps["seed-to-soil"].get_ranges(seed_range)
    fertilizer = []
    for s in soil:
        fertilizer.extend(maps["soil-to-fertilizer"].get_ranges(s))
    water = []
    for f in fertilizer:
        water.extend(maps["fertilizer-to-water"].get_ranges(f))
    light = []
    for w in water:
        light.extend(maps["water-to-light"].get_ranges(w))
    temperature = []
    for ll in light:
        temperature.extend(maps["light-to-temperature"].get_ranges(ll))
    humidity = []
    for t in temperature:
        humidity.extend(maps["temperature-to-humidity"].get_ranges(t))
    location = []
    for h in humidity:
        location.extend(maps["humidity-to-location"].get_ranges(h))
    return min(location).start


def min_location_for_ranges(seed_ranges, maps):
    return min(
        [
            min_location_for_range(seed_range, maps)
            for seed_range in seed_ranges
        ]
    )


def seed_ranges(seeds):
    ranges = []
    for i in range(0, len(seeds), 2):
        ranges.append(Range(seeds[i], seeds[i] + seeds[i + 1] - 1))
    return ranges


def main():
    seeds, maps = parse_almanac("example.txt")
    assert min_location(seeds, maps) == 35
    assert min_location_for_ranges(seed_ranges(seeds), maps) == 46

    seeds, maps = parse_almanac("input.txt")
    assert min_location(seeds, maps) == 178159714
    assert min_location_for_ranges(seed_ranges(seeds), maps) == 100165128
    print("All tests passed.")


if __name__ == "__main__":
    main()
