# Advent of code day 23, LAN Party.
# https://adventofcode.com/2024/day/23

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt


def render(G, triangles):
    pos = nx.circular_layout(G)  # Node positions.
    nx.draw(G, pos, with_labels=True)  # Base graph.

    # Highlight triangles by shading inside them.
    if triangles:
        for triangle in triangles:
            # Get positions of the triangle's vertices.
            pts = [pos[node] for node in triangle]
            pts.append(pts[0])  # Close the triangle by repeating the first point.

            has_t = False
            for v in triangle:
                if v[0] == 't':
                    has_t = True

            if has_t:
                this_colour = 'orange'
            else:
                this_colour = 'blue'
            plt.fill(*zip(*pts), color=this_colour, alpha=0.3)

            # Draw edges and nodes for emphasis.
            nx.draw_networkx_edges(G, pos,
                                   edgelist=[(triangle[i], triangle[j]) for i in range(3) for j in range(i + 1, 3)],
                                   edge_color=this_colour, width=2)

    plt.show()

with open('input.txt', 'r') as file:
    network_str = file.read()

G = nx.Graph()

for computer1, computer2 in [line.split('-') for line in network_str.split('\n')]:
    G.add_edge(computer1, computer2)

triangles = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]

part1 = 0
for tri in triangles:
    found = False
    for v in tri:
        if not found and v[0] == 't':
            part1 += 1
            found = True
ic(part1)

render(G, triangles=triangles)

cliques = list(nx.find_cliques(G))
largest_clique = max(cliques, key=len)
ic(largest_clique)
part2 = None
for computer in sorted(largest_clique):
    if part2 is None:
        part2 = computer
    else:
        part2 += ',' + computer
ic(part2)
