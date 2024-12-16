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


def adjecent(tiles: dict) -> bool:
    for x, y in tiles:
        neighbors = 0
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                if (x + dx, y + dy) in tiles:
                    neighbors += 1
        if neighbors == 9:
            return True
    return False


robots = []
for line in robots_str.split('\n'):
    p_str, v_str = line.split(' ')
    x, y = [int(p.replace('p=', '')) for p in p_str.split(',')]
    vx, vy = [int(v.replace('v=', '')) for v in v_str.split(',')]

    robot = {'x': x, 'y': y, 'vx': vx, 'vy': vy}
    robots.append(robot)

tiles = count(robots)
w, h = 101, 103

i = 0
tree = False
while not tree :
    i += 1
    if i % 100 == 0:
        ic(i)

    new_robots = []
    for r in robots:
        x = (r['x'] + r['vx']) % w
        y = (r['y'] + r['vy']) % h
        nr = {'x': x, 'y': y, 'vx': r['vx'], 'vy': r['vy']}
        new_robots.append(nr)
    robots = new_robots

    tiles = count(robots)
    if adjecent(tiles):
        print(i)
        render(tiles=tiles, width=w, height=h)
        tree = True
