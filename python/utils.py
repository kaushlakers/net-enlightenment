#Utility functions for reading/visualizing graphs in different formats

import networkx as nx
from pylab import show
import time


def read_graphml_file(file):
    return nx.read_graphml(file)


#visualizes a networkx graph object
def plot_graph(G):
    pos = nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,node_color='b',alpha=0.2,node_size=8)
    nx.draw_networkx_edges(G,pos,alpha=0.1)
    show()


'''
removes edges below a given threshold. Also removes duplicate edges between
2 nodes. Returns a new graph object
'''
def threshold_graph(G1, thresh):
    edge_weights = []
    G = nx.DiGraph()
    for u,v in G1.edges():
        if not G.has_edge(u,v):
            edge_dict = G1[u][v]
            if "weight" not in edge_dict:
                edge_dict = edge_dict[0]
            if edge_dict['weight'] > thresh:
                G.add_edge(u, v, weight=edge_dict['weight'])
    return G
