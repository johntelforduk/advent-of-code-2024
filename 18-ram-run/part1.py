# Advent of code day 8, RAM Run.
# https://adventofcode.com/2024/day/18

from icecream import ic
import networkx as nx

with open('input.txt', 'r') as file:
    memory_str = file.read()

mx, my = 70, 70
G = nx.DiGraph()        # Directed graph.

for x in range(mx + 1):
    for y in range(my + 1):
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            x1 = x + dx
            y1 = y + dy
            if 0 <= x1 <= mx and 0 <= y1 <= my:
                G.add_edge((x, y), (x1, y1), weight=1)

start = (0, 0)
end = (mx, my)
shortest_path_length = nx.shortest_path_length(G, source=start, target=end, weight='weight')

lines = memory_str.split('\n')
reachable = True
while len(lines) > 0 and reachable:
    this_line = lines.pop(0)
    x_str, y_str = this_line.split(',')
    x, y = int(x_str), int(y_str)
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        x1 = x + dx
        y1 = y + dy
        if 0 <= x1 <= mx and 0 <= y1 <= my:
            G.remove_edge((x, y), (x1, y1))         # Makes (x, y) a dead-end.

    if not nx.has_path(G, start, end):
        ic(f'{x},{y}')
        reachable = False
