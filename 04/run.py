#!/usr/bin/env python

import dataclasses
import pathlib
import re

from rich import print


@dataclasses.dataclass
class Card:
    card_number: int
    num_winning_numbers: int
    num_my_numbers: int
    winning_numbers: list[int]
    my_numbers: list[int]
    num_matches: int = dataclasses.field(init=False)
    points: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.num_matches = len(
            set(self.winning_numbers).intersection(set(self.my_numbers))
        )
        self.points = (
            2 ** (self.num_matches - 1) if self.num_matches != 0 else 0
        )

    @classmethod
    def from_dict(
        cls,
        data: dict[str, str],
        num_winning_numbers: int,
        num_my_numbers: int,
    ):
        winning_numbers = []
        my_numbers = []
        for i in range(num_winning_numbers):
            winning_numbers.append(int(data[f"winning_number_{i}"]))
        for i in range(num_my_numbers):
            my_numbers.append(int(data[f"my_number_{i}"]))
        return cls(
            int(data["card_number"]),
            num_winning_numbers,
            num_my_numbers,
            winning_numbers,
            my_numbers,
        )


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
        r"^Card\s+(?P<card_number>\d+):\s+"
        + winning_numbers
        + r"\|"
        + my_numbers
        + "$"
    )


def read_cards(
    path: str, num_winning_numbers: int, num_my_numbers: int
) -> dict[int, Card]:
    cards = {}
    for m in re.finditer(
        build_pattern(num_winning_numbers, num_my_numbers),
        pathlib.Path(path).read_text(),
        re.MULTILINE,
    ):
        card = Card.from_dict(
            m.groupdict(), num_winning_numbers, num_my_numbers
        )
        cards[card.card_number] = card
    return cards


def total_points(cards: dict[int, Card]) -> int:
    return sum(card.points for card in cards.values())


def processed_cards(cards: dict[int, Card]) -> int:
    processed = 0
    stack = list(cards.values())
    while stack:
        card = stack.pop()
        processed += 1
        for i in range(card.num_matches):
            stack.append(cards[card.card_number + i + 1])
    return processed


def main() -> None:
    cards = read_cards("example.txt", 5, 8)
    assert total_points(cards) == 13
    assert processed_cards(cards) == 30
    cards = read_cards("input.txt", 10, 25)
    assert total_points(cards) == 20667
    processed_cards(cards) == 5833065
    print("All tests passed.")


if __name__ == "__main__":
    main()
