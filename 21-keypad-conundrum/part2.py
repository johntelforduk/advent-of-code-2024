# Advent of code day 21, Keypad Conundrum.
# https://adventofcode.com/2024/day/21

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt
from functools import lru_cache


def add_non_space(d:dict, k, v):
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

    # @lru_cache(maxsize=None)
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

    # @lru_cache(maxsize=None)
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

    # @lru_cache(maxsize=None)
    def start_key_a(self, required: str) -> str:
        """For a parm required sequence, start at key 'A'. Return one example of the shortest sequence
        possible."""
        shortest = None
        for sequence in self.press_keys(required=required, found='', start_key='A'):
            if shortest is None:
                shortest = sequence
            else:
                if len(sequence) < len(shortest):
                    shortest = sequence

        # # To make output compatible with example.
        # if shortest == 'v<':
        #     return '<v'

        return shortest


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



def length(patterns: dict) -> int:
    """Work out the total length of the sequence represented by the pattern occurance counts."""
    total = 0
    for p in patterns:
        total += len(p) * patterns[p]
    return total


def patterns(sequence: str) -> dict:
    """For a parm sequence string, count the number of occurances of each pattern in it."""
    output = {}
    output_str = ''
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
        # if sub != '':

            if sub not in output:
                output[sub] = 1
            else:
                output[sub] += 1
            output_str += sub
            stage = 'moves'

            sub = x

    # Don's miss the last one.
    # if sub != '':
    # output.append(sub)
    if sub not in output:
        output[sub] = 1
    else:
        output[sub] += 1

    output_str += sub

    assert sequence == output_str
    assert length(output) == len(sequence)
    return output


with open('test.txt', 'r') as file:
    code_str = file.read()

total = 0
for code in code_str.split('\n'):
    numeric_sequences = numeric.press_keys(required=code, found='', start_key='A')

    lowest = None
    for sequence in numeric_sequences:
        current_sequence = sequence
        pattern_dict = patterns(current_sequence)

        for robot in range(3):
            ic(robot, length(pattern_dict), pattern_dict)

            next_pattern_dict = {}
            for pattern in pattern_dict:
                shortest = directional.start_key_a(required=pattern)
                new_patterns = patterns(shortest)
                ic(robot, pattern, shortest)

                for each in new_patterns:
                    if each not in next_pattern_dict:
                        next_pattern_dict[each] = pattern_dict[pattern] * new_patterns[each]
                    else:
                        next_pattern_dict[each] += pattern_dict[pattern] * new_patterns[each]

            pattern_dict = next_pattern_dict.copy()

        sequence_length = length(pattern_dict)

    # ic(code, sequence, current_sequence, sequence_length)
    if lowest is None:
        lowest = sequence_length
    else:
        lowest = min(lowest, sequence_length)

    numeric_part = int(code[:-1])
    complexity = lowest * numeric_part
    ic(code, lowest)
    total += complexity

# ic(total)

ic(patterns("<vA<AA>>^AvAA<^A>A"))
