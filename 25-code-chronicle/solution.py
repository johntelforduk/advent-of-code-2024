# Advent of code day 25, Code Chronicle.
# https://adventofcode.com/2024/day/25

from icecream import ic


def match(lock: list, key: list) -> bool:
    for p1, p2 in zip(lock, key):
        if p1 + p2 > 5:
            return False
    return True


# Lock 0,5,3,4,3 and key 5,0,2,1,3: overlap in the last column.
assert not match([0,5,3,4,3], [5,0,2,1,3])

# Lock 0,5,3,4,3 and key 4,3,4,0,2: overlap in the second column.
assert not match([0,5,3,4,3], [4,3,4,0,2])

# Lock 0,5,3,4,3 and key 3,0,2,0,1: all columns fit!
assert match([0,5,3,4,3], [3,0,2,0,1])

# Lock 1,2,0,5,3 and key 5,0,2,1,3: overlap in the first column.
assert not match([1,2,0,5,3], [5,0,2,1,3])

# Lock 1,2,0,5,3 and key 4,3,4,0,2: all columns fit!
assert match([1,2,0,5,3], [4,3,4,0,2])

# Lock 1,2,0,5,3 and key 3,0,2,0,1: all columns fit!
assert match([1,2,0,5,3], [3,0,2,0,1])

with open('input.txt', 'r') as file:
    schematics_str = file.read()

keys, locks = [], []
for schematic in schematics_str.split('\n\n'):
    # ic(schematic)

    grid = set()
    count_top_row = 0
    for y, line in enumerate(schematic.split('\n')):
        # ic(y, line)
        for x, c in enumerate(line):
            # ic(x)
            if c == '#':
                grid.add((x, y))
                if y == 0:
                    count_top_row += 1      # If this ends up being 5, then this is a lock.
    # ic(grid, count_top_row)

    combo = []
    for x in range(5):
        x_count = 0
        for y in range(7):
            if (x, y) in grid:
                x_count += 1
        combo.append(x_count - 1)
    # ic(combo, count_top_row)

    if count_top_row == 5:
        locks.append(combo)
    else:
        keys.append(combo)

ic(locks)
ic(keys)

matches = 0
for l in locks:
    for k in keys:
        if match(l, k):
            matches += 1
ic(matches)
