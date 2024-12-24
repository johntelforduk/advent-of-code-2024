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
        output = []
        for path in paths:
            labels = ''
            for i in range(len(path) - 1):
                labels += self.G[path[i]][path[i + 1]]['direction']
            labels += 'A'
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
            so_far = found + option
            new.extend(self.press_keys(required=left, found=so_far, start_key=next_key))
        return new

    @lru_cache(maxsize=None)
    def start_key_a(self, required) -> str:
        """For a parm required sequence, start at key 'A'. Return one example of the shortest sequence
        possible."""
        shortest = None
        for sequence in self.press_keys(required=required, found='', start_key='A'):
            if shortest is None:
                shortest = sequence
            else:
                if len(sequence) < len(shortest):
                    shortest = sequence
        return shortest


# def score(sequence: str) -> int:
#     score = 0
#     # Distance from "A".
#     for c in sequence:
#         if c == '<':
#             score += 3
#         elif c == 'v':
#             score += 2
#         else:
#             score += 1
#     return score


# def reduce(sequences: list) -> list:
#     shortest = None
#     for s in sequences:
#         if shortest is None:
#             shortest = len(s)
#         else:
#             shortest = min(shortest, len(s))
#
#     shorts = []
#     for s in sequences:
#         if len(s) == shortest:
#             shorts.append(s)
#     return shorts


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

def patterns(sequence: str) -> dict:
    """For a parm sequence string, count the number of occurances of each pattern in it."""
    output = {}
    sub = ''
    stage = 'moves'
    for x in sequence:
        if stage == 'moves' and x != 'A':
            sub += x
        elif stage == 'moves' and x == 'A':
            stage = 'aiis'
            sub += x
        elif stage == 'aiis' and x == 'A':
            sub += x
        elif stage == 'aiis' and x != 'A':
            if sub != '':
                if sub not in output:
                    output[sub] = 1
                else:
                    output[sub] += 1
            stage = 'moves'
            sub = x

    # Don's miss the last one.
    if sub != '':
        if sub not in output:
            output[sub] = 1
        else:
            output[sub] += 1

    return output


total = 0
for code_no, code in enumerate(code_str.split('\n')):
    numeric_sequences = numeric.press_keys(required=code, found='', start_key='A')

    for sequence in numeric_sequences:
        current_patterns = patterns(sequence)
        ic(code_no, code, sequence, current_patterns)

        # Robot 1
        new_whole_pattern = {}
        for pattern in current_patterns:
            shortest = directional.start_key_a(required=pattern)
            ic(pattern, shortest)
            new_patterns = patterns(shortest)
            ic(new_patterns)

            for each in new_patterns:
                if each not in new_whole_pattern:
                    new_whole_pattern[each] = new_patterns[each]
                else:
                    new_whole_pattern[each] += new_patterns[each]
        ic(new_whole_pattern)
        




#     for robot in range(1):
#         ic(code_no, robot)
#         seq2 = []
#         processed = 0
#
#         ic(len(seq1))
#         for s in seq1:
#
#             for sub in s.split('A'):
#                 if sub != '':
#                     need = sub + 'A'
#                     ic(s, sub, need)
#                     sub_seq = directional.press_keys(required=need, found='', position='A')[0]
#
#
#             seq = directional.press_keys(required=s, found='', position='A')
#             seq2.extend(seq)
#             processed += 1
#
#         # seq2 = reduce(seq2)
#         # seq1 = seq2.copy()
#
#     shortest = min(len(s) for s in seq1)
#     ic(shortest)
#
#     numeric_part = int(code[:-1])
#     total += shortest * numeric_part
#
# ic(total)
