import re
from typing import Final, Pattern
from pathlib import Path

INPUT_PATH: Final[Path] = Path(".\\d3gear_ratios\\input.txt")
TEST_LINE: Final[str] = ".58..+.58."
NUMBER_REGEX: Final[Pattern] = re.compile(r"(\d+)")
SYMBOL_REGEX: Final[Pattern] = re.compile(r"([^\d\w\. ]+)")
DEBUG_LINE_COUNTER: int = 0


def get_line_numbers(input_str: str) -> list[tuple[int, tuple[int, int]]]:
    list_of_numbers: list[tuple[int, tuple[int, int]]] = []
    numbers: list[str] = NUMBER_REGEX.findall(input_str)
    for unique_number in set(numbers):
        starting_index: int = None
        for _ in range(input_str.count(unique_number)):
            starting_index = input_str.index(unique_number, starting_index)
            list_of_numbers.append((int(unique_number), (starting_index, starting_index + len(unique_number) - 1)))
            starting_index = starting_index + 1
    return list_of_numbers


def is_symbol(input_str: str) -> bool:
    return bool(SYMBOL_REGEX.match(input_str))


def adjacent_to_symbol(number_location: tuple[int, int], previous_line: str, current_line: str, next_line: str) -> bool:
    x_min: int = max(0, number_location[0] - 1)
    x_max: int = min(number_location[1] + 1, len(previous_line) - 1)
    if is_symbol(current_line[x_min]) or is_symbol(current_line[x_max]):
        print(f"Number at {number_location} on line {DEBUG_LINE_COUNTER} next to {current_line[x_min]} to the left or {current_line[x_max]} to the right")
        return True
    for x in range(x_min, x_max + 1):
        if is_symbol(previous_line[x]) or is_symbol(next_line[x]):
            print(f"Number at {number_location} on line {DEBUG_LINE_COUNTER} next to {previous_line[x]} on line above or {next_line[x]} on line below")
            return True
    return False


def get_sum_of_parts_in_line(current_line: str, previous_line: str | None, next_line: str | None) -> int:
    if isinstance(previous_line, type(None)):
        previous_line = next_line  # Gen zin om met None-types te dealen, gezien het puur om een check van symbolen gaat kunnen we dit doen :D
    elif isinstance(next_line, type(None)):
        next_line = previous_line
    sum_of_parts: int = 0
    current_line_numbers: list[tuple[int, int, int]] = get_line_numbers(current_line)
    for number in current_line_numbers:
        if adjacent_to_symbol(number[1], previous_line, current_line, next_line):
            sum_of_parts = sum_of_parts + number[0]
    return sum_of_parts


def get_sum_of_parts_in_file(input_path: Path) -> int:
    global DEBUG_LINE_COUNTER
    sum_of_parts: int = 0
    with open(INPUT_PATH) as file:
        previous_line: str = None
        current_line: str = file.readline()[:-1]
        next_line: str = file.readline()[:-1]
        while next_line:
            sum_of_parts = sum_of_parts + get_sum_of_parts_in_line(current_line, previous_line, next_line)
            previous_line = current_line
            current_line = next_line
            next_line = file.readline()[:-1]  # Catch that this fails if there is no line available
            DEBUG_LINE_COUNTER = DEBUG_LINE_COUNTER + 1
        sum_of_parts = sum_of_parts + get_sum_of_parts_in_line(current_line, previous_line, None)
    return sum_of_parts


if __name__ == "__main__":
    print(get_sum_of_parts_in_file(INPUT_PATH))


# 545094 too high
# Sooooo values are added that SHOULDN't be?
# But the test input works....
