# Advent of code day 11, Plutonian Pebbles.
# https://adventofcode.com/2024/day/11

from icecream import ic

with open('input.txt', 'r') as file:
    line_str = file.read()


def set_or_add(d: dict, k: int, a: int):
    if k not in d:
        d[k] = a
    else:
        d[k] += a


stones = {int(stone): 1 for stone in line_str.split()}
ic(stones)

for blink in range(75):
    new_stones = {}
    for engraving in stones:
        amount = stones[engraving]
        engraving_str = str(engraving)
        if engraving == 0:
            # If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
            set_or_add(new_stones, 1, amount)

        elif (len(engraving_str) % 2) == 0:
            # If the stone is engraved with a number that has an even number of digits, it is replaced by two stones.
            # The left half of the digits are engraved on the new left stone,
            # and the right half of the digits are engraved on the new right stone.
            l = int(len(engraving_str) / 2)
            a, b = int(engraving_str[:l]), int(engraving_str[l:])

            set_or_add(new_stones, a, amount)
            set_or_add(new_stones, b, amount)
        else:
            # If none of the other rules apply, the stone is replaced by a new stone; the old stone's number
            # multiplied by 2024 is engraved on the new stone.
            set_or_add(new_stones, 2024 * engraving, amount)

    stones = new_stones.copy()
    ic(blink + 1, len(stones))

total = 0
for engraving in stones:
    amount = stones[engraving]
    total += amount
ic(total)
