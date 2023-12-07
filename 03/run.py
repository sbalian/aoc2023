#!/usr/bin/env python

import collections
import pathlib
import re
from typing import NamedTuple

from rich import print


class Number(NamedTuple):
    value: int
    starting_position: tuple[int, int]
    num_digits: int


class Symbol(NamedTuple):
    symbol: str
    position: tuple[int, int]


def read_grid(path: str) -> list[str]:
    return [row for row in pathlib.Path(path).read_text().splitlines()]


def extract_numbers_for_row(row: str, row_index: int) -> list[Number]:
    return [
        Number(
            value=int(m[0]),
            starting_position=(row_index, m.start(0)),
            num_digits=len(m[0]),
        )
        for m in re.finditer(r"\d+", row)
    ]


def extract_numbers(grid: list[str]) -> list[Number]:
    numbers = []
    for row_index, row in enumerate(grid):
        numbers.extend(extract_numbers_for_row(row, row_index))
    return numbers


def is_symbol(string: str) -> bool:
    return not string.isdigit() and string != "."


def symbol_on_left(i: int, j: int, grid: list[str]) -> Symbol | None:
    if j - 1 > 0 and is_symbol(grid[i][j - 1]):
        return Symbol(grid[i][j - 1], (i, j - 1))
    return None


def symbol_on_top(i: int, j: int, grid: list[str]) -> Symbol | None:
    if i - 1 > 0 and is_symbol(grid[i - 1][j]):
        return Symbol(grid[i - 1][j], (i - 1, j))
    return None


def symbol_on_bottom(
    i: int, j: int, grid: list[str], num_rows: int
) -> Symbol | None:
    if i + 1 < num_rows and is_symbol(grid[i + 1][j]):
        return Symbol(grid[i + 1][j], (i + 1, j))
    return None


def symbol_on_top_left(i: int, j: int, grid: list[str]) -> Symbol | None:
    if i - 1 > 0 and j - 1 > 0 and is_symbol(grid[i - 1][j - 1]):
        return Symbol(grid[i - 1][j - 1], (i - 1, j - 1))
    return None


def symbol_on_bottom_left(
    i: int, j: int, grid: list[str], num_rows: int
) -> Symbol | None:
    if i + 1 < num_rows and j - 1 > 0 and is_symbol(grid[i + 1][j - 1]):
        return Symbol(grid[i + 1][j - 1], (i + 1, j - 1))
    return None


def symbol_on_right(
    i: int, j: int, grid: list[str], num_cols: int
) -> Symbol | None:
    if j + 1 < num_cols and is_symbol(grid[i][j + 1]):
        return Symbol(grid[i][j + 1], (i, j + 1))
    return None


def symbol_on_top_right(
    i: int, j: int, grid: list[str], num_cols: int
) -> Symbol | None:
    if i - 1 > 0 and j + 1 < num_cols and is_symbol(grid[i - 1][j + 1]):
        return Symbol(grid[i - 1][j + 1], (i - 1, j + 1))
    return None


def symbol_on_bottom_right(
    i: int, j: int, grid: list[str], num_rows: int, num_cols: int
) -> Symbol | None:
    if i + 1 < num_rows and j + 1 < num_cols and is_symbol(grid[i + 1][j + 1]):
        return Symbol(grid[i + 1][j + 1], (i + 1, j + 1))
    return None


def symbol_for_number(number: Number, grid: list[str]) -> Symbol | None:
    num_rows = len(grid)
    num_cols = len(grid[0])

    i, start_j = number.starting_position
    n = number.num_digits

    for j in range(start_j, start_j + n):
        if j == start_j:
            if symbol := symbol_on_left(i, j, grid):
                return symbol
            if symbol := symbol_on_top(i, j, grid):
                return symbol
            if symbol := symbol_on_bottom(i, j, grid, num_rows):
                return symbol
            if symbol := symbol_on_top_left(i, j, grid):
                return symbol
            if symbol := symbol_on_bottom_left(i, j, grid, num_rows):
                return symbol
            if n == 1:
                if symbol := symbol_on_right(i, j, grid, num_cols):
                    return symbol
                if symbol := symbol_on_top_right(i, j, grid, num_cols):
                    return symbol
                if symbol := symbol_on_bottom_right(
                    i, j, grid, num_rows, num_cols
                ):
                    return symbol
        elif j == start_j + n - 1:
            if symbol := symbol_on_right(i, j, grid, num_cols):
                return symbol
            if symbol := symbol_on_top(i, j, grid):
                return symbol
            if symbol := symbol_on_bottom(i, j, grid, num_rows):
                return symbol
            if symbol := symbol_on_top_right(i, j, grid, num_cols):
                return symbol
            if symbol := symbol_on_bottom_right(
                i, j, grid, num_rows, num_cols
            ):
                return symbol
        else:
            if symbol := symbol_on_top(i, j, grid):
                return symbol
            if symbol := symbol_on_bottom(i, j, grid, num_rows):
                return symbol
    return None


def part1(grid: list[str]) -> int:
    answer = 0
    for number in extract_numbers(grid):
        if symbol_for_number(number, grid):
            answer += number.value
    return answer


def part2(grid: list[str]) -> int:
    gears = collections.defaultdict(list)
    for number in extract_numbers(grid):
        if symbol := symbol_for_number(number, grid):
            if symbol.symbol == "*":
                gears[symbol.position].append(number.value)
    answer = 0
    for numbers in gears.values():
        if len(numbers) == 2:
            answer += numbers[0] * numbers[1]
    return answer


def main() -> None:
    grid = read_grid("example.txt")
    assert part1(grid) == 4361
    assert part2(grid) == 467835

    grid = read_grid("input.txt")
    assert part1(grid) == 529618
    assert part2(grid) == 77509019

    print("All tests passed.")


if __name__ == "__main__":
    main()
