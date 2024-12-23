# Advent of code day 20, Race Condition.
# https://adventofcode.com/2024/day/20

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt


def render(G):
    pos = nx.random_layout(G)
    nx.draw(G, pos, with_labels=True)
    plt.show()


with open('input.txt', 'r') as file:
    track_str = file.read()

ic('loading track from file')
track = set()
my = 0
for line in track_str.split('\n'):
    mx = 0
    for t in line:
        if t in '.SE':
            track.add((mx, my))
        if t == 'S':
            start = (mx, my)
        elif t == 'E':
            end = (mx, my)
        mx += 1
    my += 1

# ic(track)
G = nx.DiGraph()        # Directed graph.

ic('creating graph')
for x, y in track:
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x2 = x + dx
        y2 = y + dy
        if (x2, y2) in track:
            G.add_edge((x, y), (x2, y2), weight=1)

# render(G)
# base = nx.shortest_path_length(G, source=start, target=end, weight='weight')
# ic(base)

count = 0

def manhattan(x1, y1, x2, y2) -> int:
    return abs(x1 - x2) + abs(y1 - y2)

# Work our shortest distance from each track position to the end.
ic('work out shortest distances')
shortest_dist = {}
for x, y in track:
    ic('working out shortest', x, y)
    shortest_dist[x, y] = nx.shortest_path_length(G, source=(x, y), target=end, weight='weight')
# ic(shortest_dist)

ic('work out savings')
MINIMUM_SAVING = 100
cheats = {}
count = 0
len_track = len(track)
checked = 0
for x1, y1 in track:
    checked += 1
    # Find all the other squares that are within 20 of this one.
    for x2, y2 in track:
        m = manhattan(x1, y1, x2, y2)
        if m <= 20:
            # ic(x1, y1, x2, y2)

            # Will this candidate "short-cut" actually get us closer to the end?
            d1 = shortest_dist[(x1, y1)]
            d2 = shortest_dist[(x2, y2)]
            potential = d1 - d2 - m
            if potential >= MINIMUM_SAVING:
                ic('potential time saver', checked, len_track, potential)
                count += 1
                if potential not in cheats:
                    cheats[potential] = 1
                else:
                    cheats[potential] += 1

for c in sorted(cheats):
    ic(c, cheats[c])

ic(count)
