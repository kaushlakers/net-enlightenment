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