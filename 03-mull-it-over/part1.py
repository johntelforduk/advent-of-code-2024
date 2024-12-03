# Advent of code day 3, Mull It Over.
# https://adventofcode.com/2024/day/3

from icecream import ic
import re

with open('input.txt', 'r') as file:
    memory = file.read()

total = 0
instructions = re.findall(r'mul\(\d+,\d+\)', memory)
for i in instructions:
    ic(i)
    terms = re.findall(r'\d+', i)
    x = 1
    for t in terms:
        x *= int(t)
    total += x

ic(total)
