# Advent of code day 16, Reindeer Maze.
# https://adventofcode.com/2024/day/16

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt


def render(G):
    pos = nx.random_layout(G)

    subax1 = plt.subplot(111)
    nx.draw(G, pos, with_labels=True)

    # Add edge labels
    edge_labels = nx.get_edge_attributes(G, 'weight')  # Get the 'weight' attribute for labels
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()



with open('input.txt', 'r') as file:
    maze_str = file.read()

maze = {}

my = 0
for line in maze_str.split('\n'):
    mx = 0
    for t in line:
        maze[(mx, my)] = t
        if t == 'S':
            start_x, start_y = mx, my
        elif t == 'E':
            end_x, end_y = mx, my
        mx += 1
    my += 1

G = nx.DiGraph()

turns = {'N': 'WE', 'S': 'WE', 'E': 'NS', 'W': 'NS'}
for x, y in maze:
    if maze[x, y] in '.SE':
        moves = {'E': (1, 0), 'S': (0, 1), 'W': (-1, 0), 'N': (0, -1)}
        for m in moves:
            dx, dy = moves[m]
            if (x + dx, y + dy) in maze:
                if maze[(x + dx, y + dy)] in '.SE':
                    cost = 1
                    G.add_edge((x, y, m), (x + dx, y + dy, m), weight=cost)

        for d1 in turns:
            for d in turns[d1]:
                cost = 1000
                G.add_edge((x, y, d1), (x, y, d), weight=cost)


# # Add horizontal edges.
# for y in range(1, my):
#     inside = False
#     sx = None
#     for x in range(mx):
#         # ic(x, y, maze[(x, y)], inside)
#         if not inside and maze[(x, y)] in '.SE':
#             sx = x
#             inside = True
#         elif inside:
#             if maze[(x, y)] == '#':
#                 if x != sx + 1:         # Just part of a vertical path.
#                     cost = x - sx
#                     # ic(start, end, cost)
#                     G.add_edge((sx, y, 'E'), (x - 1, y, 'E'), weight=cost)
#                     G.add_edge((x - 1, y, 'W'), (sx, y, 'W'), weight=cost)
#                 inside = False
#
# # Add vertical edges.
# for x in range(1, mx):
#     inside = False
#     sy = None
#     for y in range(mx):
#         # ic(x, y, maze[(x, y)], inside)
#         if not inside and maze[(x, y)] in '.SE':
#             sy = y
#             inside = True
#         elif inside:
#             if maze[(x, y)] == '#':
#                 if y != sy + 1:         # Just part of a vertical path.
#                     cost = y - sy
#                     ic((x, sy), (x, y - 1), cost)
#                     G.add_edge((x, sy, 'S'), (x, y - 1, 'S'), weight=cost)
#                     G.add_edge((x, y - 1, 'N'), (x, sy, 'N'), weight=cost)
#                 inside = False

#
# # Add rotation edges.
# G_copy = G.copy()
#
# turns = {'N': 'WE', 'S': 'WE', 'E': 'NS', 'W': 'NS'}
# for x, y, d in G_copy.nodes:
#     ic(x, y, d)
#     for t in turns[d]:
#         cost = 1000
#         G.add_edge((x, y, d), (x, y, t), weight=cost)

ic(start_x, start_y, end_x, end_y)

# Define source and target nodes

best = None
start = (start_x, start_y, 'E')
for d in 'NE':                      # Can end with a move that is either travelling N or E.
    end = (end_x, end_y, d)
    ic(start, end)
    shortest_path_length = nx.shortest_path_length(G, source=start, target=end, weight='weight')
    if best is None:
        best = shortest_path_length
    else:
        shortest_path_length = min(best, shortest_path_length)
    ic(shortest_path_length)


ic(best)



