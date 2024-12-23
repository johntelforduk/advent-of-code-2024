# Advent of code day 19, Linen Layout.
# https://adventofcode.com/2024/day/19

from icecream import ic

from functools import lru_cache


@lru_cache(maxsize=None)
def matches(candidate: str) -> bool:
    if len(candidate) == 0:
        return True

    curr_patt_length = 0
    any_match = False
    for p in SORTED_PATTERNS:
        lp = len(p)
        if curr_patt_length != lp:
            front = candidate[:lp]
            back = candidate[lp:]
            curr_patt_length = lp

        if p == front:
            if matches(back):
                any_match = True
        if any_match:
            return True

    return False


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
        count += 1
    ic(design, m, count)
