# Advent of code day 4, Ceres Search.
# https://adventofcode.com/2024/day/4

from icecream import ic

with open('input.txt', 'r') as file:
    ws_str = file.read()

ws = {}
y = 0
for line in ws_str.split('\n'):
    x = 0
    for c in line:
        ws[(x, y)] = c
        x += 1
    y += 1

patterns = [{(-1, -1): 'M', (1, 1): 'S', (-1, 1): 'M', (1, -1): 'S'},
            {(-1, -1): 'S', (1, 1): 'M', (-1, 1): 'M', (1, -1): 'S'},
            {(-1, -1): 'M', (1, 1): 'S', (-1, 1): 'S', (1, -1): 'M'},
            {(-1, -1): 'S', (1, 1): 'M', (-1, 1): 'S', (1, -1): 'M'}]

part2 = 0
mx, my = x, y
for y in range(my):
    for x in range(mx):
        if ws[(x, y)] == 'A':
            for p in patterns:
                found = True

                for dx, dy in p:
                    check = (x + dx, y + dy)
                    if ws.get(check, '') != p[(dx, dy)]:
                        found = False
                if found:
                    part2 += 1

ic(part2)
