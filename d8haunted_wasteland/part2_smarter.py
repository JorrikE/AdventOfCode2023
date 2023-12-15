import re
from typing import Final, Pattern
from pathlib import Path

INPUT_PATH: Final[Path] = Path(".\\d8haunted_wasteland\\input.txt")
NETWORK_REGEX: Final[Pattern] = re.compile(r"(\w+) = \((\w+), (\w+)\)")
STARTING__SUB_ELEMENT: Final[str] = "A"
END_SUB_ELEMENT: Final[str] = "Z"

# Old code I had laying around


def primeFactor(n):
    '''Determine the samllest prime factor below the positive integer n.
    If n is a prime, returns n
    '''
    for ii in range(2, n+1):
        if isPrime(ii) and n % ii == 0:
            return ii


def primeFactors(n, **kwargs):
    '''Determine the prime factorisation of the integer n.
    If n is a prime, returns n
    '''
    if n < 1 or not type(n) == int:
        return None
    factors = kwargs.setdefault('factors', [])
    finalval = kwargs.setdefault('finalval', n)
    if productation(factors) == finalval:
        return factors
    else:
        factor = primeFactor(n)
        factors.append(factor)
        return primeFactors(int(n/factor), factors=factors, finalval=finalval)


def isPrime(n):
    '''Determine whether integer n is prime. Will return False if not a positive integer.
    '''
    if all((n <= 1 or n % 2 == 0, not n == 2)) or not type(n) == int:
        return False
    for ii in range(3, int(n**0.5)+1, 2):
        if n % ii == 0:
            return False
    return True


def productation(m):
    try:
        n = 1
        for ii in m:
            n *= ii
        return n
    except TypeError:
        return m
###


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


def get_all_starting_elements(network: dict[str, dict[str, str]]) -> list[str]:
    return [x for x in network.keys() if x[-1] == STARTING__SUB_ELEMENT]


def get_steps_to_end(starting_element: str, sequence: str, network: dict[str, dict[str, str]], instruction_index: int = 0) -> tuple[int, str, int]:
    sequence_length: int = len(sequence)
    steps: int = 0
    current_element: str = starting_element
    while ((steps == 0) or (current_element[-1] != END_SUB_ELEMENT)):  # Force 1 step to be taken
        instruction: str = sequence[instruction_index]
        current_element = network[current_element][instruction]
        steps = steps + 1
        instruction_index = increment_instruction_index(instruction_index, sequence_length)
    return current_element, steps, instruction_index


def get_steps_to_end_and_loop(starting_element: str, sequence: str, network: dict[str, dict[str, str]]) -> tuple[list[int, list[str]]]:
    end_network: dict[tuple[str, int], dict[str, int | tuple[str, int]]] = {}
    end_element: str = None
    last_instruction: int = None
    starting_instruction: int = 0
    current_starting_element = starting_element
    while (end_element, last_instruction) not in end_network.keys():
        (end_element, steps_to_end, last_instruction) = get_steps_to_end(current_starting_element, sequence, network, starting_instruction)
        end_network[(current_starting_element, starting_instruction)] = {"steps": steps_to_end,
                                                                         "end": (end_element, last_instruction)}
        starting_instruction = last_instruction
        current_starting_element = end_element
    return end_network


def get_end_network(sequence: str, network: dict[str, dict[str, str]]) -> dict[str, tuple[list[int, list[str]]]]:
    end_network: dict[str, dict[tuple[str, int], dict[str, int | tuple[str, int]]]] = {}
    starting_element_list: list[str] = get_all_starting_elements(network)
    for starting_element in starting_element_list:
        end_network[starting_element] = get_steps_to_end_and_loop(starting_element, sequence, network)
    return end_network


if __name__ == "__main__":
    sequence, network = get_sequence_and_network(INPUT_PATH)
    end_network = get_end_network(sequence, network)
    # Observed dat het cyclisch is. JQA -> SCZ -> SCZ, waar alle dezelfde stepsize hebben
    list_of_stepsizes: list[int] = [x["steps"] for x in [end_network[y][(y, 0)] for y in end_network.keys()]]
    print(list_of_stepsizes)
    all_prime_factors: list[list[int]] = [primeFactors(x) for x in list_of_stepsizes]
    print(all_prime_factors)
    flat_prime_factors_set: list[int] = set([factor for factors in all_prime_factors for factor in factors])
    common_multiple: int = 1
    for prime_factor in flat_prime_factors_set:
        max_occurrence: int = 0
        for prime_factors in all_prime_factors:
            max_occurrence = max(max_occurrence, prime_factors.count(prime_factor))
        common_multiple = common_multiple * (prime_factor ** max_occurrence)
    print(common_multiple)
