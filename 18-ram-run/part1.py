# Advent of code day 8, RAM Run.
# https://adventofcode.com/2024/day/18

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt


def render(G):
    pos = nx.random_layout(G)
    nx.draw(G, pos, with_labels=True)
    nx.draw_networkx(G, pos)
    plt.show()


def draw(memory: set, mx, my):
    for y in range(my + 1):
        for x in range(mx + 1):
            if (x, y) in memory:
                print('#', end='')
            else:
                print('.', end='')
        print()


with open('input.txt', 'r') as file:
    memory_str = file.read()

memory = set()
mx, my = 0, 0
count = 0
for line_str in memory_str.split('\n'):
    x_str, y_str = line_str.split(',')
    x, y = int(x_str), int(y_str)
    mx = max(mx, x)
    my = max(my, y)

    count += 1
    if count <= 1024:
        memory.add((x, y))

ic(mx, my)

G = nx.DiGraph()        # Directed graph.

for x in range(mx + 1):
    for y in range(my + 1):
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x1 = x + dx
            y1 = y + dy
            if 0 <= x1 <= mx and 0 <= y1 <= my:
                if (x, y) not in memory and (x1, y1) not in memory:
                    G.add_edge((x, y), (x1, y1), weight=1)

# render(G)
start = (0, 0)
end = (mx, my)
shortest_path_length = nx.shortest_path_length(G, source=start, target=end, weight='weight')
ic(shortest_path_length)
