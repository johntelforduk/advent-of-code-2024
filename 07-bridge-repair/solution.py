# Advent of code day 7, Bridge Repair.
# https://adventofcode.com/2024/day/7

from icecream import ic


def solvable(target: int, so_far, terms: list, bread: str) -> bool:
    # ic(target, so_far, terms)
    if not terms:
        if target == so_far:
            ic(target, bread)
            return True
        else:
            return False

    new_terms = terms.copy()
    next_term = new_terms.pop(0)
    success = False
    for op in '+*':
        new = eval(f'{so_far} {op} {next_term}')
        new_bread = bread + f' {op} {next_term}'
        # ic(op, next_term, new)

        if solvable(target, new, new_terms, new_bread):
            success = True

    if success:
        return True
    return False


with open('test.txt', 'r') as file:
    operators = file.read()

part1 = 0
for line in operators.split('\n'):
    target_str, terms_str = line.split(': ')
    target = int(target_str)
    terms = [int(t) for t in terms_str.split(' ')]
    if solvable(target, 0, terms, ''):
        part1 += target
        ic(part1, target, terms)

ic(part1)
# ic(solvable(3267, 0, [81, 40, 27]))

# ic(solvable(190, 0, [10, 19]))
