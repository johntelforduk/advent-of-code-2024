# Advent of code day 9, Disk Fragmenter.
# https://adventofcode.com/2024/day/9

from icecream import ic


def checksum(files: dict) -> int:
    total = 0
    for file_pos in sorted(files):
        file_id, file_size = files[file_pos]

        for i in range(file_size):
            total += file_id * (file_pos + i)
    return total


with open('input.txt', 'r') as file:
    disk_map = file.read()

files, free = {}, {}

file_id, position = 0, 0
file_length = True
for block_value_str in disk_map:
    block_value = int(block_value_str)

    if file_length:                                     # Digit indicates the length of a file.
        files[position] = (file_id, block_value)
        file_id += 1
    else:                                                   # Digit indicates the length of free space.
        if block_value != 0:
            free[position] = block_value
    position += block_value

    file_length = not file_length                       # Alternate.


def first_gap(required_size: int, curr_pos: int, frees: dict) -> int | None:
    for free in sorted(frees):
        if free >= curr_pos:                            # Free space must be to the left of current file position.
            return None
        if required_size <= frees[free]:
            return free
    return None


def defrag(files, frees):
    files_copy = files.copy()
    for file_pos in sorted(files_copy, reverse=True):
        file_id, file_size = files[file_pos]
        fg = first_gap(required_size=file_size, curr_pos=file_pos, frees=frees)
        ic(file_pos)
        if fg is not None:                              # File is move-able.
            files[fg] = files[file_pos]                 # Copy the file to its new location.
            del files[file_pos]                         # Remove the file from its old location.

            if file_size == frees[fg]:                  # File entirely fills the free gap.
                del frees[fg]
            else:
                new_size = frees[fg] - file_size        # Reduce size of the free gap.
                frees[fg + file_size] = new_size
                del frees[fg]


defrag(files, free)
ic(checksum(files))
