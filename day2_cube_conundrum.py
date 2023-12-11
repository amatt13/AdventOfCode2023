from typing import List
import re

from input_files.day2_input import day_2_input_string

short_input_string = """The author of Advent of Code, has specifically requested people to not include the input strings. So I won't."""

input_string = day_2_input_string


class GamePull:
    def __init__(self, red=0, green=0, blue=0):
        self.red = red
        self.green = green
        self.blue = blue

    def __len__(self):
        return self.red + self.green + self.blue


class Game:
    def __init__(self, game_id: int, game_pulls: List[GamePull]):
        self.game_id = game_id
        self.game_pulls = game_pulls

    def game_was_possible(self):
        max_red = 12
        max_green = 13
        max_blue = 14
        return all(pull.red <= max_red and pull.green <= max_green and pull.blue <= max_blue for pull in self.game_pulls)

    def power(self):
        min_red = max(game_pull.red for game_pull in self.game_pulls if game_pull.red != 0)
        min_green = max(game_pull.green for game_pull in self.game_pulls if game_pull.green != 0)
        min_blue = max(game_pull.blue for game_pull in self.game_pulls if game_pull.blue != 0)
        return min_red * min_green * min_blue


def build_games():
    game_id_pattern = r"Game (\d+)"
    game_pull_pattern = r"([ \d\w,]+)"
    red_pattern = r"(\d+) red"
    green_pattern = r"(\d+) green"
    blue_pattern = r"(\d+) blue"

    games: List[Game] = []
    for line in input_string.split("\n"):
        game_id = int(re.findall(game_id_pattern, line).pop())
        game_pulls: List[GamePull] = []
        for grab in re.findall(game_pull_pattern, line.split(":")[1]):
            red_match = re.findall(red_pattern, grab)
            red = int(red_match.pop()) if red_match else 0

            green_match = re.findall(green_pattern, grab)
            green = int(green_match.pop()) if green_match else 0

            blue_match = re.findall(blue_pattern, grab)
            blue = int(blue_match.pop()) if blue_match else 0

            game_pulls.append(GamePull(red, green, blue))
        games.append(Game(game_id, game_pulls))

    return games


def part1():
    built_games = build_games()
    result = sum(game.game_id for game in built_games if game.game_was_possible())
    return result


def part2():
    built_games = build_games()
    result = sum(game.power() for game in built_games)
    return result


print(part1())
print(part2())
