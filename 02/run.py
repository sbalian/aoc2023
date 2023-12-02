import pathlib

MAX_CUBES = {"red": 12, "green": 13, "blue": 14}


def is_game_possible(game_line: str) -> tuple[bool, int]:
    left, right = game_line.split(":")
    id_ = int(left.replace("Game ", ""))
    cube_counts = right.strip().replace(",", "").replace(";", "").split()
    for i in range(0, len(cube_counts), 2):
        count_ = int(cube_counts[i])
        color = cube_counts[i + 1]
        if count_ > MAX_CUBES[color]:
            return False, id_
    return True, id_


def part1() -> int:
    answer = 0
    for line in pathlib.Path("input.txt").read_text().splitlines():
        possible, id_ = is_game_possible(line)
        if possible:
            answer += id_
    return answer


def min_power(game_line: str) -> int:
    _, right = game_line.split(":")
    cube_counts = right.strip().replace(",", "").replace(";", "").split()
    max_ = {"red": 0, "blue": 0, "green": 0}
    for i in range(0, len(cube_counts), 2):
        count_ = int(cube_counts[i])
        color = cube_counts[i + 1]
        if count_ > max_[color]:
            max_[color] = count_
    return max_["red"] * max_["blue"] * max_["green"]


def part2() -> int:
    answer = 0
    for line in pathlib.Path("input.txt").read_text().splitlines():
        answer += min_power(line)
    return answer


def main() -> None:
    assert part1() == 2563
    assert part2() == 70768
    print("All tests passed.")


if __name__ == "__main__":
    main()
