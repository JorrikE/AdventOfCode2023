import re
from typing import Final

FILE_NAME: Final[str] = ".\\trebuchet\\input.txt"


def regex_loop() -> int:
    summation: int = 0
    regex = re.compile('\d')
    summation: float = 0
    with open(FILE_NAME) as file:
        for line in file.readlines():
            mps = regex.findall(line)
            if len(mps) == 1:
                mps.append(mps[0])
            summation = summation + int(mps[0] + mps[-1])
    return summation


def dumb_loop() -> int:
    summation: int = 0
    with open(FILE_NAME) as file:
        for line in file.readlines():
            numbers: list[str] = []
            for character in line:
                if character.isnumeric():
                    numbers.append(character)
            if len(numbers) == 1:
                numbers.append(numbers[0])
            summation = summation + int(numbers[0] + numbers[-1])
    return summation


def debug_dumb_loop() -> int:
    summation: int = 0
    with open(FILE_NAME) as file:
        for line in file.readlines():
            print(str(line), end="")
            numbers: list[str] = []
            for character in line:
                if character.isnumeric():
                    numbers.append(character)
            print(f" -> {numbers}", end="")
            if len(numbers) == 1:
                numbers.append(numbers[0])
            print(f" -> {numbers[0]} & {numbers[-1]}", end="")
            value_to_add: int = int(numbers[0] + numbers[-1])
            print(f" -> {value_to_add}")
            summation = summation + value_to_add
    return summation


if __name__ == "__main__":
    print(dumb_loop())
    print(regex_loop())
