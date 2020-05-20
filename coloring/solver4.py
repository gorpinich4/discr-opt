#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))

    Node = namedtuple("Node", ['index', 'neighbors'])

    nodes = []

    for i in range(node_count):
        nodes.append(Node(i, []))

    for i in range(node_count):
        for e in edges:
            if e[0] == i:
                nodes[i].neighbors.append(e[1])
            elif e[1] == i:
                nodes[i].neighbors.append(e[0])

    def myfunc(node):
        sum = 0
        for i in node.neighbors:
            sum += len(nodes[i].neighbors)
        return sum

    color = [-1] * node_count
    nodes = sorted(nodes, key=myfunc, reverse=True)

    def check_constraints(domain, color, node):
        color[node.index] = domain[0]
        c = 0
        for i in node.neighbors:
            if color[i] == color[node.index]:
                del domain[0]
                c += 1
                break
        if c != 0:
            color = check_constraints(domain, color, node)
        return color

    for node in nodes:
        domain = list(range(node_count))
        col = color.copy()
        color = check_constraints(domain, col, node)

    # prepare the solution in the specified output format
    output_data = str(max(color)) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, color))

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

