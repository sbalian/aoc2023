#!/usr/bin/env python

import pathlib

from rich import print as rprint


def det(matrix):
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def read_dig_plan(path, use_color=False):
    map_ = {"0": "R", "1": "D", "2": "L", "3": "U"}
    plan = []
    for line in pathlib.Path(path).read_text().splitlines():
        d, s, c = line.split()
        if not use_color:
            s = int(s)
        else:
            c = c[2:-1]
            s = int(c[:-1], base=16)
            d = map_[c[-1]]
        plan.append((d, s))
    return plan


def get_corner_points_and_edge_count(plan):
    position = (0, 0)
    points = []
    edge_count = 0

    for direction, step in plan:
        match direction:
            case "L":
                position = (position[0], position[1] - step)
            case "R":
                position = (position[0], position[1] + step)
            case "U":
                position = (position[0] + step, position[1])
            case "D":
                position = (position[0] - step, position[1])
        points.append(position)
        edge_count += step
    return points, edge_count


def compute_area(corner_points, edge_count):
    twice_area = 0
    for point1, point2 in zip(corner_points, corner_points[1:]):
        matrix = [
            [point1[0], point2[0]],
            [point1[1], point2[1]],
        ]
        twice_area += det(matrix)

    twice_area += det(
        [
            [corner_points[-1][0], corner_points[0][0]],
            [corner_points[-1][1], corner_points[0][1]],
        ]
    )
    return int(abs(twice_area / 2) + edge_count / 2 + 1)


def main():
    plan = read_dig_plan("example.txt")
    points, edge_count = get_corner_points_and_edge_count(plan)
    assert compute_area(points, edge_count) == 62

    plan = read_dig_plan("example.txt", use_color=True)
    points, edge_count = get_corner_points_and_edge_count(plan)
    assert compute_area(points, edge_count) == 952408144115

    plan = read_dig_plan("input.txt")
    points, edge_count = get_corner_points_and_edge_count(plan)
    assert compute_area(points, edge_count) == 92758

    plan = read_dig_plan("input.txt", use_color=True)
    points, edge_count = get_corner_points_and_edge_count(plan)
    assert compute_area(points, edge_count) == 62762509300678

    rprint("All tests passed.")


if __name__ == "__main__":
    main()
