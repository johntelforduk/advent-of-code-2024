# Advent of code day 21, Keypad Conundrum.
# https://adventofcode.com/2024/day/21

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt
from functools import lru_cache


def add_non_space(d:dict, k, v):
    if v != ' ':
        d[k] = v

# input = the layout of the keys.
# input = desired code, 029A
# output = list of shortest possible key sequences to achieve it.
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
        # ic(pad)

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
        # ic(paths)

        output = []
        for path in paths:
            labels = ''
            for i in range(len(path) - 1):
                labels += self.G[path[i]][path[i + 1]]['direction']
            labels += 'A'
            output.append(labels)
        return output

    # @lru_cache(maxsize=None)
    def press_keys(self, required: str, found: str, position: str) -> list:
        # ic('press_keys', required, found, position, sequences)

        if len(required) == 0:
            return [found]

        next_key = required[0]          # Next key we need is the front character of the string.
        left = required[1:]             # Once we get the next key, what's left is the rest of the characters.

        new = []
        for option in self.press_one_key(current_key=position, target_key=next_key):
            so_far = found + option
            new.extend(self.press_keys(required=left, found=so_far, position=next_key))
        return new

def reduce(sequences: list) -> list:
    shortest = None
    for s in sequences:
        if shortest is None:
            shortest = len(s)
        else:
            shortest = min(shortest, len(s))

    shorts = []
    for s in sequences:
        if len(s) == shortest:
            shorts.append(s)
    return shorts


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

directional = Keypad(layout="""
    +---+---+
    | ^ | A |
+---+---+---+
| < | v | > |
+---+---+---+""")

with open('test.txt', 'r') as file:
    code_str = file.read()

total = 0
for code_no, code in enumerate(code_str.split('\n')):
    seq1 = numeric.press_keys(required=code, found='', position='A')
    ic(seq1)

    for robot in range(2):
        ic(code_no, robot)
        seq2 = []
        processed = 0
        seq1 = reduce(seq1)

        for s in seq1:
            ic(s)
            seq = directional.press_keys(required=s, found='', position='A')
            seq2.extend(seq)
            processed += 1
        seq1 = seq2.copy()

    shortest = min(len(s) for s in seq1)
    ic(shortest)

    numeric_part = int(code[:-1])
    total += shortest * numeric_part

ic(total)
