import math
import pathlib
import re
from typing import Generator

LIMITS = {"red": 12, "green": 13, "blue": 14}


def read_games(path: str) -> list[str]:
    return pathlib.Path(path).read_text().splitlines()


def cube_counts(game_line: str) -> Generator[tuple[int, str], None, None]:
    for m in re.finditer(r"\d+\s(red|blue|green)", game_line):
        count_, color = m[0].split(" ")
        yield (int(count_), color)


def game_possible(game_line: str) -> bool:
    for count_, color in cube_counts(game_line):
        if count_ > LIMITS[color]:
            return False
    return True


def part1(game_lines: list[str]) -> int:
    answer = 0
    # Game ids are just 1, 2, 3, ...
    for id_, game_line in enumerate(game_lines, start=1):
        if game_possible(game_line):
            answer += id_
    return answer


def min_power(game_line: str) -> int:
    max_ = {"red": 0, "green": 0, "blue": 0}
    for count_, color in cube_counts(game_line):
        if count_ > max_[color]:
            max_[color] = count_
    return math.prod(max_.values())


def part2(game_lines: list[str]) -> int:
    answer = 0
    for game_line in game_lines:
        answer += min_power(game_line)
    return answer


def main() -> None:
    game_lines = read_games("input.txt")
    assert part1(game_lines) == 2563
    assert part2(game_lines) == 70768
    print("All tests passed.")


if __name__ == "__main__":
    main()
