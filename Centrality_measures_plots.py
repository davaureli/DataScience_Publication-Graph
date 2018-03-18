import numpy as np
import networkx as nx
from pylab import show
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from itertools import count


# Consider the top 10% of nodes according to a centrality measure
def most_important(G, measure):
    r = [x[1] for x in measure.items()]
    r_sort = sorted(r)
    Gt = G.copy()
    # take only top 10%
    big = r_sort[int(len(r_sort) * 0.90): len(r_sort)]
    for n,v in measure.items():
        if v not in big:
            Gt.remove_node(n)
    return Gt


# Plot with most important nodes wrt a centrality measure
def draw_1(G, G_imp, measure_name):
    # create the layout
    pos = nx.spring_layout(G)
    # draw the nodes and the edges
    nx.draw_networkx_nodes(G,pos,node_color='b',alpha=0.2,node_size=8)
    nx.draw_networkx_edges(G,pos,alpha=0.1)
    # draw the most important nodes with a different style
    nx.draw_networkx_nodes(G_imp,pos,node_color='r',alpha=0.4,node_size=254)
    # add labels and title
    nx.draw_networkx_labels(G_imp,pos,font_size=9,font_color='b')
    plt.title(measure_name)
    plt.show()


# Plot centrality measure with color scale
def draw_2(G, measures, measure_name):
    # create the layout
    pos = nx.spring_layout(G)
    # draw the nodes, the edges and the labels
    nodes = nx.draw_networkx_nodes(G, pos, node_size=250, cmap=plt.cm.plasma,
                                   node_color=np.array(list(measures.values())).astype(float),
                                   nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1))
    labels = nx.draw_networkx_labels(G, pos, font_size=9)
    edges = nx.draw_networkx_edges(G, pos)
    # add title and color legend
    plt.title(measure_name)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()


# Plot hop distance with color scale associated to node distance
def draw_3(G, id, author):
    # attributes a color to nodes at different distance
    groups = set(nx.get_node_attributes(G,'level').values())
    mapping = dict(zip(sorted(groups),count()))
    nodes = G.nodes()
    colors = [mapping[G.node[n]['level']] for n in nodes]
    # get different label for starting node
    label = {}
    label[id]= author

    pos = nx.spring_layout(G)
    # draw the nodes and the edges
    nodes = nx.draw_networkx_nodes(G,pos,node_color=colors,cmap=plt.cm.viridis, alpha=0.2,node_size=[18 * G.degree(n) for n in G])
    nx.draw_networkx_edges(G,pos,alpha=0.1)
    # draw the most important nodes with a different style
    nx.draw_networkx_nodes(G,pos,node_color='r',alpha=0.4,node_size=1000, nodelist=[id])
    # add labels and title
    nx.draw_networkx_labels(G,pos,label,font_size=14,font_color='b', nodelist=[id])
    plt.title('Hop distance graph')
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()


# Plot hop distance (without clors for each distance)
def draw_3_bis(G, id, author):
    # get different label for starting node
    label = {}
    label[id]= author

    pos = nx.spring_layout(G)
    # draw the nodes and the edges
    nodes = nx.draw_networkx_nodes(G,pos,node_color='b', alpha=0.2,node_size=[18 * G.degree(n) for n in G])
    nx.draw_networkx_edges(G,pos,alpha=0.1)
    # draw the most important nodes with a different style
    nx.draw_networkx_nodes(G,pos,node_color='r',alpha=0.4,node_size=1000, nodelist=[id])
    # add labels and title
    nx.draw_networkx_labels(G,pos,label,font_size=14,font_color='b', nodelist=[id])
    plt.title('Hop distance graph')
    plt.show()
    
