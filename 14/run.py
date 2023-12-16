#!/usr/bin/env python

import pathlib

from rich import print as rich_print

std_print = print
print = rich_print


def read_grid(path):
    return [list(line) for line in pathlib.Path(path).read_text().splitlines()]


def part1(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    load = 0
    for j in range(num_cols):
        floor = 0
        for i in range(num_rows):
            if grid[i][j] == "#":
                floor = i + 1
            elif grid[i][j] == "O":
                load += num_rows - floor
                floor += 1
            else:
                continue
    return load


def tilt_north(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    for j in range(num_cols):
        floor = 0
        for i in range(num_rows):
            if grid[i][j] == "#":
                floor = i + 1
            elif grid[i][j] == "O":
                grid[i][j] = "."
                grid[floor][j] = "O"
                floor += 1
            else:
                continue


def tilt_west(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    for i in range(num_rows):
        floor = 0
        for j in range(num_cols):
            if grid[i][j] == "#":
                floor = j + 1
            elif grid[i][j] == "O":
                grid[i][j] = "."
                grid[i][floor] = "O"
                floor += 1
            else:
                continue


def tilt_south(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    for j in range(num_cols):
        floor = num_rows - 1
        for i in reversed(range(num_rows)):
            if grid[i][j] == "#":
                floor = i - 1
            elif grid[i][j] == "O":
                grid[i][j] = "."
                grid[floor][j] = "O"
                floor -= 1
            else:
                continue


def tilt_east(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    for i in range(num_rows):
        floor = num_cols - 1
        for j in reversed(range(num_cols)):
            if grid[i][j] == "#":
                floor = j - 1
            elif grid[i][j] == "O":
                grid[i][j] = "."
                grid[i][floor] = "O"
                floor -= 1
            else:
                continue


def find_north_load(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    load = 0
    for j in range(num_cols):
        for i in range(num_rows):
            if grid[i][j] == "O":
                load += num_rows - i
    return load


def cycle(grid):
    tilt_north(grid)
    tilt_west(grid)
    tilt_south(grid)
    tilt_east(grid)


def print_grid(grid):
    for row in grid:
        std_print("".join(row))
    print()


def part2(grid):
    seen = {}
    i = 0
    loads = []
    while True:
        cycle(grid)
        loads.append(find_north_load(grid))
        state = tuple(map(tuple, grid))
        if state in seen:
            break
        else:
            seen[state] = i
        i += 1
    first_seen = seen[state]
    loads = loads[first_seen:i]
    return loads[(1000000000 - first_seen - 1) % len(loads)]


def main():
    grid = read_grid("example.txt")
    assert part1(grid) == 136
    assert part2(grid) == 64

    grid = read_grid("input.txt")
    assert part1(grid) == 108857
    assert part2(grid) == 95273
    print("All tests passed.")


if __name__ == "__main__":
    main()
