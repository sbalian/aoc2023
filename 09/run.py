#!/usr/bin/env python

import pathlib

from rich import print


def read_histories(path):
    return [
        [int(num) for num in line.split()]
        for line in pathlib.Path(path).read_text().splitlines()
    ]


def make_triangle(history):
    n = len(history)
    triangle = [history]
    for d in range(1, n):
        triangle.append([])
        for i in range(n - d):
            triangle[d].append(triangle[d - 1][i + 1] - triangle[d - 1][i])
        if all(val == 0 for val in triangle[d]):
            break
    return triangle


def next_value(triangle):
    n = len(triangle[0])
    for d in range(len(triangle) - 1, -1, -1):
        m = len(triangle[d])
        if d == len(triangle) - 1:
            triangle[d].append(0)
        else:
            triangle[d].append(triangle[d + 1][m - 1] + triangle[d][m - 1])
    return triangle[0][n]


def previous_value(triangle):
    values = []
    for d in range(len(triangle) - 1, -1, -1):
        if d == len(triangle) - 1:
            values.append(0)
        else:
            values.append(triangle[d][0] - values[len(triangle) - d - 2])
    return values[-1]


def find_sum(next_or_prev_func, histories):
    return sum(
        next_or_prev_func(triangle)
        for triangle in [make_triangle(history) for history in histories]
    )


def main():
    histories = read_histories("example.txt")
    assert find_sum(next_value, histories) == 114
    assert find_sum(previous_value, histories) == 2
    histories = read_histories("input.txt")
    assert find_sum(next_value, histories) == 1992273652
    assert find_sum(previous_value, histories) == 1012
    print("All tests passed.")


if __name__ == "__main__":
    main()
