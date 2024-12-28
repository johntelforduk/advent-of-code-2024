# Advent of code day 24, Crossed Wires.
# https://adventofcode.com/2024/day/24

from icecream import ic

def ready(wires: dict, gates: list) -> list:
    """Return list of gates that are ready to be evaluated."""
    output = []
    for i1, operator, i2, out in gates:
        # ic(i1, operator, i2, out)
        if wires[i1] is not None and wires[i2] is not None and wires[out] is None:
            output.append((i1, operator, i2, out))
    return output


def result(wires: dict) -> int | None:
    """Using the wires with names that begin with zed, work out denary result."""
    output = 0

    power = 0
    for wire in [wire for wire in sorted(wires) if wire[0] == 'z']:
        if wires[wire] is None:
            return None

        # ic(wire, wires[wire], power)
        output += wires[wire] * 2 ** power
        power += 1
    return output



with open('input.txt', 'r') as file:
    device_str = file.read()

wires = {}

wires_str, gates_str = device_str.split('\n\n')

for wire_str, value_str in [line.split(': ') for line in wires_str.split('\n')]:
    # ic(wire_str, value_str)
    wires[wire_str] = int(value_str)

gates = []
for line in gates_str.split('\n'):
    terms = line.split(' ')

    gates.append((terms[0], terms[1], terms[2], terms[4]))

    wire1 = terms[0]
    wire2 = terms[2]
    wire3 = terms[4]
    if wire1 not in wires:
        wires[wire1] = None
    if wire2 not in wires:
        wires[wire2] = None
    if wire3 not in wires:
        wires[wire3] = None


ic(wires)
ic(gates)
ic(result(wires))



while result(wires) is None:
    r = ready(wires, gates)
    # ic(r)

    for wire1, operator, wire2, out in r:
        operand1, operand2 = wires[wire1], wires[wire2]
        if operator == 'OR':
            wires[out] = operand1 or operand2
        elif operator == 'AND':
            wires[out] = operand1 and operand2
        else:
            wires[out] = operand1 ^ operand2

# ic(wires)
ic(result(wires))
