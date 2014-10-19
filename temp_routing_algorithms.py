"""
Bellman-Ford and Dijkstra Shortest-path Routing Algorithms

This pretty-prints calculation and routing tables for user-defined networks.
The "broker" is the optimal node to go through for a given target.
The "cost" is the quantity to minimize for each path, as a sum of edge costs.

.. moduleauthor:: Jan Van Bruggen <jancvanbruggen@gmail.com>
"""

from __future__ import print_function
from heapq import heappop, heappush


def bellman_ford(edges, source):
    """
    Return two dictionaries of node IDs keying to broker node IDs and costs
    for the shortest paths to each node, using the Bellman-Ford algorithm
    """
    brokers, costs = {}, {}
    nodes = []
    for edge in edges:
        for node in edge[:2]:
            if node not in nodes:
                nodes.append(node)
                # Initialize the broker as -1, except as source for source
                brokers[node] = source if node is source else -1
                # Initialize the cost as infinite, except as 0 for source
                costs[node] = 0 if node is source else float('inf')
    print_targets(brokers.keys())
    print_bellman_state(brokers, costs)
    # Iterate the maximum number of times needed to converge
    for edge in edges * (len(nodes) - 2):
        node1, node2, cost = edge
        # Check the edge in both directions
        for sender, receiver in ((node1, node2), (node2, node1)):
            # If the new path to the receiver is cheaper, save the path
            if costs[sender] + cost < costs[receiver]:
                brokers[receiver] = sender
                costs[receiver] = costs[sender] + cost
        print_bellman_state(brokers, costs)
    return brokers, costs


def dijkstra(edges, source):
    """
    Return two dictionaries of node IDs keying to broker node IDs and costs
    for the shortest paths to each node, using Dijkstra's algorithm
    """
    paths, costs = {}, {}
    seen = set()
    unseen = [(0, source, ())]
    # all nodes (for print table)
    all = list(set(edge[i] for edge in edges for i in (0, 1)))
    print_targets(all)
    print_dijkstra_state(all, paths, costs)
    # While nodes remain in the unseen heap
    while unseen:
        # Get the next node from the heap
        cost, node1, path = heappop(unseen)
        # If the node is unseen, save the path and check neighboring nodes
        if node1 not in seen:
            seen.add(node1)
            path = (node1, path)
            # Save the optimal path and cost
            paths[node1] = path
            costs[node1] = cost
            # Check all neighboring nodes
            for edge in [edge for edge in edges if node1 in edge[:2]]:
                edgecost = edge[2]
                # Find the edge's other node
                node2 = edge[0] if edge.index(node1) else edge[1]
                if node2 not in seen:
                    # Add the unseen other node to the unseen heap
                    heappush(unseen, (cost + edgecost, node2, path))
        print_dijkstra_state(all, paths, costs)
    return paths, costs


def print_targets(targets):
    """Print all targets."""
    print('_' * (6 * len(targets) + 1))
    print('| ', end='')
    for target in sorted(targets):
        print('  ' + str(target) + '   ', end=' | ')
    print()
    print('|' + '-' * (6 * len(targets) - 1) + '|')


def print_bellman_chains(brokers, costs, edges, source):
    """Print the routing chain from source to each target, with costs."""
    for target in sorted(brokers.keys()):
        chain = [target]
        next = target
        while chain[-1] is not source:
            chain.append(brokers[next])
            next = brokers[next]
        print(source, '-->', target,
              'costs', costs[target],
              '|', source, end='')
        last = source
        for broker in chain[-2::-1]:
            for edge in edges:
                if edge[:2] in ((last, broker), (broker, last)):
                    cost = edge[2]
                    break
            print(' --' + str(cost) + '--> ' + str(broker), end='')
            last = broker
        print()


def print_bellman_state(brokers, costs):
    """Print the current set of brokers and costs for each target"""
    print('| ', end='')
    for target in sorted(brokers.keys()):
        broker = str(brokers[target])
        cost = str(costs[target])
        print(' ' * (2 - len(broker)) + broker + ',' +
              ' ' * (3 - len(cost)) + cost, end=' | ')
    print()
    print('|' + '-' * (6 * len(brokers) - 1) + '|')


def print_dijkstra_chains(paths, costs, edges, source):
    """Print the routing chain from source to each target, with costs"""
    for target in sorted(paths.keys()):
        chain = [target]
        path = paths[target][1]
        while path:
            chain.append(path[0])
            path = path[1]
        print(source, '-->', target,
              'costs', costs[target],
              '|', source, end='')
        last = source
        for broker in chain[-2::-1]:
            for edge in edges:
                if edge[:2] in ((last, broker), (broker, last)):
                    cost = edge[2]
                    break
            print(' --' + str(cost) + '--> ' + str(broker), end='')
            last = broker
        print()


def print_dijkstra_state(targets, paths, costs):
    """Print the current set of brokers and costs for each target"""
    print('| ', end='')
    for target in sorted(targets):
        if target not in paths:
            broker = '-1'
        elif not paths[target][1]:
            broker = str(-1 if target not in paths else paths[target][0])
        else:
            broker = str(-1 if target not in paths else paths[target][1][0])
        cost = str(float('inf') if target not in costs else costs[target])
        print(' ' * (2 - len(broker)) + broker + ',' +
              ' ' * (3 - len(cost)) + cost, end=' | ')
    print()
    print('|' + '-' * (6 * len(targets) - 1) + '|')


if __name__ == '__main__':
    edges = [(1, 2, 2),  # (node1, node2, cost)
             (1, 7, 3),
             (2, 3, 1),
             (3, 4, 8),
             (4, 5, 1),
             (5, 1, 4),
             (5, 6, 2),
             (5, 7, 1),
             (6, 7, 4)]
    source = 3
    print('\nBellmanFord:')
    brokers, costs = bellman_ford(edges, source)
    print_bellman_chains(brokers, costs, edges, source)
    print('\nDijkstra:')
    paths, costs = dijkstra(edges, source)
    print_dijkstra_chains(paths, costs, edges, source)
