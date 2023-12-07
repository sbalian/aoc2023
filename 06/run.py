#!/usr/bin/env python

import math
import pathlib

from rich import print


def read_races(path):
    times, distances = pathlib.Path(path).read_text().splitlines()
    times = [int(x) for x in times.split()[1:]]
    distances = [int(x) for x in distances.split()[1:]]
    races = []
    for i in range(len(times)):
        races.append((times[i], distances[i]))
    return races


def read_race(path):
    times, distances = pathlib.Path(path).read_text().splitlines()
    time = int(times.replace("Time:", "").replace(" ", ""))
    distance = int(distances.replace("Distance:", "").replace(" ", ""))
    return time, distance


def num_ways_to_win(time, distance):
    sqrt = math.sqrt(time * time - 4 * distance)
    upper_root = (time + sqrt) / 2
    lower_root = (time - sqrt) / 2
    min_ = math.ceil(lower_root)
    max_ = math.floor(upper_root)
    wtw = max_ - min_ + 1

    # this is equivalent to ...
    # if min_ * min_ - time * min_ + distance == 0:
    #     wtw -= 1
    # if max_ * max_ - time * max_ + distance == 0:
    #     wtw -= 1
    wtw -= sum([float.is_integer(upper_root), float.is_integer(lower_root)])
    return wtw


def part1(races):
    prod = 1
    for time, distance in races:
        prod *= num_ways_to_win(time, distance)
    return prod


def part2(race):
    time, distance = race
    return num_ways_to_win(time, distance)


def main():
    races = read_races("example.txt")
    assert part1(races) == 288
    races = read_races("input.txt")
    assert part1(races) == 440000
    race = read_race("example.txt")
    assert part2(race) == 71503
    race = read_race("input.txt")
    assert part2(race) == 26187338
    print("All tests passed.")


if __name__ == "__main__":
    main()
