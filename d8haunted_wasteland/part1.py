import re
from typing import Final, Pattern
from pathlib import Path

INPUT_PATH: Final[Path] = Path(".\\d8haunted_wasteland\\input.txt")
NETWORK_REGEX: Final[Pattern] = re.compile(r"(\w+) = \((\w+), (\w+)\)")
STARTING_ELEMENT: Final[str] = "SCZ"
END_ELEMENT: Final[str] = "Z"


def get_sequence_and_network(input_path: Path) -> tuple[str, dict[str, dict[str, str]]]:
    network: dict[str, dict[str, str]] = {}
    with open(input_path) as file:
        sequence_line = file.readline()[:-1]  # Remove \n
        file.readline()  # skip
        for line in file.readlines():
            mps = NETWORK_REGEX.match(line)
            network[mps.group(1)] = {"L": mps.group(2),
                                     "R": mps.group(3)}
        return sequence_line, network


def increment_instruction_index(current_index: int, sequence_length: int):
    next_index: int = current_index + 1
    return next_index if next_index < sequence_length else 0


def steps_to_the_end(sequence: str, network: dict[str, dict[str, str]]) -> int:
    sequence_length: int = len(sequence)
    steps: int = 0
    instruction_index: int = 0
    current_element: str = STARTING_ELEMENT
    while ((steps == 0) or (current_element[-1] != END_ELEMENT)):
        instruction: str = sequence[instruction_index]
        current_element = network[current_element][instruction]
        steps = steps + 1
        instruction_index = increment_instruction_index(instruction_index, sequence_length)
    return steps


if __name__ == "__main__":
    sequence, network = get_sequence_and_network(INPUT_PATH)
    print(len(sequence))
    print(steps_to_the_end(sequence, network))
