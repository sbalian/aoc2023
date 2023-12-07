#!/usr/bin/env python

import collections
import dataclasses
import pathlib
from typing import ClassVar, Self

from rich import print


@dataclasses.dataclass
class Card:
    label: str
    strength: int

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Card):
            return NotImplemented
        return self.strength < other.strength


def make_cards(labels: list[str]) -> dict[str, Card]:
    return {
        label: Card(label, strength)
        for label, strength in zip(labels, range(len(labels) - 1, -1, -1))
    }


@dataclasses.dataclass
class Hand:
    cards: list[Card]
    bid: int
    strength: int = dataclasses.field(init=False)

    joker_rules: ClassVar[bool] = False
    all_cards: ClassVar[dict[str, Card]] = make_cards(
        ["A", "K", "Q", "J", "T"] + [str(label) for label in range(9, 1, -1)]
    )
    all_cards_with_joker: ClassVar[dict[str, Card]] = make_cards(
        [label for label in all_cards.keys() if label != "J"] + ["J"]
    )
    counts_to_strength: ClassVar[dict[tuple[int, ...], int]] = {
        (5,): 6,
        (1, 4): 5,
        (2, 3): 4,
        (1, 1, 3): 3,
        (1, 2, 2): 2,
        (1, 1, 1, 2): 1,
        (1, 1, 1, 1, 1): 0,
    }

    def __post_init__(self) -> None:
        if len(self.cards) != 5:
            raise ValueError
        counts = collections.Counter([card.label for card in self.cards])
        if not self.joker_rules or "J" not in counts:
            self.strength = self.counts_to_strength[
                tuple(sorted(counts.values()))
            ]
        else:
            match sorted(
                {
                    label: count
                    for label, count in counts.items()
                    if label != "J"
                }.values()
            ):
                case [1, 1, 1, 1]:
                    self.strength = 1
                case [1, 1, 2] | [1, 1, 1]:
                    self.strength = 3
                case [2, 2]:
                    self.strength = 4
                case [1, 3] | [1, 2] | [1, 1]:
                    self.strength = 5
                case _:
                    self.strength = 6
        return

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Hand):
            return NotImplemented
        if self.strength < other.strength:
            return True
        elif self.strength > other.strength:
            return False
        else:  # equal
            for i in range(5):
                if self.cards[i] < other.cards[i]:
                    return True
                elif self.cards[i] > other.cards[i]:
                    return False
        raise RuntimeError("could not break the tie")

    @classmethod
    def from_line(cls, line: str) -> Self:
        hand, bid = line.split()
        if cls.joker_rules:
            cards = cls.all_cards_with_joker
        else:
            cards = cls.all_cards
        return cls(
            [cards[c] for c in hand],
            int(bid),
        )


def read_hands(path: str) -> list[Hand]:
    return [
        Hand.from_line(line)
        for line in pathlib.Path(path).read_text().splitlines()
    ]


def total_winnings(hands: list[Hand]) -> int:
    w = 0
    for i, hand in enumerate(sorted(hands)):
        w += (i + 1) * hand.bid
    return w


def main() -> None:
    hands = read_hands("example.txt")
    assert total_winnings(hands) == 6440
    hands = read_hands("input.txt")
    assert total_winnings(hands) == 251806792

    Hand.joker_rules = True
    hands = read_hands("example.txt")
    assert total_winnings(hands) == 5905
    hands = read_hands("input.txt")
    assert total_winnings(hands) == 252113488

    print("All tests passed.")


if __name__ == "__main__":
    main()
