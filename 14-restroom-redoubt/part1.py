# Advent of code day 14, Restroom Redoubt.
# https://adventofcode.com/2024/day/14

from icecream import ic

with open('input.txt', 'r') as file:
    robots_str = file.read()


def render(tiles: dict, width: int, height: int):
    for y in range(height):
        for x in range(width):
            if (x, y) not in tiles:
                print('.', end='')
            else:
                print(tiles[(x, y)], end='')
        print()
    print()


def count(robots: list) -> dict:
    tiles = {}
    for r in robots:
        x, y = r['x'], r['y']
        if (x, y) not in tiles:
            tiles[(x, y)] = 1
        else:
            tiles[(x, y)] += 1
    return tiles


def quadrant(x: int, y:int, width: int, height: int) -> tuple | None:
    x_mid = int(width / 2)
    y_mid = int(height / 2)
    if x == x_mid or y == y_mid:
        return None
    left, top = x < x_mid, y < y_mid
    return left, top

robots = []
for line in robots_str.split('\n'):
    p_str, v_str = line.split(' ')
    x, y = [int(p.replace('p=', '')) for p in p_str.split(',')]
    vx, vy = [int(v.replace('v=', '')) for v in v_str.split(',')]

    robot = {'x': x, 'y': y, 'vx': vx, 'vy': vy}
    robots.append(robot)

# ic(robots)
tiles = count(robots)
# ic(c)
w, h = 101, 103
render(tiles=tiles, width=w, height=h)

for i in range(100):
    new_robots = []
    for r in robots:
        x = (r['x'] + r['vx']) % w
        y = (r['y'] + r['vy']) % h
        nr = {'x': x, 'y': y, 'vx': r['vx'], 'vy': r['vy']}
        new_robots.append(nr)
    robots = new_robots

tiles = count(robots)
render(tiles=tiles, width=w, height=h)

quads = {}
for x, y in tiles:
    q = quadrant(x=x, y=y, width=w, height=h)
    if q is not None:
        if q not in quads:
            quads[q] = tiles[(x, y)]
        else:
            quads[q] += tiles[(x, y)]
ic(quads)

total = 1
for q in quads:
    total *= quads[q]
ic(total)
