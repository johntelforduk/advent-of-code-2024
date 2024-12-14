# Advent of code day 13, Claw Contraption.
# https://adventofcode.com/2024/day/13

from icecream import ic


def cost(ax:int, ay:int, bx: int, by:int, px: int, py: int) -> None|int:
    most_a = max(px // ax, py // ay) + 2
    most_b = max(px // bx, py // by) + 2

    best = None
    for a in range(most_a):
        for b in range(most_b):
            if a * ax + b * bx == px and a * ay + b * by == py:
                this_cost = 3 * a + b
                if best is None or this_cost < best:
                    best = this_cost
    return best


with open('input.txt', 'r') as file:
    machines_str = file.read()

total = 0
for machine in machines_str.split('\n\n'):
    for line in machine.split('\n'):
        type_str, terms_str = line.split(': ')
        # ic(type_str, terms_str)
        if type_str == 'Prize':
            px, py = [int(p.replace('X=', '').replace('Y=', '')) for p in terms_str.split(', ')]
            ic(type_str, px, py)
        else:
            x, y = [int(p.replace('X+', '').replace('Y+', '')) for p in terms_str.split(', ')]
            ic(type_str, x, y)
            if type_str == 'Button A':
                ax, ay = x, y
            else:
                bx, by = x, y

    this_cost = cost(ax, ay,bx, by, px, py)
    ic(this_cost)
    if this_cost is not None:
        total += this_cost

ic(total)
