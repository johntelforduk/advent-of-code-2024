# Advent of code day 21, Keypad Conundrum.
# https://adventofcode.com/2024/day/21

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt
from functools import lru_cache


def add_non_space(d: dict, k, v):
    if v != ' ':
        d[k] = v


class Keypad:

    def __init__(self, layout: str):

        # Parse the layout ASCII art into a dictionary of coordinates and key-caps.
        pad, y = {}, 0
        lines = [row for row in layout[1:].split('\n')]
        while len(lines) > 0:
            row = lines.pop(0)
            if row[-1] != '+':
                add_non_space(pad, (0, y), row[2])
                add_non_space(pad, (1, y), row[6])
                add_non_space(pad, (2, y), row[10])
                y += 1

        # Use the dict to make a graph of key routes.
        self.G = nx.DiGraph()
        for x1, y1 in pad:
            for dx, dy, direction in [(1, 0, '>'), (0, 1, 'v'), (-1, 0, '<'), (0, -1, '^')]:
                x2, y2 = x1 + dx, y1 + dy
                if (x2, y2) in pad:
                    self.G.add_edge(pad[(x1, y1)],
                                    pad[(x2, y2)],
                                    direction=direction)

        self.pos = 'A'

    def render(self):
        pos = nx.circular_layout(self.G)
        nx.draw(self.G, pos, with_labels=True)
        plt.show()

    @lru_cache(maxsize=None)
    def press_one_key(self, current_key: str, target_key: str) -> list:
        paths = list(nx.all_shortest_paths(self.G, source=current_key, target=target_key))
        output = []
        for path in paths:
            labels = ''
            for i in range(len(path) - 1):
                labels += self.G[path[i]][path[i + 1]]['direction']
            # labels += 'A'
            output.append(labels)
        return output

    @lru_cache(maxsize=None)
    def press_keys(self, required: str, found: str, start_key: str) -> list:
        if len(required) == 0:
            return [found]

        next_key = required[0]          # Next key we need is the front character of the string.
        left = required[1:]             # Once we get the next key, what's left is the rest of the characters.

        new = []
        for option in self.press_one_key(current_key=start_key, target_key=next_key):
            so_far = found + option + 'A'
            new.extend(self.press_keys(required=left, found=so_far, start_key=next_key))
        return new


@lru_cache(maxsize=None)
def split_sequence(sequence: str) -> list:
    assert sequence[-1] == 'A'                          # Sequences should always end with 'A'.
    return [c + 'A' for c in sequence.split('A')[:-1]]


@lru_cache(maxsize=None)
def shortest(sequence: str, depth: int, kp: Keypad) -> int:
    if depth == 0:
        return len(sequence)

    total = 0
    for sub_sequence in split_sequence(sequence):
        keys_list = kp.press_keys(required=sub_sequence, found='', start_key='A')
        minimum = None
        for each_key_seq in keys_list:
            this_short = shortest(sequence=each_key_seq, depth=depth - 1, kp=kp)
            if minimum is None:
                minimum = this_short
            else:
                minimum = min(minimum, this_short)
        total += minimum
    return total


numeric = Keypad(layout="""
+---+---+---+
| 7 | 8 | 9 |
+---+---+---+
| 4 | 5 | 6 |
+---+---+---+
| 1 | 2 | 3 |
+---+---+---+
    | 0 | A |
    +---+---+""")

ic(numeric.press_one_key('7', '0'))

directional = Keypad(layout="""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+""")

with open('input.txt', 'r') as file:
    code_str = file.read()

total = 0
for code in code_str.split('\n'):
    numeric_sequences = numeric.press_keys(required=code, found='', start_key='A')

    lowest = None
    for sequence in numeric_sequences:
        this = shortest(sequence=sequence, depth=25, kp=directional)
        if lowest is None:
            lowest = this
        else:
            lowest = min(lowest, this)

    numeric_part = int(code[:-1])
    complexity = lowest * numeric_part
    ic(code, lowest)
    total += complexity

ic(total)
