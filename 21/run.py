#!/usr/bin/env python

import pathlib

from rich import print as rprint


def read_grid(path):
    rows = []
    for i, line in enumerate(pathlib.Path(path).read_text().splitlines()):
        row = []
        for j in range(len(line)):
            if line[j] == "S":
                start = (i, j)
            row.append(line[j])
        rows.append(row)
    return rows, start


def get_neighbors(tile, grid):
    num_rows = len(grid)
    num_cols = len(grid[0])
    i, j = tile
    neighbors = [(i, j + 1), (i, j - 1), (i + 1, j), (i - 1, j)]
    if i == 0:
        neighbors.remove((i - 1, j))
    if j == 0:
        neighbors.remove((i, j - 1))
    if i == num_rows - 1:
        neighbors.remove((i + 1, j))
    if j == num_cols - 1:
        neighbors.remove((i, j + 1))
    return [
        neighbor
        for neighbor in neighbors
        if grid[neighbor[0]][neighbor[1]] in ".S"
    ]


def part1(grid, start, max_steps):
    depths = {0: [start]}
    for i in range(1, max_steps + 1):
        children = set([])
        for previous in depths[i - 1]:
            for child in get_neighbors(previous, grid):
                children.add(child)
        depths[i] = children
    return len(depths[max_steps])


def main():
    grid, start = read_grid("example.txt")
    assert part1(grid, start, 6) == 16

    grid, start = read_grid("input.txt")
    assert part1(grid, start, 64) == 3562
    rprint("All tests passed.")


if __name__ == "__main__":
    main()
