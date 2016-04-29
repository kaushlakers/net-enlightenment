import networkx as nx
import time
import sys
import random
#from mcl_clustering import mcl

from utils import read_graphml_file
from utils import threshold_graph

#from net_enlightener import *

def print_edgelist_graph(G, out_filename):
    out_filepath = '/home/shridhar/Acads/5245/net-enlightenment/python/intermediate_graphs/' + out_filename
#    nx.write_graphml(G,out_filepath)
    nx.write_edgelist(G,out_filepath)

def print_graphml_graph(G, out_filename):
    out_filepath = '/home/shridhar/Acads/5245/net-enlightenment/python/intermediate_graphs/' + out_filename
    nx.write_graphml(G,out_filepath)
#    nx.write_edgelist(G,out_filepath)

def main(args):
    filename = sys.argv[1]
    filepath = '/home/shridhar/Acads/5245/net-enlightenment/python/graphml-data/' + filename + '.graphml' 

    G1 = read_graphml_file(filepath)

    print G1.nodes()
    print "number of edges = ", len(G1.edges())

    G_list = []
    num_certain_graphs_generated = 100

    #generate a bunch of certain graphs based on probability
    for i in range(0,num_certain_graphs_generated):
        G = nx.DiGraph()
        for u,v in G1.edges():
            if not G.has_edge(u,v):
                edge_dict = G1[u][v]
                if "weight" not in edge_dict:
                    edge_dict = edge_dict[0]
                if edge_dict['weight']:
                    if random.random() < edge_dict['weight']:
                        G.add_edge(u, v, weight=edge_dict['weight'])
        #M, clusters = networkx_mcl(G, expand_factor = 2,inflate_factor =2 , max_loop = 60,mult_factor = 2)
        #print "output matrix = ", M
        #print "cluster node mapping:", clusters

        G_list.append(G)

    for i in range(0,len(G_list)):
        print_edgelist_graph(G_list[i], filename + "-certain-" + str(i) + ".edgelist")
        print_graphml_graph(G_list[i], filename + "-certain-" + str(i) + ".graphml")
    
    G_dedup = threshold_graph(G1, 0)
    print G_dedup.nodes()
    print "number of edges = ", len(G_dedup.edges())

    for i in range(1,3):
        thresh = i/10.0
        G_thresh = threshold_graph(G1, thresh)
        print_edgelist_graph(G_thresh,filename +"thresh-"+str(thresh) + ".edgelist")
        print_graphml_graph(G_thresh,filename +"thresh-"+str(thresh) + ".graphml")

    #filename = '/home/shridhar/Acads/5245/net-enlightenment/python/graphml-data/113_session_2.graphml' 
    #G2 = read_graphml_file(filename)
    #print G2.nodes()

if __name__ == "__main__":
    main(sys.argv)
