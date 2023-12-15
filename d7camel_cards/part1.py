from typing import Final
from pathlib import Path
from enum import Enum

INPUT_PATH: Final[Path] = Path(".\\d7camel_cards\\input.txt")
TEST_HAND: Final[str] = "AQKKK"
TEST_HAND_2: Final[str] = "KKKKQ"

FACE_CARD_STRENGTH_MAP: Final[dict[str, int]] = {"T": 10,
                                                 "J": 11,
                                                 "Q": 12,
                                                 "K": 13,
                                                 "A": 14}


class HandType(list[int], Enum):
    HIGH_CARD = [1, 1, 1, 1, 1]
    ONE_PAIR = [2, 1, 1, 1]
    TWO_PAIR = [2, 2, 1]
    THREE_OF_A_KIND = [3, 1, 1]
    FULL_HOUSE = [3, 2]
    FOUR_OF_A_KIND = [4, 1]
    FIVE_OF_A_KIND = [5]


HAND_TYPE_STRENGTH_MAP: Final[dict[HandType, int]] = {HandType.HIGH_CARD.name: 1,
                                                      HandType.ONE_PAIR.name: 2,
                                                      HandType.TWO_PAIR.name: 3,
                                                      HandType.THREE_OF_A_KIND.name: 4,
                                                      HandType.FULL_HOUSE.name: 5,
                                                      HandType.FOUR_OF_A_KIND.name: 6,
                                                      HandType.FIVE_OF_A_KIND.name: 7}


def get_card_strength(card_str: str) -> int:
    return card_str if card_str.isnumeric() else FACE_CARD_STRENGTH_MAP[card_str]


def get_hand_strenght(hand_type: HandType) -> int:
    return HAND_TYPE_STRENGTH_MAP[hand_type.name]


def get_hand_code(hand_str: str) -> list[int]:
    hand_code: list[int] = []
    for card_str in set(hand_str):
        hand_code.append(hand_str.count(card_str))
    hand_code.sort(reverse=True)
    return hand_code


def get_hand_score(hand_str: str) -> float:
    hand_score_str: str = ""
    hand_code: list[int] = get_hand_code(hand_str)
    hand_type: HandType = get_hand_type(hand_code)
    hand_strength: int = get_hand_strenght(hand_type)
    hand_score_str = hand_score_str + pstr(hand_strength) + "."
    card_str: str
    for card_str in hand_str:
        card_score: int = get_card_strength(card_str)
        hand_score_str = hand_score_str + pstr(card_score)
    return float(hand_score_str)


def pstr(input, pad_to: int = 2):
    input_str: str = str(input)
    return "0"*(pad_to-len(str(input_str))) + input_str


def get_hand_type(hand_code: list[int]) -> HandType:
    return HandType(hand_code)


# def compare_handes(hand_1_str: str, hand_2_str: str) -> tuple[str, str]:
#     hand_1_strenght: int = get_hand_strenght(get_hand_type(get_hand_code(hand_1_str)))
#     hand_2_strength: int = get_hand_strenght(get_hand_type(get_hand_code(hand_2_str)))
#     if hand_1_strenght == hand_2_strength:
#         for idx in range(len(hand_1_str)):
#             if get_card_strength(hand_1_str[idx]) > get_card_strength(hand_2_str[idx]):
#                 return (hand_1_str, hand_2_str)
#             if get_card_strength(hand_2_str[idx]) > get_card_strength(hand_1_str[idx]):
#                 return (hand_2_str, hand_1_str)
#         return (hand_1_str, hand_2_str)  # Both hands are the exact same, return in original order
#     if hand_1_strenght > hand_2_strength:
#         return (hand_1_str, hand_2_str)
#     if hand_2_strength > hand_1_strenght:
#         return (hand_2_str, hand_1_str)
#     raise Exception


def get_hands_and_bids(input_path: Path) -> tuple[list[str], list[int]]:
    hands: list[str] = []
    bids: list[int] = []
    with open(input_path) as file:
        for line in file.readlines():
            hand, bid = line.split(" ")
            hands.append(hand)
            bids.append(int(bid))
    return hands, bids


def get_sorted_bids(hands: list[str], bids: list[int]):
    scores: list[float] = []
    for hand in hands:
        scores.append(get_hand_score(hand))
    bids = [bid for _, bid in sorted(zip(scores, bids))]
    return bids


def get_total_winnings(sorted_bids: list[int]) -> int:
    total_winnings: int = 0
    for idx in range(len(sorted_bids)):
        total_winnings = total_winnings + (idx + 1) * sorted_bids[idx]
    return total_winnings


if __name__ == "__main__":
    hands, bids = get_hands_and_bids(INPUT_PATH)
    bids = get_sorted_bids(hands, bids)
    print(get_total_winnings(bids))
