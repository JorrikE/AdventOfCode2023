from typing import Final
from pathlib import Path

INPUT_PATH: Final[Path] = Path(".\\d5if_you_give_a_seed_a_fertilizer\\input.txt")


class Mapping:
    def __init__(self, source_range_starts: list[int], destination_range_starts: list[int], range_lengths: list[int]) -> None:
        self.source_range_starts: list[int] = source_range_starts
        self.destination_range_start: list[int] = destination_range_starts
        self.range_lengths: list[int] = range_lengths
        self.__post_init__()
        return

    def __post_init__(self) -> None:
        # sort the lists based on source_range_starts
        self.destination_range_start = [x for _, x in sorted(zip(self.source_range_starts, self.destination_range_start))]
        self.range_lengths = [x for _, x in sorted(zip(self.source_range_starts, self.range_lengths))]
        self.source_range_starts = sorted(self.source_range_starts)
        return

    def get_source_index(self, source: int) -> int | None:
        for index in range(len(self.source_range_starts)):
            source_range_start = self.source_range_starts[index]
            source_range_end = source_range_start + self.range_lengths[index] - 1
            if source_range_start <= source <= source_range_end:
                return index
        return None

    def get_destination_for_source(self, source: int) -> int:
        source_index: int | None = self.get_source_index(source)
        if isinstance(source_index, type(None)):
            return source
        source_delta: int = source - self.source_range_starts[source_index]
        destination_start: int = self.destination_range_start[source_index]
        destination: int = destination_start + source_delta
        return destination


def get_seeds_from_seed_str(input_str: str) -> list[int]:
    return [int(x) for x in input_str[:-1].replace("\n", "").lstrip("seeds: ").split(" ")]


def is_seed_in_seeds(seed: int, seeds: list[int]) -> bool:
    for index in range(0, len(seeds), 2):
        seed_number_range_start = seeds[index]
        seed_number_range_end = seed_number_range_start + seeds[index + 1]
        if seed_number_range_start <= seed < + seed_number_range_end:
            return True
    return False


def get_info_from_line(input_str: str) -> tuple[int, int, int]:
    return [int(x) for x in input_str.replace("\n", "").split(" ")]


def get_seeds_and_mapping(input_path: Path) -> tuple[list[int], list[Mapping]]:
    seed_list: list[int] = []
    mapping_list: list[Mapping] = []
    with open(input_path) as file:
        seed_list = get_seeds_from_seed_str(file.readline())
        file.readline()  # skip empty line

        # Initialise lists
        source_range_starts = []
        destination_range_starts = []
        range_lenghts = []

        for line in file.readlines():
            if "map" in line:
                pass
            elif line == "\n":
                mapping_list.append(Mapping(source_range_starts,
                                            destination_range_starts,
                                            range_lenghts))
                source_range_starts = []
                destination_range_starts = []
                range_lenghts = []
            elif len(line) > 1:
                line_info: tuple[int, int, int] = get_info_from_line(line)
                source_range_starts.append(line_info[0])
                destination_range_starts.append(line_info[1])
                range_lenghts.append(line_info[2])
        mapping_list.append(Mapping(source_range_starts,
                                    destination_range_starts,
                                    range_lenghts))
    return (seed_list, mapping_list)


if __name__ == "__main__":
    seeds, mappings = get_seeds_and_mapping(INPUT_PATH)
    mappings.reverse()
    seed_matched: bool = False
    destination_guess: int = 0  # min(seeds)
    while not seed_matched:
        destination = destination_guess
        for mapping in mappings:
            source = mapping.get_destination_for_source(destination)
            destination = source
        if is_seed_in_seeds(destination, seeds):
            seed_matched = True
        else:
            destination_guess = destination_guess + 1
    print(destination_guess, destination)
