# Advent of code day 4, Ceres Search.
# https://adventofcode.com/2024/day/4

from icecream import ic

with open('test.txt', 'r') as file:
    ws_str = file.read()

ws = {}
y = 0
for line in ws_str.split('\n'):
    x = 0
    for c in line:
        ws[(x, y)] = c
        x += 1
    y += 1

ic(ws, x, y)

target = 'XMAS'
part1 = 0
mx, my = x, y
for y in range(my):
    for x in range(mx):
        ic(x, y)

        i = 0
        for ix, iy in [(-1, 0), (1, 0), (0, -1), (0, 1),        # N, S, W, E.
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]:     # The 4x diagonals.
            found = True

            for i in range(len(target)):                        # Check each character in the target.
                check = (x + ix * i, y + iy * i)
                if ws.get(check, '') != target[i]:
                    found = False
            if found:
                part1 += 1

ic(part1)
