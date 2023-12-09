class Race:
    def __init__(self, time, distance):
        self.time = time
        self.distance = distance

    def __repr__(self):
        return self.__dict__


part1_simple_races = [
    Race(time=7, distance=9),
    Race(time=15, distance=40),
    Race(time=30, distance=200),
]

part1_races = [
    Race(time=41, distance=214),
    Race(time=96, distance=1789),
    Race(time=88, distance=1127),
    Race(time=94, distance=1055),
]

part1_simple_race = Race(time=71530, distance=940200)
part2_race = Race(time=41968894, distance=214178911271055)


def calculate_distance_travelled(hold_time: int, race_time_limit: int) -> int:
    return (race_time_limit - hold_time) * hold_time


def part1():
    error_margins = []
    for race in part1_races:
        shortest_hold_time = 0
        longest_hold_time = race.time
        short_found = False
        long_found = False
        while shortest_hold_time < longest_hold_time and not (short_found and long_found):
            if not short_found:
                short_hold_distance = calculate_distance_travelled(shortest_hold_time, race.time)
                if short_hold_distance > race.distance:
                    short_found = True
                else:
                    shortest_hold_time += 1
            if not long_found:
                long_hold_distance = calculate_distance_travelled(longest_hold_time, race.time)
                if long_hold_distance > race.distance:
                    long_found = True
                else:
                    longest_hold_time -= 1
        margin = longest_hold_time - shortest_hold_time + 1
        error_margins.append(margin)
    res = 1
    for x in error_margins:
        res *= x
    return res


def part2():
    shortest_hold_time = 0
    longest_hold_time = part2_race.time
    short_found = False
    long_found = False
    while shortest_hold_time < longest_hold_time and not (short_found and long_found):
        if not short_found:
            short_hold_distance = calculate_distance_travelled(shortest_hold_time, part2_race.time)
            if short_hold_distance > part2_race.distance:
                short_found = True
            else:
                shortest_hold_time += 1
        if not long_found:
            long_hold_distance = calculate_distance_travelled(longest_hold_time, part2_race.time)
            if long_hold_distance > part2_race.distance:
                long_found = True
            else:
                longest_hold_time -= 1
    margin = longest_hold_time - shortest_hold_time + 1
    return margin


print(part1())
print(part2())
