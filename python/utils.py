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


def remove_dups(G1):
    G = nx.DiGraph()
    for u,v in G1.edges():
        if not G.has_edge(u,v):
            edge_dict = G1[u][v]
            if "weight" not in edge_dict:
                edge_dict = edge_dict[0]
            G.add_edge(u, v, weight=edge_dict['weight'])
    return G

def threshold_graph(G1, thresh):
    G = nx.DiGraph()
    for u,v in G1.edges():
        if not G.has_edge(u,v):
            edge_dict = G1[u][v]
            if "weight" not in edge_dict:
                edge_dict = edge_dict[0]
            if edge_dict['weight'] > thresh:
                G.add_edge(u, v)
    return G


def convert_to_node_comm_map(comm_dict):
    node_com_map = {}
    for comm in comm_dict:
        for node in comm_dict[comm]:
            node_com_map[node] = comm

    return node_com_map