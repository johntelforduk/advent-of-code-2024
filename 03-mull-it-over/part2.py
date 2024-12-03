# Advent of code day 3, Mull It Over.
# https://adventofcode.com/2024/day/3

from icecream import ic
import re

with open('input.txt', 'r') as file:
    memory = file.read()

total = 0
do = True
matches = [(m.group()) for m in re.finditer(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", memory)]
ic(matches)

for i in matches:
    ic(i)
    if i == "do()":
        do = True
    elif i == "don't()":
        do = False
    elif do:
        ic(do, i)

        terms = re.findall(r'\d+', i)
        x = 1
        for t in terms:
            x *= int(t)
        total += x

ic(total)
