import math
import re
from typing import List, Dict

from input_files.day4_input import day4_input_string

short_input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


input_string = day4_input_string


class Card:
    def __init__(self, card_id: int, winning_numbers: List[int], numbers: List[int]):
        self.card_id = card_id
        self.winning_numbers = winning_numbers
        self.numbers = numbers
        self.copies = 1

    def number_of_winning_numbers(self):
        return sum([1 for n in self.numbers if n in self.winning_numbers])

    def points(self):
        winning_numbers = self.number_of_winning_numbers()
        if winning_numbers == 0:
            return 0
        return 1 if winning_numbers == 1 else round(math.pow(2, winning_numbers - 1))

    def __repr__(self):
        return f"{self.card_id}: copies={self.copies}"


def build_cards():
    card_id_pattern = r"Card[ ]*(\d+)"
    numbers_pattern = r"(\d+)"
    cards: List[Card] = []
    for line in input_string.split("\n"):
        card_id = int(re.findall(card_id_pattern, line).pop())
        winning_numbers_string, numbers_string = line.split(": ")[1].split("|")
        winning_numbers = [int(wn) for wn in (re.findall(numbers_pattern, winning_numbers_string))]
        numbers = [int(n) for n in (re.findall(numbers_pattern, numbers_string))]
        cards.append(Card(card_id, winning_numbers, numbers))
    return cards


def part1():
    built_cards = build_cards()
    return sum([c.points() for c in built_cards])


def part2():
    built_cards = build_cards()
    for idx, card in enumerate(built_cards):
        matching_numbers = card.number_of_winning_numbers()
        for n in range(0, card.copies):
            for x in range(1, matching_numbers + 1):
                card_to_copy_index = idx + x
                if card_to_copy_index <= len(built_cards):
                    built_cards[card_to_copy_index].copies += 1
        pass
    return sum([card.copies for card in built_cards])


print(part1())
print(part2())
