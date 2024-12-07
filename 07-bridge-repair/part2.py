# Advent of code day 7, Bridge Repair.
# https://adventofcode.com/2024/day/7

from icecream import ic


def solvable(target: int, so_far, terms: list, bread: str, start: bool) -> bool:
    if not terms:
        if target == so_far:
            ic(target, bread)
            return True
        else:
            return False

    new_terms = terms.copy()
    next_term = new_terms.pop(0)
    success = False
    if start:
        available_ops = '+'
    else:
        available_ops = '+*|'

    for op in available_ops:
        if op in '+*':
            new = eval(f'{so_far} {op} {next_term}')

        else:
            assert op == '|'
            new = int(f'{so_far}{next_term}')

        new_bread = bread + f' {op} {next_term}'
        if solvable(target=target, so_far=new, terms=new_terms, bread=new_bread, start=False):
            success = True

    if success:
        return True
    return False


with open('input.txt', 'r') as file:
    operators = file.read()

part2 = 0
for line in operators.split('\n'):
    target_str, terms_str = line.split(': ')
    target = int(target_str)
    terms = [int(t) for t in terms_str.split(' ')]
    if solvable(target=target, so_far=0, terms=terms, bread='', start=True):
        part2 += target
        ic(part2, target, terms)

ic(part2)
