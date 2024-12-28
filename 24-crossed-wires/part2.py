# Advent of code day 24, Crossed Wires.
# https://adventofcode.com/2024/day/24

from icecream import ic
import pydot

with open('input.txt', 'r') as file:
    device_str = file.read()

# Don't need the value on wires for part 2.
_, gates_str = device_str.split('\n\n')

gates = []
for line in gates_str.split('\n'):
    operand1, operator, operand2, _, output = tuple(line.split(' '))
    gates.append((operand1, operator, operand2, output))

for op1, operator, op2, output in gates:
    if output[0] == 'z' and operator != 'XOR':
        ic(op1, operator, op2, output)

operator_to_shape = {'AND': 'circle',
                     'OR': 'diamond',
                     'XOR': 'triangle'}

graph = pydot.Dot("my_graph", graph_type="digraph", bgcolor="white")
for operand1, operator, operand2, output in gates:

    node_name = f'{operand1}_{operator}_{operand2}'
    shape = operator_to_shape[operator]
    my_node = pydot.Node(node_name, label=operator, shape=shape)
    graph.add_node(my_node)

    my_node = pydot.Node(output, label=output, shape='none')
    graph.add_node(my_node)

    my_node = pydot.Node(operand1, label=operand1, shape='none')
    graph.add_node(my_node)

    my_node = pydot.Node(operand2, label=operand2, shape='none')
    graph.add_node(my_node)


for operand1, operator, operand2, output in gates:
    node_name = f'{operand1}_{operator}_{operand2}'

    my_edge = pydot.Edge(operand1, node_name)
    graph.add_edge(my_edge)

    my_edge = pydot.Edge(operand2, node_name)
    graph.add_edge(my_edge)

    my_edge = pydot.Edge(node_name, output)
    graph.add_edge(my_edge)

graph.write_png("output.png")
