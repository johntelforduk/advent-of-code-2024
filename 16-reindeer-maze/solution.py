# Advent of code day 16, Reindeer Maze.
# https://adventofcode.com/2024/day/16

from icecream import ic
import networkx as nx
import matplotlib.pyplot as plt


def render(G):
    pos = nx.random_layout(G)

    nx.draw(G, pos, with_labels=True)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.show()


def draw(maze: dict, short: set, mx: int, my: int):
    for y in range(my):
        for x in range(mx):
            if (x, y) in short:
                print('O', end='')
            else:
                print(maze[(x, y)], end='')
        print()
    print()


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

G = nx.DiGraph()        # Directed graph.

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

ic(start_x, start_y, end_x, end_y)

best = None
on_short_path = set()
start = (start_x, start_y, 'E')
for d in 'N':                      # Can end with a move that is either travelling N or E.
    end = (end_x, end_y, d)
    ic(start, end)
    shortest_path_length = nx.shortest_path_length(G, source=start, target=end, weight='weight')
    if best is None:
        best = shortest_path_length
    else:
        shortest_path_length = min(best, shortest_path_length)
    ic(shortest_path_length)


    # Part 2.
    all_shortest_paths = list(nx.all_shortest_paths(G, source=start, target=end, weight='weight'))
    # print(f"All shortest paths: {all_shortest_paths}")
    for a_short_path in all_shortest_paths:
        # ic(a_short_path)
        for x, y, _ in a_short_path:
            on_short_path.add((x, y))

ic(best)
ic(len(on_short_path))
# ic(on_short_path)
# render(G)

draw(maze,on_short_path, mx, my)
