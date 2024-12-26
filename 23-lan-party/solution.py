# Advent of code day 23, LAN Party.
# https://adventofcode.com/2024/day/23

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt
import random


def render(G, triangles):
    pos = nx.circular_layout(G)  # Node positions.
    nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray')  # Base graph

    # Highlight triangles by shading inside them.
    if triangles:
        for triangle in triangles:
            # Get positions of the triangle's vertices.
            pts = [pos[node] for node in triangle]
            pts.append(pts[0])  # Close the triangle by repeating the first point.

            # Shade the triangle area.
            this_colour = 'orange'
            plt.fill(*zip(*pts), color=this_colour, alpha=0.3)  # Transparent orange fill

            # Draw edges and nodes for emphasis.
            nx.draw_networkx_nodes(G, pos, nodelist=triangle, node_color='orange')
            nx.draw_networkx_edges(G, pos,
                                   edgelist=[(triangle[i], triangle[j]) for i in range(3) for j in range(i + 1, 3)],
                                   edge_color='red', width=2)

    plt.show()

with open('input.txt', 'r') as file:
    network_str = file.read()

G = nx.Graph()

for computer1, computer2 in [line.split('-') for line in network_str.split('\n')]:
    ic(computer1, computer2)
    G.add_edge(computer1, computer2)



triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]
# ic(triangles)
# render(G, triangles=triangles)

count = 0
for tri in triangles:
    found = False
    for v in tri:
        if not found and v[0] == 't':
            count += 1
            found = True
ic(count)
