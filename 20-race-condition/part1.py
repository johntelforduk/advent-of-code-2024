# Advent of code day 20, Race Condition.
# https://adventofcode.com/2024/day/20

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt


def render(G):
    pos = nx.random_layout(G)
    nx.draw(G, pos, with_labels=True)
    # edge_labels = nx.get_edge_attributes(G, 'weight')
    # nx.draw_networkx_edge_labels(G, pos)
    plt.show()


with open('input.txt', 'r') as file:
    track_str = file.read()

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

ic(track)
G = nx.DiGraph()        # Directed graph.

for x, y in track:
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x2 = x + dx
        y2 = y + dy
        if (x2, y2) in track:
            G.add_edge((x, y), (x2, y2), weight=1)

# render(G)
base = nx.shortest_path_length(G, source=start, target=end, weight='weight')
ic(base)

count = 0
for x in range(mx):
    for y in range(my):
        if (x, y) not in track:
            # ic('wall', x, y)
            for fdx, fdy, tdx, tdy in [(-1, 0, 1, 0), (1, 0, -1, 0), (0, -1, 0, 1), (0, 1, 0, -1)]:
                fx, fy, tx, ty = x + fdx, y + fdy, x + tdx, y + tdy
                if (fx, fy) in track and (tx, ty) in track:

                    G.add_edge((fx, fy), (x, y), weight=1)
                    G.add_edge((x, y), (tx, ty), weight=1)

                    this = nx.shortest_path_length(G, source=start, target=end, weight='weight')
                    if this < base:
                        saving = base - this
                        if saving >= 100:
                            count += 1
                            ic('cheat', x, y, saving, count)

                    G.remove_edge((fx, fy), (x, y))
                    G.remove_edge((x, y), (tx, ty))

ic(count)