# ADM--HW4
Homework 4 - Algorithmic Methods of Data Mining

---------------------------------------------------------
----------------    PART 1    --------------------------
---------------------------------------------------------

In this point we have to create a graph G, whose nodes are the authors and they are connected if they 
share at least one publication. To obtain that graph, we initialize three useful dictionary structures which 
contain the information we need:

{author_id: [author_name , [(id_publication, id_publication_int), ...]}

{publication_id: [[authors_id, ...], id_publication_int]}

{conference_id: [id_conference_int, [authors_id, ...]]}

Lookups in lists are O(n), lookups in dictionaries are amortized O(1), with regard to the number of items in the data structure.
A dictionary is a hash table, so it is really fast to find the keys and for this reason we used the above structures.
The edges between the nodes are weighted in the following way: w(a1, a2) = 1 − J(p1, p2)
where a1, a2 are authors, p1 and p2 are the set of publications of the two authors and, J(p1, p2) represents 
the jaccard similarity between these two sets of publications.
To calculate the weight we implemented a function that find the Jaccard similarity.
After obtaining all the necessary information, we constructed the graph adding the authors as nodes and connecting 
them with weighted edges. 


---------------------------------------------------------
----------------    PART 2    --------------------------
---------------------------------------------------------

Given a conference in input, we need to return the subgraph induced by the set of authors who published at the input 
conference at least once. A vertex-induced subgraph is a subset of the vertices of a graph G together with any edges 
whose endpoints are both in this subset. To construct this subgraph we took information from the conference dictionary 
mentioned above, considering just the authors which participated to a certain conference with a publication and adding them as nodes.

Once obtained the subgraph we can calculate some centrality measures, which give us relative measures of importance in the network. 
We can consider different measures since each of them measures a different type of 'importance'.
The degree centrality corresponds to the number of connections normalized by dividing by the maximum possible degree, which is in a simple graph n-1 (n represents the number of nodes in G).
The closeness centrality of a node is the reciprocal of the sum of the shortest path distances from that node to all n-1 other 
nodes and since the sum depends on the number of nodes in the graph, the closeness is normalized by the sum of minimum possible 
distances n-1. Remark that our graph is disconnected but the algorithm we used computes the measure for each connected part separately.
The betweeness centrality of a node is the sum of the fraction of all-pairs shortest paths that pass through that node.

On the second point of this part we need to create a subgraph induced by the nodes that have hop distance at most equal to a certain given 
distance from a particular author. Hop distance corresponds to the number of edges from one node to another. 
For doing this we implemented a breadth-first search algorithm for traversing the graph, which explores first the neighbor nodes 
and after pass to the next level of neighbours. 


---------------------------------------------------------
----------------    PART 3    --------------------------
---------------------------------------------------------

The aim of this part is to obtain the weight of the shortest path that connects an author with Aris. The weight is calculated, 
as said in part 1, with Jaccard similarity. 
First of all we retrieved the ids of the authors we want to consider and after we used an algorithm that computed the shortest path 
between the starting point and the arrival point. To improve and speed up this procedure, we implemented a function, based on Dijkstra's 
algorithm, that calculates the weight of all the possible shortest paths from a given starting node (Aris) and creates a dictionary in 
which the keys are all nodes in our graph and the values correspond to the path's weight. 
After obtaining this structure is enough to search our destination node and get the cost of the shortest path with Aris.

Now we have to generalize the previous point, but at the same time start to think about the optimization for our code. In fact now we 
have as input all the nodes in the graph and as destination a list of nodes, not just one. 
We have to calculate for each node v of the graph, its GroupNumber defined as the min{ShortestPath(v,u)}, where u are the nodes included 
in an input set of nodes. The initial idea  was to reduce the number of nodes in the graph to decrease the number of path calculations, 
removing for example the nodes with degree equal to 0 (disconnected nodes) or summarizing all the nodes connected with others through an 
edge weighted 0. If we think at the problem in a different way, we can use the same logic mentioned above, computing all possible shortest path's 
for our nodes in the input set with Dijkstra's algorithm. We collect all the paths, for a specific node, in a list of tuples and finally we compute 
the minimum distance returning the GroupNumber.
We also inserted some controls if the input set respects the limit of 21 nodes and if all of those nodes are in the graph.

---------------------------------------------------------
----------------    MODULES   --------------------------
---------------------------------------------------------

###   Module 'Distances'  ###

This module contains functions concerning distances.

The function 'jaccard' calculates the Jaccard distance between two sets of publications of two authors.
It takes in input the ids of two authors and a dictionary containing the information about the authors 
and returns the distance required. 
The Jaccard distance is calculated as the intersection of two sets divided by their union.

The function 'bfs' is an implementation of the algorithm bfs, that consider the nodes until a certain level from 
a given starting node. The parameters in input corresponds to a graph, the id of the starting node and the hop distance which we want to consider.
The mechanism is that it considers the neighbours of the starting node and adds them to a list, after it skips to the 
second step where it considers the neighbours of the nodes visited at the previous one and add them to the list if they are not
 already present and it repeats this procedure until it reaches the level of the distance given.
The function at the end return a subgraph with the visited nodes in a certain distance and each node has an attribute with containing its level.

The function 'Dijkstra' is an implementation of the Dijkstra's algorithm for finding the weight of the shortest path between nodes. It finds 
the shortest path between one node and all the others given in input a graph and a starting node. As first thing it creates a dictionary with the 
nodes of the graph as keys and as values it will take the weight of the shortest path. The logic behind the computation of the shortest paths is 
based on a heap structure, which is a tree based structure where the parent node as a value smaller than or equal to the one of the child node. 
We initialize the structure with the weight 0 and the starting node and until we have nodes to visit we compute the path. After visiting each node, 
a faster way than go through all the edges from all visited nodes, is to compute tentative distances only from the last visited node to its neighbors 
and store them in the heap from which we can obtain the minimum distance.
If there is no connection between the starting node and a given node, the function return as value None.
* More about HEAP: The heap is an integral component in many algorithms — a data structure that keeps elements organised so that it is always easy 
to find the smallest value. The heapq module defines functions for a minheap - which always returns the smallest item. To set up the heap, you add 
values using heappush and remove them using heappop.


The function 'GroupNumber' takes in input the graph, a set of destination nodes and a dictionary with shortest paths. It simply returns the groupNumber 
for each node of the graph, equal to the minimum of the shortest path between the node of the graph and the nodes in the given list. This value is 
found appending to a list the nodes for which exists a shortest path and ordering the costs of this shortest path.

(The functions 'similarity_dist' and 'get_keynode' will be useful if we want to reduce the number of nodes in a graph.)



###   Module 'Centrality_measures_plots'   ###

This module contains functions concerning the centrality measures and some pretty plots to show the results of these measures.

The function 'most_important' takes in input a graph and a centrality measure and return a graph with as nodes the 10% of 
nodes which are considered the most important given a certain centrality measure.
The output graph is obtained creating a copy of the original graph and removing the nodes that are not in the top positions 
of the sorted values returned by the centrality measure.

The function 'draw_1' provides a way to show the results of a centrality measure. It takes in input a graph, a graph with the 
most important nodes accordingly to the measure used and the name of that measure.
We obtain a plot where we have the structure of the entire graph with the most important nodes highlighted.

The function 'draw_2' provides a different way to show the results of a centrality measure. It takes in input a graph, the 
centrality measure and its name and return a graph where the nodes are colored with respect to their importance. The color 
scale starts from a clear color, which means more importance and ends with a dark color, which means less importance. 

The function 'draw_3' provides a plot of the hop distance with a color scale associated to node distance from a starting node. 
It takes as imput also the the id and the name of the author (identification of the starting node) to create an appositely label on the graph.
The dimensions of the nodes are proportionally to the number of connections they have with the other nodes.
The function 'draw_3_bis' is just a light and faster version (for huge distances) of the previous one, where we don't consider different 
colors for each level of nodes but simply a color for the starting node and one for all the others. 
