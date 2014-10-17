'''
Bellman-Ford and Dijkstra Shortest-Path Routing Algorithms

This pretty-prints calculation and routing tables for user-defined networks.
The "broker" is the optimal node to go through for a given destination.
The "cost" is the quantity to minimize for each path, as a sum of edge costs.

.. author:: Jan Van Bruggen <jancvanbruggen@gmail.com>
'''

from heapq import heappush, heappop

def bellman_ford(Edges, Source):
    '''Return two dictionaries of node IDs keying to broker node IDs and costs
       for the shortest paths to each node, using the Bellman-Ford algorithm'''
    Brokers, Costs = {}, {}
    Nodes = []
    for Edge in Edges:
        for Node in Edge[:2]:
            if Node not in Nodes:
                Nodes.append(Node)
                # Initialize the broker as -1, except as source for source
                Brokers[Node] = Source if Node is Source else -1
                # Initialize the cost as infinite, except as 0 for source
                Costs[Node] = 0 if Node is Source else float('inf')
    print_destinations(Brokers.keys())
    print_bellman_state(Brokers, Costs)
    # Iterate the maximum number of times needed to converge
    for Edge in Edges * (len(Nodes) - 2):
        Node1, Node2, Cost = Edge
        # Check the edge in both directions
        for Sender, Receiver in ((Node1, Node2), (Node2, Node1)):
            # If the new path to the receiver is cheaper, save the path
            if Costs[Sender] + Cost < Costs[Receiver]:
                Brokers[Receiver] = Sender
                Costs[Receiver] = Costs[Sender] + Cost
        print_bellman_state(Brokers, Costs)
    return Brokers, Costs

def dijkstra(Edges, Source):
    '''Return two dictionaries of node IDs keying to broker node IDs and costs
       for the shortest paths to each node, using Dijkstra's algorithm'''
    Paths, Costs = {}, {}
    Seen = set()
    Unseen = [(0, Source, ())]
    # All nodes (for print table)
    All = list(set(Edge[i] for Edge in Edges for i in (0, 1)))
    print_destinations(All)
    print_dijkstra_state(All, Paths, Costs)
    # While nodes remain in the Unseen heap
    while Unseen:
        # Get the next node from the heap
        Cost, Node1, Path = heappop(Unseen)
        # If the node is unseen, save the path and check neighboring nodes
        if Node1 not in Seen:
            Seen.add(Node1)
            Path = (Node1, Path)
            # Save the optimal path and cost
            Paths[Node1] = Path
            Costs[Node1] = Cost
            # Check all neighboring nodes
            for Edge in [Edge for Edge in Edges if Node1 in Edge[:2]]:
                EdgeCost = Edge[2]
                # Find the edge's other node
                Node2 = Edge[0] if Edge.index(Node1) else Edge[1]
                if Node2 not in Seen:
                    # Add the unseen other node to the Unseen heap
                    heappush(Unseen, (Cost + EdgeCost, Node2, Path))
        print_dijkstra_state(All, Paths, Costs)
    return Paths, Costs

def print_destinations(Destinations):
    '''Print all destinations'''
    print('_' * 64)
    print('| ', end='')
    for Destination in sorted(Destinations):
        print('  ' + str(Destination) + '   ', end=' | ')
    print()
    print('|' + '-' * 62 + '|')

def print_bellman_chains(Brokers, Costs, Edges, Source):
    '''Print the routing chain from Source to each destination, with Costs'''
    for Destination in sorted(Brokers.keys()):
        Chain = [Destination]
        Next = Destination
        while Chain[-1] is not Source:
            Chain.append(Brokers[Next])
            Next = Brokers[Next]
        print(Source, '-->', Destination, 'costs', Costs[Destination], '|', Source, end='')
        Last = Source
        for Broker in Chain[-2::-1]:
            for Edge in Edges:
                if Edge[:2] in ((Last, Broker), (Broker, Last)):
                    Cost = Edge[2]
                    break
            print(' --' + str(Cost) + '--> ' + str(Broker), end='')
            Last = Broker
        print()

def print_bellman_state(Brokers, Costs):
    '''Print the current set of Brokers and Costs for each destination'''
    print('| ', end='')
    for Destination in sorted(Brokers.keys()):
        Broker = str(Brokers[Destination])
        Cost = str(Costs[Destination])
        print(' ' * (2 - len(Broker)) + Broker + ',' +
              ' ' * (3 - len(Cost)) + Cost, end=' | ')
    print()
    print('|' + '-' * 62 + '|')

def print_dijkstra_chains(Paths, Costs, Edges, Source):
    '''Print the routing chain from Source to each destination, with Costs'''
    for Destination in sorted(Paths.keys()):
        Chain = [Destination]
        Path = Paths[Destination][1]
        while Path:
            Chain.append(Path[0])
            Path = Path[1]
        print(Source, '-->', Destination, 'costs', Costs[Destination], '|', Source, end='')
        Last = Source
        for Broker in Chain[-2::-1]:
            for Edge in Edges:
                if Edge[:2] in ((Last, Broker), (Broker, Last)):
                    Cost = Edge[2]
                    break
            print(' --' + str(Cost) + '--> ' + str(Broker), end='')
            Last = Broker
        print()

def print_dijkstra_state(Destinations, Paths, Costs):
    '''Print the current set of brokers and Costs for each destination'''
    print('| ', end='')
    for Destination in sorted(Destinations):
        if Destination not in Paths:
            Broker = '-1'
        elif not Paths[Destination][1]:
            Broker = str(-1 if Destination not in Paths else Paths[Destination][0])
        else:
            Broker = str(-1 if Destination not in Paths else Paths[Destination][1][0])
        Cost = str(float('inf') if Destination not in Costs else Costs[Destination])
        print(' ' * (2 - len(Broker)) + Broker + ',' +
              ' ' * (3 - len(Cost)) + Cost, end=' | ')
    print()
    print('|' + '-' * 62 + '|')

# Edge: (Node1, Node2, Cost)
Edges = [(1,2,2),
         (1,7,3),
         (2,3,1),
         (3,4,8),
         (4,5,1),
         (5,1,4),
         (5,6,2),
         (5,7,1),
         (6,7,4)]
Source = 3

print('BellmanFord:')
Brokers, Costs = bellman_ford(Edges, Source)
print_bellman_chains(Brokers, Costs, Edges, Source)
print()
print('Dijkstra:')
Paths, Costs = dijkstra(Edges, Source)
print_dijkstra_chains(Paths, Costs, Edges, Source)
