import networkx as nx
import time
import sys


from utils import read_graphml_file
from utils import threshold_graph

#from net_enlightener import *

def print_graph(G, out_filename):
    out_filepath = '/home/shridhar/Acads/5245/net-enlightenment/python/intermediate_graphs/' + out_filename
    nx.write_graphml(G,out_filepath)

def main(args):
    filename = sys.argv[1]
    filepath = '/home/shridhar/Acads/5245/net-enlightenment/python/graphml-data/' + filename + '.graphml' 

    G1 = read_graphml_file(filepath)

    print G1.nodes()
    print "number of edges = ", len(G1.edges())

    G_dedup = threshold_graph(G1, 0)
    print G_dedup.nodes()
    print "number of edges = ", len(G_dedup.edges())

    for i in range(1,3):
        thresh = i/10.0
        G_thresh = threshold_graph(G1, thresh)
        print_graph(G_thresh,filename +"thresh-"+str(thresh) + ".graphml")
         

    #filename = '/home/shridhar/Acads/5245/net-enlightenment/python/graphml-data/113_session_2.graphml' 
    #G2 = read_graphml_file(filename)
    #print G2.nodes()

if __name__ == "__main__":
    main(sys.argv)
