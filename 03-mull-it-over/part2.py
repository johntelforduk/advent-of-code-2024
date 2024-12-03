# Advent of code day 3, Mull It Over.
# https://adventofcode.com/2024/day/3

from icecream import ic
import re

with open('test.txt', 'r') as file:
    memory = file.read()

total = 0

matches = [(m.group(), m.start(), m.end()) for m in re.finditer(r'mul\(\d+,\d+\)', memory)]
ic(matches)


# for i in instructions:
#     ic(i)
#     terms = re.findall(r'\d+', i)
#     x = 1
#     for t in terms:
#         x *= int(t)
#     total += x

ic(total)
