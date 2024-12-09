# Advent of code day 9, Disk Fragmenter.
# https://adventofcode.com/2024/day/9

from icecream import ic
import itertools

def render(files: dict, free: dict):
    last = max(files)
    # ic(last)
    for i in range(last + 1):
        if i in files:
            print(files[i], end='')
        else:
            print('.', end='')
    print()


def contiguous(files: dict) -> bool:
    prev = None
    for x in sorted(files,reverse=True):
        # ic(x, prev)
        if prev is not None:
            gap = prev - x
            if gap != 1:
                return False
        prev = x

    return True


def checksum(files: dict) -> int:
    total = 0
    # ic(files)
    for i in files:
        total += i * files[i]
    return total


with open('input.txt', 'r') as file:
    disk_map = file.read()

# Dictionary of occupied blocks.
# Dictionary of free blocks.
files, free = {}, {}

file_id, position = 0, 0
file_length = True
for block_value_str in disk_map:
    # ic(position, block_value_str, file_length)
    block_value = int(block_value_str)

    if file_length:         # Digit indicates the length of a file.
        for i in range(block_value):
            files[position + i] = file_id
        file_id += 1
    else:                   # Digit indicates the length of free space.
        if block_value != 0:
            free[position] = block_value
    position += block_value

    file_length = not file_length           # Alternate.

# ic(files, free)

# render(files, free)

max_free = max(free)
def defrag(files, free):
    for free_start in free:
        ic(free_start, max_free)
        for i in range(free[free_start]):
            free_pos = free_start + i
            last_file_pos = max(files)
            # ic(free_pos, last_file_pos)
            files[free_pos] = files[last_file_pos]
            del files[last_file_pos]
            # render(files, free)
            # ic(files)
            if contiguous(files):
                return


defrag(files, free)
# ic(files)
# render(files, free)
ic(checksum(files))