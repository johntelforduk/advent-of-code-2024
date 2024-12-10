# Advent of code day 10, Hoof It.
# https://adventofcode.com/2024/day/10

from icecream import ic


def trailhead(topo: dict, x: int, y: int) -> int:
    height = topo[(x, y)]
    if height == 9:
        return 1

    count = 0
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        xn, xy = x + dx, y + dy
        if (xn, xy) in topo:
            if topo[(xn, xy)] == height + 1:
                count += trailhead(topo, xn, xy)

    return count


def trail_rating(topo: dict) -> int:
    total, progress = 0, 0
    for x, y in topo:
        if y > progress:
            progress = y
            ic(progress)

        if topo[(x, y)] == 0:
            total += trailhead(topo, x, y)
    return total


with open('input.txt', 'r') as file:
    topo_str = file.read()


topo = {}
y = 0
for line in topo_str.split('\n'):
    x = 0
    for height_str in line:
        if height_str != '.':
            topo[(x, y)] = int(height_str)
        x += 1
    y += 1

ic(trail_rating(topo))
