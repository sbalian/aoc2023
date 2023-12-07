#!/usr/bin/env python

import pathlib
import re
from typing import Callable

from rich import print

SPELLED_OUT_DIGITS = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def reverse_string(string: str) -> str:
    return "".join(reversed(list(string)))


SPELLED_OUT_DIGITS_REVERSED = [
    reverse_string(digit) for digit in SPELLED_OUT_DIGITS
]

DIGIT_MAP = {
    spelled_out_digit: str(i)
    for i, spelled_out_digit in enumerate(SPELLED_OUT_DIGITS, start=1)
}
DIGIT_MAP.update({str(i): str(i) for i in range(1, 10)})


def calibration_value(line: str) -> int:
    """For part 1."""

    first: str | None = None
    last: str | None = None
    for char in line:
        if char.isdigit():
            if first is None:
                first = char
            else:
                last = char
    if last is None:
        last = first
    return int(f"{first}{last}")


def real_calibration_value(line: str) -> int:
    """For part 2."""

    first = re.search(r"|".join(SPELLED_OUT_DIGITS) + r"|\d", line)
    assert first is not None
    last = re.search(
        r"|".join(SPELLED_OUT_DIGITS_REVERSED) + r"|\d", reverse_string(line)
    )
    assert last is not None
    return int(f"{DIGIT_MAP[first[0]]}{DIGIT_MAP[reverse_string(last[0])]}")


def calibration_sum(calibration_function: Callable[[str], int]) -> int:
    answer = 0
    for line in pathlib.Path("input.txt").read_text().splitlines():
        answer += calibration_function(line)
    return answer


def main() -> None:
    assert calibration_sum(calibration_value) == 54331
    assert calibration_sum(real_calibration_value) == 54518
    print("All tests passed.")


if __name__ == "__main__":
    main()
