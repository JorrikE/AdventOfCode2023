import re
from typing import Final, Pattern
from pathlib import Path

INPUT_PATH: Final[Path] = Path(".\\d2cube_conundrum\\input.txt")
GAME_ID_REGEX: Final[Pattern] = re.compile(r"Game(\d*)")
NUM_COLOUR_REGEX: Final[Pattern] = re.compile(r"(\d*)(\w*)")


def get_game_info_from_str(input_str: str) -> tuple[int, dict[str, int]]:
    formatted_str: str = input_str.replace(" ", "").replace("\n", "")
    game_id_str, draws_str = formatted_str.split(":")
    game_id: int = int(GAME_ID_REGEX.match(game_id_str).group(1))
    game_info_dict: dict[str, int] = {}
    draws_list = draws_str.split(";")
    for draw_list in draws_list:
        for draw in draw_list.split(","):
            mps = NUM_COLOUR_REGEX.match(draw)
            number: int = int(mps.group(1))
            colour: str = mps.group(2)
            game_info_dict[colour] = max(game_info_dict.get(colour, 0), number)
    return (game_id, game_info_dict)


def get_all_game_infos(input_path: Path) -> dict[int, dict[str, int]]:
    games_info_dict: dict[int, dict[str, int]] = {}
    with open(input_path) as file:
        for line in file.readlines():
            game_id, game_info_dict = get_game_info_from_str(line)
            games_info_dict[game_id] = game_info_dict
    return games_info_dict


def is_game_possible(game_info_dict: dict[str, int], reference_info_dict: dict[str, int]):
    for key in game_info_dict.keys():
        if (key not in reference_info_dict) or (game_info_dict[key] > reference_info_dict[key]):
            return False
    return True


def get_game_power(game_info_dict: dict[str, int]) -> int:
    game_power: int = 1
    for value in game_info_dict.values():
        game_power = game_power * value
    return game_power


def get_sum_of_possible_game_ids(input_path: Path, reference_info_dict: dict[str, int]) -> int:
    sum_of_ids: int = 0
    games_info_dict: dict[int, dict[str, int]] = get_all_game_infos(input_path)
    for id in games_info_dict.keys():
        if is_game_possible(games_info_dict[id], reference_info_dict):
            sum_of_ids = sum_of_ids + id
    return sum_of_ids


def get_sum_of_game_powers(input_path: Path) -> int:
    sum_of_powers: int = 0
    games_info_dict: dict[int, dict[str, int]] = get_all_game_infos(input_path)
    for game_info_dict in games_info_dict.values():
        sum_of_powers = sum_of_powers + get_game_power(game_info_dict)
    return sum_of_powers


if __name__ == "__main__":
    print(get_sum_of_game_powers(INPUT_PATH))
