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


def section(tiles: dict, x, y, xd, yd) -> int:
    count = 0
    for xt, yt in tiles:
        if xt <= x + xd and yt <= y + xd and xt >= x and yt >= y:
            count += tiles[(xt, yt)]
    return count


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

i = 0
tree = False
while not tree :
    i += 1
    new_robots = []
    for r in robots:
        x = (r['x'] + r['vx']) % w
        y = (r['y'] + r['vy']) % h
        nr = {'x': x, 'y': y, 'vx': r['vx'], 'vy': r['vy']}
        new_robots.append(nr)
    robots = new_robots

    tiles = count(robots)

    quads = {}
    for x, y in tiles:
        q = quadrant(x=x, y=y, width=w, height=h)
        if q is not None:
            if q not in quads:
                quads[q] = tiles[(x, y)]
            else:
                quads[q] += tiles[(x, y)]

    nw, ne, sw, se = quads[True, True], quads[False, True], quads[True, False], quads[False, False]
    s = section(tiles=tiles, x=0, y=0, xd=10, yd=10)
    if nw == ne and sw == se and s == 0:
        ic(i, nw, ne, sw, se, s)
        render(tiles=tiles, width=w, height=h)

