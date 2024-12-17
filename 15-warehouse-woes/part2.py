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


def tree_of_boxes(wh, rx, ry, dy) -> dict:
    """For parm (x, y) location and vertical direction of travel (-1 or 1),
    return a set of locations that want to move in that direction if pushed."""

    # We've reached either a wall or a space. Either way, it the end of the search.
    if wh[rx, ry] not in '[]':
        return {}
    pass

    new_boxes = {}
    new_boxes[(rx, ry)] = wh[(rx, ry)]    # Current position must be a part of a box.
    new_boxes.update(tree_of_boxes(wh, rx, ry + dy, dy))  # Search onward from this part of the box.

    # Search onwards from other part of box.
    if wh[rx, ry] == '[':
        new_boxes[(rx + 1, ry)] = wh[(rx + 1, ry)]
        new_boxes.update(tree_of_boxes(wh, rx + 1, ry + dy, dy))
    else:                               # Must be a ']' part of box.
        new_boxes[(rx - 1, ry)] = wh[(rx - 1, ry)]
        new_boxes.update(tree_of_boxes(wh, rx - 1, ry + dy, dy))

    return new_boxes


def pushable(wh:dict, tree:dict, dy: int) -> bool:
    """For parm set that contains a connected tree of boxes, and parm direction of travel (-1 or 1),
     return True if it can be moved 1 space in that direction, otherwise return False."""
    min_max = {}
    for x, y in tree:
        if x not in min_max:
            min_max[x] = y
        else:
            if dy == -1:
                min_max[x] = min(min_max[x], y)
            else:
                min_max[x] = max(min_max[x], y)

    for x in min_max:
        if wh[(x, min_max[x] + dy)] != '.':
            return False
    return True


def push_vertical(wh:dict, tree:dict, dy: int) -> bool:
    """For parm set that contains a connected tree of boxes, and parm direction of travel (-1 or 1),
    move the boxes 1 space in that direction."""

    # Everywhere the tree used to be becomes space.
    for x, y in tree:
        wh[(x, y)] = '.'

    # Now put the tree in its new position.
    for x, y in tree:
        wh[(x, y + dy)] = tree[(x, y)]


def blocked(wh, rx, ry, dx, dy) -> bool:
    """Blocked if there are zero '.' between the robot and path to wall."""
    while wh[(rx, ry)] != '#':
        rx += dx
        ry += dy
        if wh[(rx, ry)] == '.':     # Found (at least) 1x gap, so robot is not blocked.
            return False
    return True                     # We reached a wall without finding a ',' so robot is blocked.


def gps_calc(wh: dict) -> int:
    total = 0
    for x, y in wh:
        if wh[(x, y)] == '[':
            total += x + 100 * y
    return total


def push_horizontal(wh:dict, rx, ry, dx: int) -> bool:
    # Look for space at end of this row.
    if blocked(wh, rx, ry, dx, 0):
        return False            # Robot not able to move.

    boxes = {}
    x = rx + dx
    while wh[(x, ry)] not in '.#':
        boxes[(x, ry)] = wh[(x, ry)]
        x += dx

    # ic(boxes)

    # Everywhere the boxes used to be becomes space.
    for x, y in boxes:
        wh[(x, y)] = '.'

    # Now put the boxes in their new positions.
    for x, y in boxes:
        wh[(x + dx, y)] = boxes[(x, y)]

    return True             # Robot able to move.


with open('input.txt', 'r') as file:
    input_str = file.read()

warehouse_str, moves_str = input_str.split('\n\n')

wh = {}
my = 0
for line in warehouse_str.split('\n'):
    mx = 0
    for tile in line:
        if tile == '#':
            wh[(mx, my)] = '#'
            wh[(mx + 1, my)] = '#'
        elif tile == 'O':
            wh[(mx, my)] = '['
            wh[(mx + 1, my)] = ']'
        else:
            wh[(mx, my)] = '.'
            wh[(mx + 1, my)] = '.'
        if tile == '@':
            rx, ry = mx, my

        mx += 2
    my += 1


render(wh, rx, ry, mx, my)

deltas = {'>': (1, 0), 'v': (0, 1), '<': (-1, 0), '^': (0, -1)}
for m in moves_str.replace('\n', ''):
    dx, dy = deltas[m]

    if wh[(rx + dx, ry + dy)] == '.':   # Move into space.
        rx += dx
        ry += dy
    elif wh[(rx + dx, ry + dy)] == '#': # Hit a wall.
        pass
    else:
        if dx != 0:           # Horizontal move.
            if push_horizontal(wh, rx, ry, dx):
                rx += dx
        else:                   # Vertical move.

            tree = tree_of_boxes(wh, rx, ry + dy, dy)
            # ic(tree)
            if pushable(wh,tree, dy):
                push_vertical(wh, tree, dy)
                ry += dy

    print(m, end='')

print()
render(wh, rx, ry, mx, my)
ic(gps_calc(wh))

#     if not blocked(wh, rx, ry, dx, dy):
#         push(wh, rx, ry, dx, dy)
#         rx += dx
#         ry += dy
#     print(m, end='')
#
# render(wh, rx, ry, mx, my)
# ic(gps_calc(wh))







# rx, ry = 8, 4
# dy = -1
# render(wh, rx, ry, mx, my)
# ic(rx, ry, dy)
#
# tree = tree_of_boxes(wh, rx, ry + dy, dy)
# ic(tree)
# ic(pushable(wh,tree, dy))
#
# push_vertical(wh, tree, dy)
# render(wh, rx, ry, mx, my)
#
#
# push_horizontal(wh,rx,ry, -1)
# render(wh, rx, ry, mx, my)
#
# rx, ry = 5, 5
# render(wh, rx, ry, mx, my)
# tree = tree_of_boxes(wh, rx, ry + dy, dy)
# ic(pushable(wh,tree, dy))
# push_vertical(wh, tree, dy)
# render(wh, rx, ry, mx, my)
#
