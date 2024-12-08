# Advent of code day 8, Resonant Collinearity.
# https://adventofcode.com/2024/day/8

from icecream import ic
import itertools


def distance(v1: tuple, v2: tuple) -> int:
    x1, y1 = v1
    x2, y2 = v2
    return abs(x1 - x2) + abs(y1 - y2)


assert distance((4,3), (5, 5)) == 3


with open('test1.txt', 'r') as file:
    antennas_str = file.read()

my = 0
antennas = {}
for line in antennas_str.split('\n'):
    mx = 0
    for frequency in line:
        if frequency not in '.#':
            if frequency not in antennas:
                antennas[frequency] = [(mx, my)]
            else:
                antennas[frequency].append((mx, my))
        mx += 1
    my += 1

ic(antennas, mx, my)


# distances = {}


for y in range(my):             # Look at every square on the grid.
    for x in range(mx):
        for frequency in antennas:
            # For each antenna, work out how far each square is from it.

            distances = [distance((x, y), antenna) for antenna in antennas[frequency]]

            # Check pairs of distances to see if one of them matches the rule.

            ic(x, y, frequency, distances)
            for d1, d2 in itertools.combinations(distances, 2):
                if d1 * 2 == d2 or d2 * 2 == d1:
                    ic(x, y, frequency, d1, d2)
