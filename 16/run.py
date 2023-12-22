#!/usr/bin/env python

import collections
import pathlib


def read_grid(path):
    return [list(line) for line in pathlib.Path(path).read_text().splitlines()]


def next_positions(position, velocity, grid):
    i, j = position
    tile = grid[i][j]
    num_rows, num_cols = len(grid), len(grid[0])
    match velocity:
        case (0, 1):
            match tile:
                case "." | "-":
                    if j == num_cols - 1:
                        return []
                    else:
                        return [((i, j + 1), velocity)]
                case "|":
                    down = ((i + 1, j), (1, 0))
                    up = ((i - 1, j), (-1, 0))
                    next_ = [up, down]
                    if i == 0:
                        next_.remove(up)
                    elif i == num_rows - 1:
                        next_.remove(down)
                    return next_
                case "/":
                    if i == 0:
                        return []
                    else:
                        return [((i - 1, j), (-1, 0))]
                case "\\":
                    if i == num_rows - 1:
                        return []
                    else:
                        return [((i + 1, j), (1, 0))]
        case (0, -1):
            match tile:
                case "." | "-":
                    if j == 0:
                        return []
                    else:
                        return [((i, j - 1), velocity)]
                case "|":
                    down = ((i + 1, j), (1, 0))
                    up = ((i - 1, j), (-1, 0))
                    next_ = [up, down]
                    if i == 0:
                        next_.remove(up)
                    elif i == num_rows - 1:
                        next_.remove(down)
                    return next_
                case "/":
                    if i == num_rows - 1:
                        return []
                    else:
                        return [((i + 1, j), (1, 0))]
                case "\\":
                    if i == 0:
                        return []
                    else:
                        return [((i - 1, j), (-1, 0))]

        case (1, 0):
            match tile:
                case "." | "|":
                    if i == num_rows - 1:
                        return []
                    else:
                        return [((i + 1, j), velocity)]
                case "-":
                    right = ((i, j + 1), (0, 1))
                    left = ((i, j - 1), (0, -1))
                    next_ = [right, left]
                    if j == 0:
                        next_.remove(left)
                    elif j == num_cols - 1:
                        next_.remove(right)
                    return next_
                case "/":
                    if j == 0:
                        return []
                    else:
                        return [((i, j - 1), (0, -1))]
                case "\\":
                    if j == num_cols - 1:
                        return []
                    else:
                        return [((i, j + 1), (0, 1))]
        case (-1, 0):
            match tile:
                case "." | "|":
                    if i == 0:
                        return []
                    else:
                        return [((i - 1, j), velocity)]
                case "-":
                    right = ((i, j + 1), (0, 1))
                    left = ((i, j - 1), (0, -1))
                    next_ = [right, left]
                    if j == 0:
                        next_.remove(left)
                    elif j == num_cols - 1:
                        next_.remove(right)
                    return next_
                case "/":
                    if j == num_cols - 1:
                        return []
                    else:
                        return [((i, j + 1), (0, 1))]
                case "\\":
                    if j == 0:
                        return []
                    else:
                        return [((i, j - 1), (0, -1))]


def num_energized(grid, initial_position, initial_velocity):
    queue = collections.deque([(initial_position, initial_velocity)])
    visited = set()
    visited_positions = set()
    while queue:
        pos, vel = queue.popleft()
        visited.add((pos, vel))
        visited_positions.add(pos)
        for new_pos, new_vel in next_positions(pos, vel, grid):
            if (new_pos, new_vel) not in visited:
                queue.append((new_pos, new_vel))
    return len(visited_positions)


def max_num_energized(grid):
    energized = []

    for j in range(len(grid[0])):
        energized.append(num_energized(grid, (0, j), (1, 0)))

    for j in range(len(grid[0])):
        energized.append(num_energized(grid, (len(grid) - 1, j), (-1, 0)))

    for i in range(len(grid)):
        energized.append(num_energized(grid, (i, 0), (0, 1)))

    for i in range(len(grid)):
        energized.append(num_energized(grid, (i, len(grid[0]) - 1), (0, -1)))

    return max(energized)


def main():
    grid = read_grid("example.txt")
    initial_position = (0, 0)
    initial_velocity = (0, 1)
    assert num_energized(grid, initial_position, initial_velocity) == 46
    assert max_num_energized(grid) == 51

    grid = read_grid("input.txt")
    initial_position = (0, 0)
    initial_velocity = (0, 1)
    assert num_energized(grid, initial_position, initial_velocity) == 7034
    assert max_num_energized(grid) == 7759
    print("All tests passed.")


if __name__ == "__main__":
    main()
