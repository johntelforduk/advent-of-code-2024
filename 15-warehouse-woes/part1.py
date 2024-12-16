# Advent of code day 15, Warehouse Woes.
# https://adventofcode.com/2024/day/15

from icecream import ic


def render(wh: dict, rx: int, ry: int, mx: int, my: int):
    for y in range(my):
        for x in range(mx):
            if x == rx and y == ry:
                print('@', end='')
            else:
                print(wh[(x, y)], end='')
        print()
    print()



def blocked(wh, rx, ry, dx, dy) -> bool:
    """Blocked if there are zero '.' between the robot and path to wall."""
    while wh[(rx, ry)] != '#':
        rx += dx
        ry += dy
        if wh[(rx, ry)] == '.':     # Found (at least) 1x gap, so robot is not blocked.
            return False
    return True                     # We reached a wall without finding a ',' so robot is blocked.


def push(wh, rx, ry, dx, dy):
    space_found = False
    nx, ny = rx, ry
    while not space_found:
        nx += dx
        ny += dy
        if wh[(nx, ny)] == '.':
            space_found = True
            wh[(nx, ny)] = 'O'

    wh[(rx + dx, ry + dy)] = '.'


def gps_calc(wh: dict) -> int:
    total = 0
    for x, y in wh:
        if wh[(x, y)] == 'O':
            total += x + 100 * y
    return total


with open('input.txt', 'r') as file:
    input_str = file.read()

warehouse_str, moves_str = input_str.split('\n\n')

wh = {}
my = 0
for line in warehouse_str.split('\n'):
    mx = 0
    for tile in line:
        if tile == '@':
            rx, ry = mx, my
            wh[(mx, my)] = '.'
        else:
            wh[(mx, my)] = tile
        mx += 1
    my += 1

render(wh, rx, ry, mx, my)

deltas = {'>': (1, 0), 'v': (0, 1), '<': (-1, 0), '^': (0, -1)}
for m in moves_str.replace('\n', ''):
    dx, dy = deltas[m]

    if not blocked(wh, rx, ry, dx, dy):
        push(wh, rx, ry, dx, dy)
        rx += dx
        ry += dy
    print(m, end='')

render(wh, rx, ry, mx, my)
ic(gps_calc(wh))
