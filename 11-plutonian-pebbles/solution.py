# Advent of code day 11, Plutonian Pebbles.
# https://adventofcode.com/2024/day/11

from icecream import ic

with open('input.txt', 'r') as file:
    line_str = file.read()

stones = [(1, int(stone)) for stone in line_str.split()]
ic(stones)

for blink in range(25):
    new_stones = []
    for amount, engraving in stones:
        engraving_str = str(engraving)
            # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
        if engraving == 0:
            new_stones.append((amount, 1))

        elif (len(engraving_str) % 2) == 0:
            # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
            # The left half of the digits are engraved on the new left stone,
            # and the right half of the digits are engraved on the new right stone.
            l = int(len(engraving_str) / 2)
            a, b = int(engraving_str[:l]), int(engraving_str[l:])
            new_stones.append((amount, a))
            new_stones.append((amount, b))
        else:
            # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number
            # multiplied by 2024 is engraved on the new stone.
            new_stones.append((amount, 2024 * engraving))
    stones = new_stones.copy()
    ic(blink + 1, len(stones))
