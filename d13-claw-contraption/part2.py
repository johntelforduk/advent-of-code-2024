# Advent of code day 13, Claw Contraption.
# https://adventofcode.com/2024/day/13

from icecream import ic


def search_backwards(gamma_x, gamma_y, delta_x, delta_y, px: int, py:int, ) -> tuple | None:
    ta = gamma_x + gamma_y
    tb = delta_x + delta_y
    tp = px + py

    tries = ta * tb + 1

    gamma_presses = tp // ta            # Most possible presses of gamma.
    ic(gamma_presses)
    while gamma_presses >= 0 and tries > 0:
        delta_presses = (tp - gamma_presses * ta) // tb

        this_gamma = gamma_presses * gamma_x + delta_presses * delta_x
        this_delta = gamma_presses * gamma_y + delta_presses * delta_y

        ic(px, this_gamma, py, this_delta)

        if px == this_gamma and py == this_delta:
            return gamma_presses, delta_presses
        else:
            gamma_presses -= 1
        tries -= 1
    return None

def one_cost(a_presses, b_presses) -> int:
    return 3 * a_presses + b_presses

def cost(ax:int, ay:int, bx: int, by:int, px: int, py: int) -> int | None:
    # 94 * a + 22 * b = 8400
    # 22 * a + 67 * b = 5400
    #
    # 94 * a + 22 * a + 22 * b + 67 * b = 8400 + 5400
    # a(94 + 22) + b(22 + 67) = 8400 + 5400
    # a(128) + b(89) = 13800

    # tp = ta * a + tb * b


    # a_presses = tp // ta            # Most possible presses of A.
    #
    # found = False
    # while not found and a_presses > 0:
    #     b_presses = (tp - a_presses * ta) // tb
    #     if px == a_presses * ax + b_presses * bx and py == a_presses * ay + b_presses * by:
    #         found = True
    #     else:
    #         a_presses -= 1


    sb1 = search_backwards(ax,ay,bx, by,px, py)
    if sb1 is None:
        cost1 = None
    else:
        a_presses, b_presses = sb1
        cost1 = one_cost(a_presses, b_presses)

    sb2 = search_backwards(bx,by,ax, ay,px, py)
    if sb2 is None:
        cost2 = None
    else:
        b_presses, a_presses = sb2
        cost2 = one_cost(a_presses, b_presses)

    ic(sb1, sb2, cost1, cost2)

    if cost1 is None:
        return cost2
    elif cost2 is not None:
        return min(cost1, cost2)
    return cost1

    # return(min(a_presses, b_presses))


with open('input.txt', 'r') as file:
    machines_str = file.read()

total = 0
for machine in machines_str.split('\n\n'):
    for line in machine.split('\n'):
        type_str, terms_str = line.split(': ')
        # ic(type_str, terms_str)
        if type_str == 'Prize':
            px, py = [int(p.replace('X=', '').replace('Y=', ''))  + 10000000000000
                      for p in terms_str.split(', ')]
            # ic(type_str, px, py)
        else:
            x, y = [int(p.replace('X+', '').replace('Y+', '')) for p in terms_str.split(', ')]
            # ic(type_str, x, y)
            if type_str == 'Button A':
                ax, ay = x, y
            else:
                bx, by = x, y

    this_cost = cost(ax, ay,bx, by, px, py)

    if this_cost is not None:
        total += this_cost

ic(total)
