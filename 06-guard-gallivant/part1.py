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

ic(x, y, gx, gy, gd)

ic('start')
while (gx, gy) in lab:
    # render(lab, x, y, gx, gy, gd)

    visited.add((gx, gy))

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

ic(len(visited))
