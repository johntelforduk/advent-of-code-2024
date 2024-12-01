# Advent of code day 1, part 1, Historian Hysteria.
# https://adventofcode.com/2024/day/1

from icecream import ic

with open('input.txt', 'r') as file:
    ids = file.read()

left = sorted([int(line.split('   ')[0]) for line in ids.split('\n')])
right = sorted([int(line.split('   ')[1]) for line in ids.split('\n')])

total_dist = 0
for l, r in zip(left, right):
    total_dist += abs(l - r)

ic(total_dist)
