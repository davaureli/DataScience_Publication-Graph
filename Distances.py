import networkx as nx
import math
from heapq import heappush, heappop

# Calculate Jaccard distance between two sets of publications of two authors
def jaccard(id1,id2, authors_dict):
    list1 = []
    list2 = []
    # take publications
    for t in authors_dict[id1][1]:
        list1.append(t[1])
    for t in authors_dict[id2][1]:
        list2.append(t[1])
    # calculate Jaccard distance
    j = float(len(set(list1).intersection(set(list2))))/(len(set(list1).union(list2)))
    return j


# Hop distance algorithm
def bfs(G, id, distance):
    visited = {}         #level (number of hops) when seen in BFS
    height = 0         #the current level
    unexplored={id:1}  #dict of nodes to check at next level
    while unexplored and not (distance+1 <= height):
        thislevel = unexplored  #advance to next level
        unexplored = {}         #and start a new list (fringe)
        for elem in thislevel:
            if elem not in visited:
                visited[elem] = height  #set the level of vertex v
                unexplored.update(G[elem])  #add neighbors of v
        height = height+1
    hopGraph = G.subgraph(visited.keys())
    nx.set_node_attributes(hopGraph, 'level', visited)
    return hopGraph


# Weight of shortest path with Dijkstra algorithm
def Dijkstra(graph, s):
    A = {node: None for node in graph.nodes()} #dictionary with nodes id and shortest paths weight
    queue = [(0, s)]  #heap of weight and starting node
    while queue:
        weight, v = heappop(queue)  #pop and return the smallest item from queue
        if A[v] is None:  #if node v is unvisited add it to the dictionary
            A[v] = weight
            for w, edge_len in graph[v].items():
                if A[w] is None:
                    heappush(queue, (weight + edge_len['weight'], w)) #push values into queue
    return A


# Groupby nodes connected to one node with edges of weight equal to 0
def similarity_dist(G):
    Similarity_dist = {}
    lista = nx.nodes(G)
    listadeleted = []

    for node in lista:
        if node not in listadeleted:
            for node2 in lista:
                if node2 != node and node2 in G.neighbors(node) and node2 not in listadeleted:
                    if node not in Similarity_dist and G[node][node2]['weight'] == 0:
                        Similarity_dist[node] = [node2]
                        listadeleted.append(node2)
                    elif node in Similarity_dist and G[node][node2]['weight'] == 0 and node2 not in listadeleted:
                        Similarity_dist[node].append(node2)
                        listadeleted.append(node2)
    return Similarity_dist


# Obtain the key node for the destination nodes
def get_keynode(destination_nodes, similarity_dist):
    new_dest = []
    for dest in destination_nodes:
        enter = False
        for k,v in similarity_dist.items():
            if dest in v:
                new_dest.append(k)
                enter = True
                break
        if enter == False:
            new_dest.append(dest)
    return new_dest


# Get Group Number
def groupNumber(G, destination_nodes, shortest_paths):
    for node in G.nodes():
        lista = []

        i = 0
        for dictionary in shortest_paths:
            if dictionary[node] != None:
                lista.append((dictionary[node], destination_nodes[i]))
            else:
                lista.append((-(math.inf), destination_nodes[
                    i]))  #if the node cannot reach that specific node we associate to it a big value
            i += 1
        if len(lista) != 0:
            lista.sort(key=lambda x: x[0])
            minimo = lista[-1][0]
            if minimo == -(math.inf):
                print('This node ' + str(node) + ' cannot reach any node of the list.')
            else:
                for i in range(1, len(lista)):
                    if lista[-i][0] == minimo:

                        print('The shortest path for node ' + str(node) + ' is ' + 'destination: ' + str(
                            lista[-i][1]) + ' with cost: ' + str(lista[-i][0]))
                    else:
                        break
