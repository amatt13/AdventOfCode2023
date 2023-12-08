from input_files.day1_input import day_1_input_string

short_input_string = """twoonetwo
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen"""


input_string = day_1_input_string


def part_one():
    lines = input_string.split("\n")
    all_line_numbers = []
    for line in lines:
        numbers = [c for c in line if c.isdigit()]
        first = numbers[0]
        last = numbers[-1]
        combined = first + last
        all_line_numbers.append(combined)

    return sum(int(n) for n in all_line_numbers)


def part_one_super_short():
    return sum(int(n) for n in [[c for c in line if c.isdigit()][0] + [c for c in line if c.isdigit()][-1] for line in input_string.split("\n")])


def part_two():
    lines = input_string.split("\n")
    all_line_numbers = []
    string_numbers = [("one", "1"), ("two", "2"), ("three", "3"), ("four", "4"), ("five", "5"), ("six", "6"), ("seven", "7"), ("eight", "8"), ("nine", "9")]

    for line in lines:
        line = line.lower()

        digit_numbers = [(idx, c) for idx, c in enumerate(line) if c.isdigit()]
        first_digit: tuple[int, str] = digit_numbers[0] if len(digit_numbers) else (999, "")
        last_digit: tuple[int, str] = digit_numbers[-1] if len(digit_numbers) else (-1, "")

        first_strings = [(line.find(sn[0]), sn[1]) for sn in string_numbers if sn[0] in line]
        last_strings = [(line.rfind(sn[0]), sn[1]) for sn in string_numbers if sn[0] in line]

        first_strings.sort(key=lambda x: x[0])
        last_strings.sort(key=lambda x: x[0], reverse=True)

        first_string = first_strings[0] if len(first_strings) else (999, "")
        last_string = last_strings[0] if len(last_strings) else (-1, "")

        first = first_digit[1] if first_digit[0] < first_string[0] else first_string[1]
        last = last_digit[1] if last_digit[0] > last_string[0] else last_string[1]
        combined = first + last
        all_line_numbers.append(combined)

    return sum(int(n) for n in all_line_numbers)


def replace_test():
    """
    Does not work as a letter can belong to two numbers.

    Fx "eightwothree" here the first letters "eightwo" can both be "eight" and "two" where the "t" is a part of both numbers
    Replacing the t in the above example ruins the other number
    """
    all_line_numbers = []
    string_numbers = [("one", "1"), ("two", "2"), ("three", "3"), ("four", "4"), ("five", "5"), ("six", "6"), ("seven", "7"), ("eight", "8"), ("nine", "9")]
    for line in short_input_string.split("\n"):
        print(line)
        for sn in string_numbers:
            line = line.replace(sn[0], sn[1])
        print(line)
        numbers = [c for c in line if c.isdigit()]
        first = numbers[0]
        last = numbers[-1]
        combined = first + last
        all_line_numbers.append(combined)

    return sum(int(n) for n in all_line_numbers)


print(part_one())
print(part_two())
