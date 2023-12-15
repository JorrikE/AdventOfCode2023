from typing import Final
from pathlib import Path

INPUT_PATH: Final[Path] = Path(".\\d9mirage_maintenance\\input.txt")
TEST_SEQUENCE: Final[list[int]] = [10, 13, 16, 21, 30, 45]


def get_sequences(input_path: Path) -> list[list[int]]:
    sequences: list[list[int]] = []
    with open(input_path) as file:
        for line in file.readlines():
            sequences.append([int(x) for x in line.replace("\n", "").split(" ")])
    return sequences


def get_derivative_sequence(sequence: list[int]) -> list[int]:
    derivative_sequence: list[int] = []
    for idx in range(len(sequence) - 1):
        derivative_sequence.append(sequence[idx+1] - sequence[idx])
    return derivative_sequence


def get_next_value_in_sequence(sequence: list[int]):
    if not any(sequence):  # all values in sequence are 0
        return 0
    return sequence[0] - get_next_value_in_sequence(get_derivative_sequence(sequence))  # REALLY.....


if __name__ == "__main__":
    extrapolated_values: int = 0
    sequences = get_sequences(INPUT_PATH)
    for sequence in sequences:
        extrapolated_values = extrapolated_values + get_next_value_in_sequence(sequence)
    print(extrapolated_values)
