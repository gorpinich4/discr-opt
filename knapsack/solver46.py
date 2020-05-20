#!/usr/bin/python
# -*- coding: utf-8 -*-

from recordclass import recordclass
from collections import deque
import heapq

Item = recordclass('Item', 'index value weight')
Node = recordclass('Node', 'level value weight items')

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count + 1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i - 1, int(parts[0]), int(parts[1])))

    # branch and bound

    def bound(u, capacity, item_count, items):
        if (u.weight >= capacity):
            return 0
        else:
            result = u.value
            j = u.level + 1
            totweight = u.weight

            while (j < item_count and totweight + items[j].weight <= capacity):
                totweight = totweight + items[j].weight
                result = result + items[j].value
                j += 1

            k = j
            if (k <= item_count - 1):
                result += (capacity - totweight) * items[k].value / items[k].weight
            return result

    items = sorted(items, key=lambda Item: Item.value / Item.weight, reverse=True)

    #traversing
    snode = Node(level=-1, value=0, weight=0, items=[])
    Q = deque([])
    Q.append(snode)

    max_val = 0
    best_res = []

    while (len(Q) != 0):
        snode = Q[0]

        Q.popleft()

        nnode = Node(level=None, weight=None, value=None, items=[])

        nnode.level = snode.level + 1
        nnode.weight = items[nnode.level].weight + snode.weight
        nnode.value = items[nnode.level].value + snode.value
        nnode.items = list(snode.items)
        nnode.items.append(items[nnode.level].index)

        if (nnode.weight <= capacity and nnode.value > max_val):
            max_val = nnode.value
            best_res = nnode.items

        bound_u = bound(nnode, capacity, item_count, items)

        if (bound_u > max_val):
            Q.append(nnode)

        nnode = Node(level=None, weight=None, value=None, items=[])
        nnode.items = list(snode.items)
        nnode.value = snode.value
        nnode.level = snode.level + 1
        nnode.weight = snode.weight

        bound_u = bound(nnode, capacity, item_count, items)

        if (bound_u > max_val):
            Q.append(nnode)

    taken = [0] * len(items)
    for i in range(len(best_res)):
        taken[best_res[i]] = 1

    # prepare the solution in the specified output format

    output_data = str(max_val) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  '
              'Please select one from the data directory. '
              '(i.e. python solver.py ./data/ks_4_0)')
