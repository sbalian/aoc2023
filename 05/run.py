import collections
import concurrent.futures
import dataclasses
import functools
import math
import pathlib


@dataclasses.dataclass
class Map:
    source_starts: list[int] = dataclasses.field(
        init=False, default_factory=list
    )
    source_ends: list[int] = dataclasses.field(
        init=False, default_factory=list
    )
    dest_starts: list[int] = dataclasses.field(
        init=False, default_factory=list
    )
    num_sections: int = dataclasses.field(init=False, default=0)

    def add(self, source_start, dest_start, range_):
        self.source_starts.append(source_start)
        self.source_ends.append(source_start + range_ - 1)
        self.dest_starts.append(dest_start)
        self.num_sections += 1

    def get(self, source):
        for i in range(self.num_sections):
            if self.source_starts[i] <= source <= self.source_ends[i]:
                return self.dest_starts[i] + (source - self.source_starts[i])
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
        soil = maps["seed-to-soil"].get(seed)
        fertilizer = maps["soil-to-fertilizer"].get(soil)
        water = maps["fertilizer-to-water"].get(fertilizer)
        light = maps["water-to-light"].get(water)
        temperature = maps["light-to-temperature"].get(light)
        humidity = maps["temperature-to-humidity"].get(temperature)
        location = maps["humidity-to-location"].get(humidity)
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
