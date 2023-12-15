from typing import Final

FILE_NAME: Final[str] = ".\\trebuchet\\input.txt"
TEST_FILE_NAME: Final[str] = ".\\trebuchet\\test_input_p2.txt"
TEST_STRING: Final[str] = "1z\n"

NUM_DICT: Final[dict[str, str]] = {"one": "1",
                                   "two": "2",
                                   "three": "3",
                                   "four": "4",
                                   "five": "5",
                                   "six": "6",
                                   "seven": "7",
                                   "eight": "8",
                                   "nine": "9",
                                   "1": "1",
                                   "2": "2",
                                   "3": "3",
                                   "4": "4",
                                   "5": "5",
                                   "6": "6",
                                   "7": "7",
                                   "8": "8",
                                   "9": "9"
                                   }


def get_first_last_numeric(input_str: str) -> tuple[str, str]:
    # Who needs regex when you have dictionaries!
    first_numeric_index: int = float('inf')
    first_numeric: str = None
    last_numeric_index: int = -float('inf')
    last_numeric: str = None
    for key in list(NUM_DICT.keys()):
        key_index: int = None
        for _ in range(input_str.count(key)):
            key_index = input_str.index(key, key_index)
            if key_index < first_numeric_index:
                first_numeric_index = key_index
                first_numeric = NUM_DICT[key]
            if key_index > last_numeric_index:
                last_numeric_index = key_index
                last_numeric = NUM_DICT[key]
            key_index = key_index + 1
    return (first_numeric, last_numeric)


def combine_numerics(a: str, b: str) -> int:
    return int(a + b)


def get_calibration_value(input_str: str) -> int:
    first_last_numeric: tuple[str, str] = get_first_last_numeric(input_str.lower())
    return combine_numerics(*first_last_numeric)


def get_sum_calibration_values(input_file_name: str) -> int:
    sum_of_calibration_values: int = 0
    with open(input_file_name) as file:
        line: str
        for line in file.readlines():
            print(line[:-1], end=" ")
            calibration_value: int = get_calibration_value(line)
            print(calibration_value)
            sum_of_calibration_values = sum_of_calibration_values + calibration_value
    return sum_of_calibration_values


if __name__ == "__main__":
    print(get_sum_calibration_values(FILE_NAME))


# Old shit
# REGEX: Final[Pattern] = re.compile(r'\d')

# def replace_words_by_numbers(input_str: str) -> str:
#     str_contains_matching_key: bool = True
#     while str_contains_matching_key:
#         str_contains_matching_key = False
#         matched_keys: list[str] = []
#         indeces: list[int] = []
#         for key in WORD_TO_NUM_DICT.keys():
#             if key in input_str:
#                 str_contains_matching_key = True
#                 matched_keys.append(key)
#                 indeces.append(input_str.index(key))
#         if str_contains_matching_key:
#             replacement_key: str = sorted(zip(indeces, matched_keys))[0][1]
#             input_str = input_str.replace(replacement_key, WORD_TO_NUM_DICT[replacement_key])
#     return input_str


# def find_all_numerics(input_str) -> list[str]:
#     mps: list[str] = REGEX.findall(input_str)
#     return mps


# def get_first_last_numeric(list_of_nums: list[str]) -> tuple[str, str]:
#     if len(list_of_nums) == 1:
#         list_of_nums.append(list_of_nums[0])
#     return (list_of_nums[0], list_of_nums[-1])
