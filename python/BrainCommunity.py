import networkx as nx
import numpy as np
import os
import sys
from utils import *
from mcl_clustering import networkx_mcl
from igraph import *
import pandas as pd
import community

def get_mcl_communities(G):
    M, clusters = networkx_mcl(G, max_loops=100)
    node_map = convert_to_node_comm_map(clusters)
    return node_map

def get_modularity(G, node_com_map):
    #writing to gml file to read using igraph
    nx.write_graphml(G, "temp.gml")

    ig_G = GraphBase.Read_GraphML("temp.gml")
    os.remove("temp.gml")

    return ig_G.modularity(node_com_map)


def run_on_all_graphs(dir):
    df = pd.DataFrame(columns=["Naive_mcl", "prob_mcl"])
    for file in os.listdir(dir):
        print "Working on file " + file
        index = file.split(".")

        G = read_graphml_file(file)
        G = remove_dups(G)

        #mcl using probabilities as weights
        prob_mcl_com_map = get_mcl_communities(G)
        df.loc[index]["prob_mcl"] = get_modularity(G, prob_mcl_com_map)


        #mcl using naive thresholding
        G1 = threshold_graph(G, 0.3)
        thresh_mcl_com_map = get_mcl_communities(G1)
        df.loc[index]["Naive_mcl"] = get_modularity(G, thresh_mcl_com_map)

    return df

def main(argv):
    df = run_on_all_graphs(argv[1])

    df.to_csv("mod_results.csv")

if __name__ == "__main__":
    main(sys.argv)


