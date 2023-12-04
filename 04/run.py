import pathlib
import re


def build_pattern(num_winning_numbers, num_my_numbers) -> str:
    winning_numbers = "".join(
        [
            rf"(?P<winning_number_{i}>\d+)\s+"
            for i in range(num_winning_numbers)
        ]
    )
    my_numbers = "".join(
        [rf"\s+(?P<my_number_{i}>\d+)" for i in range(num_my_numbers)]
    )
    return (
        r"^Card\s+(?P<card_id>\d+):\s+"
        + winning_numbers
        + r"\|"
        + my_numbers
        + "$"
    )


def read_cards(path: str) -> str:
    return pathlib.Path(path).read_text()


def part1(cards: str, num_winning_numbers, num_my_numbers) -> int:
    pattern = build_pattern(num_winning_numbers, num_my_numbers)
    answer = 0
    for m in re.finditer(pattern, cards, re.MULTILINE):
        winning_numbers = set()
        my_numbers = set()
        group_dict = m.groupdict()
        for i in range(num_winning_numbers):
            winning_numbers.add(group_dict[f"winning_number_{i}"])
        for i in range(num_my_numbers):
            my_numbers.add(group_dict[f"my_number_{i}"])
        num_matches = len(winning_numbers.intersection(my_numbers))
        if num_matches > 0:
            answer += 2 ** (num_matches - 1)

    return answer


def main() -> None:
    cards = read_cards("example.txt")
    assert part1(cards, 5, 8) == 13
    print("All tests passed.")
    cards = read_cards("input.txt")
    assert part1(cards, 10, 25) == 20667


if __name__ == "__main__":
    main()
