import re
from typing import Final, Pattern
from pathlib import Path


INPUT_PATH: Final[Path] = Path(".\\d6wait_for_it\\input.txt")
NUMBER_REGEX: Final[Pattern] = re.compile(r"(\d+)")

v0: int = 0  # mm/s
a_c: int = 1  # mm/s/s


# Number of ways you can win
# Win if distance travelled longer than


# You win if your average velocity is greater than that of the current record
# Average velocity to beat = d_goal / t_goal
# Average velocity after press = (v0 * t_press + (v0 + a_c * t_press) * (t_goal - t_press))/t_goal
# v0 = 0, and a_c = 1 -> t_press - t_press^2 / t_goal
# Equate them, t_press - t_press^2 / t_goal =  d_goal / t_goal
# brign to one side t_press^2 - t_goal * t_press + d_goal. has the form (a * x**2 + b*x + c = 0)
# where a = 1, b = -t_goal, and c = d_goal
# fidn roots of a second order polynomial: x = (-b ± sqrt(b**2 - 4 * a * c)) / (2 * a)

def get_race_infos(input_path: Path) -> list[tuple[int, int]]:
    with open(input_path) as file:
        time_line: str = file.readline()
        distance_line: str = file.readline()
    times: list[int] = [int(time) for time in NUMBER_REGEX.findall(time_line)]
    distances: list[int] = [int(distance) for distance in NUMBER_REGEX.findall(distance_line)]
    return [(time, distance) for (time, distance) in zip(times, distances)]


def get_single_race_info(input_path: Path) -> tuple[int, int]:
    with open(input_path) as file:
        time_line: str = file.readline()
        distance_line: str = file.readline()
    time: int = int("".join(NUMBER_REGEX.findall(time_line)))
    distance: int = int("".join(NUMBER_REGEX.findall(distance_line)))
    return (time, distance)


def get_true_winning_presses(goal_time: int, goal_distance: int) -> tuple[int, int]:
    a: int = 1
    b: int = -goal_time
    c: float = goal_distance
    D: float = b ** 2 - 4 * a * c
    root1: float = (-b + D**0.5) / (2 * a)
    root2: float = (-b - D**0.5) / (2 * a)
    return (min(root1, root2), max(root1, root2))


def get_integer_winning_presses(true_winning_presses: tuple[float, float]) -> tuple[int, int]:
    return (true_winning_presses[0]//1+1, (true_winning_presses[1]-1e-6)//1)  # Yeayeah, fucking magic number :D


race_infos: list[tuple[int, int]] = get_race_infos(INPUT_PATH)
multiplication_of_margins: int = 1
for race_info in race_infos:
    true_winning_bracket = get_true_winning_presses(*race_info)
    int_winning_bracket = get_integer_winning_presses(true_winning_bracket)
    margin: int = int_winning_bracket[1] + 1 - int_winning_bracket[0]
    print(f"{true_winning_bracket} -> {int_winning_bracket} -> {margin}")
    multiplication_of_margins = multiplication_of_margins * margin
print(multiplication_of_margins)
print()

single_race_info: tuple[int, int] = get_single_race_info(INPUT_PATH)
true_winning_bracket = get_true_winning_presses(*single_race_info)
int_winning_bracket = get_integer_winning_presses(true_winning_bracket)
margin: int = int_winning_bracket[1] + 1 - int_winning_bracket[0]
print(f"{true_winning_bracket} -> {int_winning_bracket} -> {margin}")
