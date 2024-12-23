# Advent of code day 19, Linen Layout.
# https://adventofcode.com/2024/day/19

from icecream import ic
from functools import lru_cache


@lru_cache(maxsize=None)
def matches(candidate: str) -> int:
    if len(candidate) == 0:
        return 1

    curr_patt_length = 0
    match_count = 0
    for p in SORTED_PATTERNS:
        lp = len(p)
        if curr_patt_length != lp:
            front = candidate[:lp]
            back = candidate[lp:]
            curr_patt_length = lp

        if p == front:
            match_count += matches(back)

    return match_count


with open('input.txt', 'r') as file:
    patterns_str = file.read()

available_str, designs_str = patterns_str.split('\n\n')

patterns = [p for p in available_str.split(', ')]
SORTED_PATTERNS = sorted(patterns, key=len, reverse=True)
ic(patterns, SORTED_PATTERNS)

count = 0
for design in designs_str.split('\n'):
    m = matches(design)
    if m:
        count += m
    ic(design, m, count)
