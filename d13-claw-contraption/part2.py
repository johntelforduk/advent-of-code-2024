# Advent of code day 13, Claw Contraption.
# https://adventofcode.com/2024/day/13

from icecream import ic
import sympy


def calculate(ax:int, ay:int, bx: int, by:int, px: int, py: int) -> tuple | None:
    a, b = sympy.symbols('a b', integer=True)

    equation1 = sympy.Eq(ax * a + bx * b, px)
    equation2 = sympy.Eq(ay * a + by * b, py)

    solutions = sympy.solve([equation1, equation2])
    if solutions == []:
        return None
    return solutions[a], solutions[b]


with open('input.txt', 'r') as file:
    machines_str = file.read()

total = 0
for machine in machines_str.split('\n\n'):
    for line in machine.split('\n'):
        type_str, terms_str = line.split(': ')
        if type_str == 'Prize':
            px, py = [int(p.replace('X=', '').replace('Y=', ''))
                      for p in terms_str.split(', ')]
        else:
            x, y = [int(p.replace('X+', '').replace('Y+', '')) for p in terms_str.split(', ')]
            if type_str == 'Button A':
                ax, ay = x, y
            else:
                bx, by = x, y

    solution = calculate(ax, ay, bx, by, px + 10000000000000, py + 10000000000000)
    ic(px, py, solution)
    if solution is not None:
        a, b = solution
        cost = a * 3 + b
        total += cost

ic(total)
