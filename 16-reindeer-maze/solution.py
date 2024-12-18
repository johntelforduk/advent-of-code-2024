# Advent of code day 16, Reindeer Maze.
# https://adventofcode.com/2024/day/16

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt

with open('test1.txt', 'r') as file:
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

# Add horizontal edges.
for y in range(1, my):
    inside = False
    sx = None
    for x in range(mx):
        # ic(x, y, maze[(x, y)], inside)
        if not inside and maze[(x, y)] in '.SE':
            sx = x
            inside = True
        elif inside:
            if maze[(x, y)] == '#':
                if x != sx + 1:         # Just part of a vertical path.
                    cost = x - sx
                    # ic(start, end, cost)
                    G.add_edge((sx, y, 'E'), (x - 1, y, 'E'), weight=cost)
                    G.add_edge((x - 1, y, 'W'), (sx, y, 'W'), weight=cost)
                inside = False

# Add vertical edges.
for x in range(1, mx):
    inside = False
    sy = None
    for y in range(mx):
        # ic(x, y, maze[(x, y)], inside)
        if not inside and maze[(x, y)] in '.SE':
            sy = y
            inside = True
        elif inside:
            if maze[(x, y)] == '#':
                if y != sy + 1:         # Just part of a vertical path.
                    cost = y - sy
                    ic((x, sy), (x, y - 1), cost)
                    G.add_edge((x, sy, 'S'), (x, y - 1, 'S'), weight=cost)
                    G.add_edge((x, y - 1, 'N'), (x, sy, 'N'), weight=cost)
                inside = False


# Add rotation edges.
G_copy = G.copy()

turns = {'N': 'WE', 'S': 'WE', 'E': 'NS', 'W': 'NS'}
for x, y, d in G_copy.nodes:
    ic(x, y, d)
    for t in turns[d]:
        cost = 1000
        G.add_edge((x, y, d), (x, y, t), weight=cost)

ic(start_x, start_y, end_x, end_y)

# Define source and target nodes
start = (start_x, start_y, 'N')
end = (1, 7, 'E')

# Use Dijkstra's algorithm to find the shortest path
shortest_path = nx.shortest_path(G, source=start, target=end, weight='weight')
shortest_path_length = nx.shortest_path_length(G, source=start, target=end, weight='weight')

ic(shortest_path_length)




#
# # Compute node positions (spring layout for better visuals)
# pos = nx.random_layout(G)
#
# # Draw the graph with labels
# subax1 = plt.subplot(111)
# nx.draw(G, pos, with_labels=True)
#
# # Add edge labels
# edge_labels = nx.get_edge_attributes(G, 'weight')  # Get the 'weight' attribute for labels
# nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
#
# plt.show()
