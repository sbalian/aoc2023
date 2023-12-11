#!/usr/bin/env python

import dataclasses
import pathlib

from rich import print


@dataclasses.dataclass(frozen=True)
class Coord:
    i: int
    j: int

    def __add__(self, other):
        return Coord(self.i + other.i, self.j + other.j)


def read_tiles(path):
    tiles = []
    for i, row in enumerate(pathlib.Path(path).read_text().splitlines()):
        tiles.append([])
        for j, tile in enumerate(row):
            if tile == "S":
                start = Coord(i, j)
            tiles[i].append(tile)
    return tiles, start


def set_start_tile(tiles, start, tile):
    tiles[start.i][start.j] = tile
    return tiles


def advance_on_loop(position, velocity, grid):
    tile = grid[position.i][position.j]
    match tile:
        case "|" | "-":
            new_velocity = velocity
        case "L":
            match velocity:
                case Coord(1, 0):
                    new_velocity = Coord(0, 1)
                case Coord(0, -1):
                    new_velocity = Coord(-1, 0)
        case "J":
            match velocity:
                case Coord(0, 1):
                    new_velocity = Coord(-1, 0)
                case Coord(1, 0):
                    new_velocity = Coord(0, -1)
        case "7":
            match velocity:
                case Coord(0, 1):
                    new_velocity = Coord(1, 0)
                case Coord(-1, 0):
                    new_velocity = Coord(0, -1)
        case "F":
            match velocity:
                case Coord(0, -1):
                    new_velocity = Coord(1, 0)
                case Coord(-1, 0):
                    new_velocity = Coord(0, 1)
    return (position + new_velocity), new_velocity


def num_steps_to_farthest(tiles, start, initial_velocity1, initial_velocity2):
    position1, position2 = start, start
    velocity1, velocity2 = initial_velocity1, initial_velocity2
    steps = 0
    while True:
        position1, velocity1 = advance_on_loop(position1, velocity1, tiles)
        position2, velocity2 = advance_on_loop(position2, velocity2, tiles)
        steps += 1
        if position1 == position2:
            return steps


def tiles_inside_loop(tiles, start, initial_velocity):
    # Main idea: when viewing along a certain direction, the flow
    # is clock(anti)wise from inside and anti(clock)wise from outside.
    # We only need to look in one direction (we choose left to right).

    position = start
    velocity = initial_velocity
    loop = {position: initial_velocity}

    while True:
        position, velocity = advance_on_loop(position, velocity, tiles)
        if position == start:
            break
        loop[position] = velocity

    # Assumes the first column has enough outside to cover all pipe encounters
    velocities_from_outside = {}
    for i in range(len(tiles)):
        for j in range(len(tiles)):
            if Coord(i, j) in loop:
                velocities_from_outside[tiles[i][j]] = loop[Coord(i, j)]
                break

    inside = set()
    for i in range(len(tiles)):
        for j in range(len(tiles[i])):
            if Coord(i, j) in loop:
                continue
            for k in range(j + 1, len(tiles[i])):
                if Coord(i, k) in loop:
                    if (
                        loop[Coord(i, k)]
                        != velocities_from_outside[tiles[i][k]]
                    ):
                        inside.add(Coord(i, j))
                    break
    return inside, loop


BETTER_SYMBOLS = {"-": "─", "|": "│", "L": "└", "J": "┘", "7": "┐", "F": "┌"}


def plot(tiles, loop, inside):
    for i in range(len(tiles)):
        line = ""
        for j in range(len(tiles[i])):
            coord = Coord(i, j)
            if coord in loop:
                line += BETTER_SYMBOLS[tiles[i][j]]
            elif coord in inside:
                line += "∙"
            else:
                line += " "
        print(line)
    print()


def main():
    tiles, start = read_tiles("example1.txt")
    set_start_tile(tiles, start, "F")
    assert num_steps_to_farthest(tiles, start, Coord(-1, 0), Coord(0, -1)) == 4
    initial_velocity = Coord(-1, 0)
    inside, loop = tiles_inside_loop(tiles, start, initial_velocity)
    plot(tiles, loop, inside)
    assert len(inside) == 1

    tiles, start = read_tiles("example2.txt")
    set_start_tile(tiles, start, "7")
    initial_velocity = Coord(0, 1)
    inside, loop = tiles_inside_loop(tiles, start, initial_velocity)
    plot(tiles, loop, inside)
    assert len(inside) == 10

    tiles, start = read_tiles("example3.txt")
    set_start_tile(tiles, start, "F")
    initial_velocity = Coord(-1, 0)
    inside, loop = tiles_inside_loop(tiles, start, initial_velocity)
    plot(tiles, loop, inside)
    assert len(inside) == 8

    tiles, start = read_tiles("example4.txt")
    set_start_tile(tiles, start, "F")
    initial_velocity = Coord(-1, 0)
    inside, loop = tiles_inside_loop(tiles, start, initial_velocity)
    plot(tiles, loop, inside)
    assert len(inside) == 4

    tiles, start = read_tiles("input.txt")
    set_start_tile(tiles, start, "|")
    assert (
        num_steps_to_farthest(tiles, start, Coord(-1, 0), Coord(1, 0)) == 6846
    )
    initial_velocity = Coord(1, 0)
    inside, loop = tiles_inside_loop(tiles, start, initial_velocity)
    plot(tiles, loop, inside)
    assert len(inside) == 325

    print("All tests passed.")


if __name__ == "__main__":
    main()
