from input_files.day3_input import day_3_input_string
from typing import Optional, List


short_input_string = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

input_string = day_3_input_string

min_pos = 0
max_pos = len(input_string) - 1


def valid_pos(pos: int):
    return min_pos <= pos <= max_pos


def calc(number_adder):
    row_length = len(input_string.split("\n")[0])
    continuous_string = input_string.replace("\n", "")

    positions = {}
    current_str_number = ""
    current_str_number_start_pos: Optional[int] = None

    for idx, c in enumerate(continuous_string):
        if c.isdigit():
            current_str_number += c
            if current_str_number_start_pos is None:
                current_str_number_start_pos = idx
        else:
            if current_str_number:
                positions[range(current_str_number_start_pos, idx)] = current_str_number
            current_str_number = ""
            current_str_number_start_pos = None

    result: List[int] = []
    for idx, c in enumerate(continuous_string):
        if not c.isdigit() and c != ".":
            top_left = idx - row_length - 1
            top_middle = idx - row_length
            top_right = idx - row_length + 1
            same_left = idx - 1
            same_right = idx + 1
            bot_left = idx + row_length - 1
            bot_middle = idx + row_length
            bot_right = idx + row_length + 1
            to_check = [top_left, top_middle, top_right,
                        same_left, same_right,
                        bot_left, bot_middle, bot_right]
            valid_positions = [x for x in to_check if valid_pos(x)]
            numbers_pos = set()
            for valid_position_to_check in valid_positions:
                for key_range in positions:
                    if valid_position_to_check in key_range:
                        numbers_pos.add(key_range)

            if numbers_pos:
                result += number_adder(positions, numbers_pos, c)

    return sum(result)


def part1(positions, numbers_pos, c):
    return [int(positions[x]) for x in numbers_pos]


def part2(positions, numbers_pos, c):
    if len(numbers_pos) == 2 and c == "*":
        return [int(positions[numbers_pos.pop()]) * int(positions[numbers_pos.pop()])]
    else:
        return [0]


print(calc(part1))
print(calc(part2))
