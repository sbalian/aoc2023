#!/usr/bin/env python

import pathlib

from rich import print


def read_space(path):
    return pathlib.Path(path).read_text().split()


def find_empty_space(space):
    row_indices = []
    for i, row in enumerate(space):
        if row.count(".") == len(row):
            row_indices.append(i)
    col_indices = []
    for j in range(len(space[0])):
        col = []
        for i in range(len(space)):
            col.append(space[i][j])
        if col.count(".") == len(col):
            col_indices.append(j)
    return row_indices, col_indices


def get_galaxies(space):
    galaxies = []
    for i in range(len(space)):
        for j in range(len(space[i])):
            if space[i][j] == "#":
                galaxies.append((i, j))
    return galaxies


def expansion_correction(start, end, indices, multiplier=2):
    c = 0
    for i in range(start, end):
        if i in indices:
            c += 1
    return multiplier * c - c


def shortest_path(galaxy1, galaxy2, empty_rows, empty_cols, multiplier=2):
    if galaxy1[0] > galaxy2[0]:
        if galaxy1[1] < galaxy2[1]:
            return (
                (galaxy2[1] - galaxy1[1])
                + (galaxy1[0] - galaxy2[0])
                + expansion_correction(
                    galaxy1[1], galaxy2[1], empty_cols, multiplier
                )
                + expansion_correction(
                    galaxy2[0], galaxy1[0], empty_rows, multiplier
                )
            )
        else:
            return (
                (galaxy1[1] - galaxy2[1])
                + (galaxy1[0] - galaxy2[0])
                + expansion_correction(
                    galaxy2[1], galaxy1[1], empty_cols, multiplier
                )
                + expansion_correction(
                    galaxy2[0], galaxy1[0], empty_rows, multiplier
                )
            )
    else:
        if galaxy1[1] < galaxy2[1]:
            return (
                (galaxy2[1] - galaxy1[1])
                + (galaxy2[0] - galaxy1[0])
                + expansion_correction(
                    galaxy1[1], galaxy2[1], empty_cols, multiplier
                )
                + expansion_correction(
                    galaxy1[0], galaxy2[0], empty_rows, multiplier
                )
            )
        else:
            return (
                (galaxy1[1] - galaxy2[1])
                + (galaxy2[0] - galaxy1[0])
                + expansion_correction(
                    galaxy2[1], galaxy1[1], empty_cols, multiplier
                )
                + expansion_correction(
                    galaxy1[0], galaxy2[0], empty_rows, multiplier
                )
            )


def shortest_path_sum(galaxies, empty_rows, empty_cols, multiplier=2):
    s = 0
    for i in range(len(galaxies)):
        j = 0
        while j < i:
            s += shortest_path(
                galaxies[i], galaxies[j], empty_rows, empty_cols, multiplier
            )
            j += 1
    return s


def main():
    space = read_space("example.txt")
    empty_rows, empty_cols = find_empty_space(space)
    galaxies = get_galaxies(space)
    assert shortest_path_sum(galaxies, empty_rows, empty_cols) == 374
    assert (
        shortest_path_sum(galaxies, empty_rows, empty_cols, multiplier=10)
        == 1030
    )

    space = read_space("input.txt")
    empty_rows, empty_cols = find_empty_space(space)
    galaxies = get_galaxies(space)
    assert shortest_path_sum(galaxies, empty_rows, empty_cols) == 9556896
    assert (
        shortest_path_sum(galaxies, empty_rows, empty_cols, multiplier=1000000)
        == 685038186836
    )
    print("All tests passed.")


if __name__ == "__main__":
    main()
