import re

from enum import IntEnum, auto
from typing import List, Dict

from input_files.day7_input import day7_input_string


PART2_JOKER_RANK = 0
simple_input_string = """The author of Advent of Code, has specifically requested people to not include the input strings. So I won't."""


class HandType(IntEnum):
    FIVE_KIND = auto()
    FOUR_KIND = auto()
    FULL_HOUSE = auto()
    THREE_KIND = auto()
    TWO_PAIR = auto()
    ONE_PAIR = auto()
    HIGH_CARD = auto()


class Hand:
    def __init__(self, cards: str, bid: int):
        self.cards = cards
        self.bid = bid
        self.ranks: List[int] = []
        self._build_ranks()

    def _build_ranks(self):
        for card in self.cards:
            if card == "A":
                self.ranks.append(14)
            elif card == "K":
                self.ranks.append(13)
            elif card == "Q":
                self.ranks.append(12)
            elif card == "J":
                self.ranks.append(11)
            elif card == "T":
                self.ranks.append(10)
            else:
                self.ranks.append(int(card))

    def __repr__(self):
        return str(self.cards)


class HandPart2(Hand):
    def _build_ranks(self):
        for card in self.cards:
            if card == "A":
                self.ranks.append(14)
            elif card == "K":
                self.ranks.append(13)
            elif card == "Q":
                self.ranks.append(12)
            elif card == "J":
                self.ranks.append(PART2_JOKER_RANK)
            elif card == "T":
                self.ranks.append(10)
            else:
                self.ranks.append(int(card))


def sort_hands_by_strength(hands_to_sort: List[Hand]) -> List[Hand]:
    sorted_hands: List[Hand] = []
    while len(hands_to_sort):
        sort_candidate_hands = hands_to_sort
        for idx in range(0, 5):
            if len(hands_to_sort):
                strongest_rank = max(hand.ranks[idx] for hand in sort_candidate_hands)
                sort_candidate_hands = [hand for hand in sort_candidate_hands if hand.ranks[idx] == strongest_rank]
                ties = len(sort_candidate_hands)
                if ties == 1:
                    hands_to_sort.remove(sort_candidate_hands[0])
                    sorted_hands.append(sort_candidate_hands[0])
                    break
        else:
            raise Exception()

    return sorted_hands


def part1():
    def build_hands():
        hands: List[Hand] = []
        cards_patters = r"^.{5}"
        bid_pattern = r"\d+$"
        for line in day7_input_string.split("\n"):
            cards = re.findall(cards_patters, line)[0]
            bid = int(re.findall(bid_pattern, line)[0])
            hand = Hand(cards, bid)
            hands.append(hand)
        return hands

    def determine_hand_type(hand: Hand) -> HandType:
        hand_type: HandType
        set_ranks = set(hand.ranks)
        unique_ranks = len(set_ranks)
        if unique_ranks == 1:  # Only one rank is represented by the hand
            hand_type = HandType.FIVE_KIND
        elif unique_ranks == 4:  # Two of the cards share the same rank
            hand_type = HandType.ONE_PAIR
        elif unique_ranks == 2 or unique_ranks == 3:
            for rank in set_ranks:
                occurrences = hand.ranks.count(rank)
                if occurrences == 4:  # Four of the cards share the same rank
                    hand_type = HandType.FOUR_KIND
                    break
                elif (
                        occurrences == 3 or occurrences == 2) and unique_ranks == 2:  # Three of the cards share the same rank, and there are only two different ranks in the hand
                    hand_type = HandType.FULL_HOUSE
                    break
                elif occurrences == 3 and unique_ranks == 3:  # Three cards share the same rank, and there are three different ranks
                    hand_type = HandType.THREE_KIND
                    break
                elif occurrences == 2 and unique_ranks == 3:
                    hand_type = HandType.TWO_PAIR
                    break
                else:
                    continue
            else:
                raise Exception(f"Could not determine hand type for hand {hand}")
        else:  # None of the cards share the same rank
            hand_type = HandType.HIGH_CARD

        return hand_type

    def sort_hands_by_type(hands_to_sort: List[Hand]) -> Dict[HandType, List[Hand]]:
        hand_types = {
            HandType.FIVE_KIND: [],
            HandType.FOUR_KIND: [],
            HandType.FULL_HOUSE: [],
            HandType.THREE_KIND: [],
            HandType.TWO_PAIR: [],
            HandType.ONE_PAIR: [],
            HandType.HIGH_CARD: [],
        }

        for hand in hands_to_sort:
            hand_type = determine_hand_type(hand)
            if hand_type in hand_types:
                hand_types[hand_type].append(hand)

        return hand_types

    input_hands = build_hands()
    hands_sorted_by_type = sort_hands_by_type(input_hands)
    hands_sorted_by_type_and_strength = {}
    for sorted_hand_type, type_sorted_hands in hands_sorted_by_type.items():
        hands_sorted_by_strength = sort_hands_by_strength(type_sorted_hands)
        hands_sorted_by_type_and_strength[sorted_hand_type] = hands_sorted_by_strength

    total_winnings = 0
    bid_rank = len(input_hands)
    for type_sorted_hands in hands_sorted_by_type_and_strength.values():
        for sorted_hand in type_sorted_hands:
            total_winnings += sorted_hand.bid * bid_rank
            bid_rank -= 1
    return total_winnings


def part2():
    def build_hands():
        hands: List[HandPart2] = []
        cards_patters = r"^.{5}"
        bid_pattern = r"\d+$"
        for line in day7_input_string.split("\n"):
            cards = re.findall(cards_patters, line)[0]
            bid = int(re.findall(bid_pattern, line)[0])
            hand = HandPart2(cards, bid)
            hands.append(hand)
        return hands

    def determine_hand_type(hand: HandPart2) -> HandType:
        hand_type: HandType
        set_ranks = set(hand.ranks)
        unique_ranks = len(set_ranks)
        jokers_count = hand.ranks.count(0)

        if not jokers_count:
            if unique_ranks == 1:  # Only one rank is represented by the hand
                hand_type = HandType.FIVE_KIND
            elif unique_ranks == 4:  # Two of the cards share the same rank
                hand_type = HandType.ONE_PAIR
            elif unique_ranks == 2 or unique_ranks == 3:
                for rank in set_ranks:
                    occurrences = hand.ranks.count(rank)
                    if occurrences == 4:  # Four of the cards share the same rank
                        hand_type = HandType.FOUR_KIND
                        break
                    elif (
                            occurrences == 3 or occurrences == 2) and unique_ranks == 2:  # Three of the cards share the same rank, and there are only two different ranks in the hand
                        hand_type = HandType.FULL_HOUSE
                        break
                    elif occurrences == 3 and unique_ranks == 3:  # Three cards share the same rank, and there are three different ranks
                        hand_type = HandType.THREE_KIND
                        break
                    elif occurrences == 2 and unique_ranks == 3:
                        hand_type = HandType.TWO_PAIR
                        break
                    else:
                        continue
                else:
                    raise Exception(f"Could not determine hand type for hand {hand}")
            else:  # None of the cards share the same rank
                hand_type = HandType.HIGH_CARD
        else:
            if unique_ranks in [1, 2]:
                hand_type = HandType.FIVE_KIND
            elif unique_ranks == 3:
                if jokers_count in [2, 3]:
                    hand_type = HandType.FOUR_KIND
                else:  # Only 1 joker
                    if all(hand.ranks.count(card) == 2 for card in hand.ranks if card != PART2_JOKER_RANK):
                        hand_type = HandType.FULL_HOUSE
                    else:
                        hand_type = HandType.FOUR_KIND
            elif unique_ranks == 4:
                hand_type = HandType.THREE_KIND
            else:
                hand_type = HandType.ONE_PAIR

        return hand_type

    def sort_hands_by_type(hands_to_sort: List[HandPart2]) -> Dict[HandType, List[HandPart2]]:
        hand_types = {
            HandType.FIVE_KIND: [],
            HandType.FOUR_KIND: [],
            HandType.FULL_HOUSE: [],
            HandType.THREE_KIND: [],
            HandType.TWO_PAIR: [],
            HandType.ONE_PAIR: [],
            HandType.HIGH_CARD: [],
        }

        for hand in hands_to_sort:
            hand_type = determine_hand_type(hand)
            if hand_type in hand_types:
                hand_types[hand_type].append(hand)

        return hand_types

    input_hands = build_hands()
    hands_sorted_by_type = sort_hands_by_type(input_hands)
    hands_sorted_by_type_and_strength = {}
    for sorted_hand_type, type_sorted_hands in hands_sorted_by_type.items():
        hands_sorted_by_strength = sort_hands_by_strength(type_sorted_hands)
        print(sorted_hand_type.name, hands_sorted_by_strength)
        hands_sorted_by_type_and_strength[sorted_hand_type] = hands_sorted_by_strength

    total_winnings = 0
    bid_rank = len(input_hands)
    for type_sorted_hands in hands_sorted_by_type_and_strength.values():
        for sorted_hand in type_sorted_hands:
            total_winnings += sorted_hand.bid * bid_rank
            bid_rank -= 1
    return total_winnings


print(part1())
print(part2())
