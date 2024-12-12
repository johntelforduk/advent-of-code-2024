# Advent of code day 8, Resonant Collinearity.
# https://adventofcode.com/2024/day/8

from icecream import ic
import itertools

with open('input.txt', 'r') as file:
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

antinodes = set()
for frequency in antennas:
    locations = antennas[frequency]

    if len(locations) > 1:                          # Part 2: some antennas are now also antinodes.
        antinodes.update(locations)

    for loc1, loc2 in itertools.combinations(locations, 2):
        x1, y1 = loc1
        x2, y2 = loc2
        xd = x2 - x1                                # Calculate deltas.
        yd = y2 - y1

        ic(loc1, loc2, xd, yd)

        in_range = True
        factor = 1
        while in_range:
            candidates = [(x1 - factor * xd, y1 - factor * yd)]
            candidates.append((x2 + factor * xd, y2 + factor * yd))
            ic(frequency, loc1, loc2, xd, yd, candidates)
            in_range = False
            for x, y in candidates:                 # Check if candidates are in range of the map.
                if x >= 0 and x < mx and y >= 0 and y < my:
                    antinodes.add((x, y))
                    in_range = True
            factor += 1

ic(len(antinodes))