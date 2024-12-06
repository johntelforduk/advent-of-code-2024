# Advent of code day 6, Guard Gallivant.
# https://adventofcode.com/2024/day/6

from icecream import ic


def render(l, mx, my, gx, gy, gd):
    for ry in range(my):
        for rx in range(mx):
            if rx == gx and ry == gy:
                print(gd, end='')
            else:
                print(l[(rx, ry)], end='')
        print()
    print()


def loops(lab: dict, gx:int, gy: int, gd: str) -> bool:
    sx, sy, sd = gx, gy, gd             # Make a copy of the start state of the guard.

    visited = set()
    looping = False
    while (gx, gy) in lab and not looping:
        # render(lab, x, y, gx, gy, gd)
        if (gx, gy, gd) in visited:             # Guard has been here before.
            return True

        visited.add((gx, gy, gd))

        # Work out which direction the guard would normally go next.
        deltas = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}
        dx, dy = deltas[gd]

        if lab.get((gx + dx, gy + dy), '') == '#':      # Hit an obstacle.
            # Rotate to the right.
            rotate = {'^': '>', '>': 'v', 'v': '<', '<': '^'}
            gd = rotate[gd]
        else:
            # Move the guard.
            gx += dx
            gy += dy

    return False


with open('input.txt', 'r') as file:
    lab_str = file.read()


lab, y = {}, 0
visited = set()
for line in lab_str.split('\n'):
    x = 0
    for s in line:
        if s == '^':
            gx, gy, gd = x, y, s
            lab[(x, y)] = '.'
        else:
            lab[(x, y)] = s
        x += 1
    y += 1

tried = 0
part2 = 0
lab_copy = lab.copy()
for x, y in lab_copy:
    if (x != gx or y != gy) and lab[(x, y)] == '.':         # Don't put obstacle where Guard starts.
        lab[(x, y)] = '#'                                   # Put an obstacle.
        if loops(lab, gx, gy, gd):
            part2 += 1
        lab[(x, y)] = '.'                                   # Put the dot back.
    tried += 1
    ic(tried, part2)

ic(part2)
