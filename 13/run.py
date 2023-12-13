#!/usr/bin/env python

import pathlib

from rich import print


def get_dimensions(grid):
    return len(grid), len(grid[0])


def is_column_reflection(grid, left, right):
    num_rows, num_cols = get_dimensions(grid)

    while left >= 0 and right < num_cols:
        if not all(
            grid[row][left] == grid[row][right] for row in range(num_rows)
        ):
            return False
        left -= 1
        right += 1
    return True


def find_reflection_lines(grid):
    num_rows, num_cols = get_dimensions(grid)
    lines = []
    for left, right in [(i, i + 1) for i in range(num_cols - 1)]:
        if is_column_reflection(grid, left, right):
            lines.append(("vertical", left))

    for up, down in [(i, i + 1) for i in range(num_rows - 1)]:
        if is_row_reflection(grid, up, down):
            lines.append(("horizontal", up))

    return lines


def is_row_reflection(grid, up, down):
    num_rows, num_cols = get_dimensions(grid)
    while up >= 0 and down < num_rows:
        if not all(
            grid[up][col] == grid[down][col] for col in range(num_cols)
        ):
            return False
        up -= 1
        down += 1
    return True


def swap(grid, i, j):
    match grid[i][j]:
        case ".":
            new_value = "#"
        case "#":
            new_value = "."
    row = list(grid[i])
    row[j] = new_value
    grid[i] = "".join(row)


def add_to_summary(summary, orientation, position):
    match orientation:
        case "vertical":
            return summary + position + 1
        case "horizontal":
            return summary + (position + 1) * 100


def read_grids(path):
    grids = []
    for grid in pathlib.Path(path).read_text().split("\n\n"):
        grids.append(grid.split("\n"))
    return grids


def part1(grids):
    summary = 0
    reflection_lines = []
    for grid in grids:
        [(orientation, position)] = find_reflection_lines(grid)
        summary = add_to_summary(summary, orientation, position)
        reflection_lines.append((orientation, position))
    return summary, reflection_lines


def part2(grids, reflection_lines):
    summary = 0
    for i in range(len(grids)):
        num_rows, num_cols = get_dimensions(grids[i])
        for j in range(num_rows):
            for k in range(num_cols):
                swap(grids[i], j, k)
                new_reflection_lines = find_reflection_lines(grids[i])
                swap(grids[i], j, k)
                if reflection_lines[i] in new_reflection_lines:
                    new_reflection_lines.remove(reflection_lines[i])
                if len(new_reflection_lines) == 0:
                    continue
                [(new_orientation, new_position)] = new_reflection_lines
        summary = add_to_summary(summary, new_orientation, new_position)
    return summary


def main():
    grids = read_grids("example.txt")
    summary, reflection_lines = part1(grids)
    assert summary == 405
    assert part2(grids, reflection_lines) == 400

    grids = read_grids("input.txt")
    summary, reflection_lines = part1(grids)
    assert summary == 35691
    assert part2(grids, reflection_lines) == 39037

    print("All tests passed.")


if __name__ == "__main__":
    main()
