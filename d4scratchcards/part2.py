import re
from typing import Final, Pattern
from pathlib import Path

INPUT_PATH: Final[Path] = Path(".\\d4scratchcards\\input.txt")
NUMBER_REGEX: Final[Pattern] = re.compile(r"(\d+)")
CARD_ID_REGEX: Final[Pattern] = re.compile(r"Card\s*(\d+)")


def get_card_info(input_str: str) -> tuple[int, list[int, list[int]]]:
    card_id_str, numbers_str = input_str.split(":")
    card_id: int = int(CARD_ID_REGEX.match(card_id_str).group(1))
    win_list_str, have_list_str = numbers_str.split("|")
    win_list: list[int] = [int(win_num_str) for win_num_str in NUMBER_REGEX.findall(win_list_str)]
    have_list: list[int] = [int(have_num_str) for have_num_str in NUMBER_REGEX.findall(have_list_str)]
    return (card_id, win_list, have_list)


def get_card_score(num_winning_numbers: int) -> int:
    if num_winning_numbers:
        return 2 ** (num_winning_numbers - 1)
    return 0


def count_winning_numbers(have_list: list[int], win_list: list[int]) -> int:
    num_winning_numbers: int = 0
    for have in have_list:
        num_winning_numbers = num_winning_numbers + (have in win_list)
    return num_winning_numbers


def get_cumulative_score(input_path: Path) -> int:
    cumulative_score: int = 0
    with open(input_path) as file:
        for line in file.readlines():
            card_id, win_list, have_list = get_card_info(line)
            num_winning_numbers: int = count_winning_numbers(have_list, win_list)
            card_score: int = get_card_score(num_winning_numbers)
            cumulative_score = cumulative_score + card_score
    return cumulative_score


def get_winnings_per_card(input_path: Path) -> dict[int, dict[str, int]]:
    winnings_per_card: dict[int, dict[str, int]] = {}
    with open(input_path) as file:
        for line in file.readlines():
            card_id, win_list, have_list = get_card_info(line)
            num_winning_numbers: int = count_winning_numbers(have_list, win_list)
            winnings_per_card[card_id] = {}
            winnings_per_card[card_id]["num_wins"] = num_winning_numbers
            winnings_per_card[card_id]["num_have"] = 1
    return winnings_per_card


def determine_copies_won(winnings_per_card: dict[int, dict[str, int]]) -> None:
    for card_id in winnings_per_card.keys():
        for won_card_id in range(card_id + 1, card_id + 1 + winnings_per_card[card_id]["num_wins"]):
            winnings_per_card[won_card_id]["num_have"] = winnings_per_card[won_card_id]["num_have"] + winnings_per_card[card_id]["num_have"]
    return


def count_total_number_of_cards(winnings_per_card: dict[int, dict[str, int]]) -> int:
    card_counter: int = 0
    for card_id in winnings_per_card.keys():
        card_counter = card_counter + winnings_per_card[card_id]["num_have"]
    return card_counter


if __name__ == "__main__":
    winnings_per_card: dict[int, dict[str, int]] = get_winnings_per_card(INPUT_PATH)
    determine_copies_won(winnings_per_card)
    print(count_total_number_of_cards(winnings_per_card))
