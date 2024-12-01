# Advent of code day 1, part 2, Historian Hysteria.
# https://adventofcode.com/2024/day/1

from icecream import ic

with open('input.txt', 'r') as file:
    ids = file.read()

left = [int(line.split('   ')[0]) for line in ids.split('\n')]
right = [int(line.split('   ')[1]) for line in ids.split('\n')]

similarity = 0
for l in left:
    matches = len([r for r in right if r == l])
    similarity += l * matches

ic(similarity)
