import sys
import networkx as nx
import community
#import numpy as np
#import plotly.plotly as py 
#import plotly.graph_objs as go


#indent using spaces plz

#plots a histogram on plotly. I did it from ipython notebook
def plot_histogram(cent_list, filename='histogram'):
    data = [
        go.Histogram(
            x=[node[1] for node in cent_list.items()]
        )
    ]
    layout = go.Layout(
        xaxis=dict(
            autorange=True
        ),
        yaxis=dict(
            autorange=True
        )
    )
    plot_url = py.plot(data, layout=layout, filename=filename)


def get_top_keys(dictionary, top):
    items = dictionary.items()
    items.sort(reverse=True, key=lambda x: x[1])
    
    return map(lambda x: x[0], items[:top])

def get_common_nodes_across_measures(cent_dict, top_n):
    common_nodes = set()
    i = 0
    for key, value in cent_dict.iteritems():
        if i == 0:
            common_nodes = common_nodes.union(get_top_keys( value, top_n))
            i += 1
        else:
            common_nodes = common_nodes.intersection(get_top_keys( value, top_n))
            
    return common_nodes

def print_dict(cent_dict):
    for measure, value_dict in cent_dict.iteritems():
        print "Values for "+measure
        for node, value in sorted(value_dict.iteritems()):
            print str(node) + "\t" + str(value)
        print "\n\n\n"

def print_tsv(cent_dict):
    nodes = cent_dict[cent_dict.keys()[0]].keys()
    measures = cent_dict.keys()
    for measure in measures:
        print measure + "\t",
    print 
    for node in sorted(nodes):
        print str(node) + '\t',
        for measure in measures:
            print str(cent_dict[measure][node]) + "\t",
        print 
    
    
def is_connected(G, directed):
    if directed:
        return nx.is_strongly_connected(G)
    else:
        return nx.is_connected(G)

def calculate_centrality_measures(G, create_using, directed):
    measures = []
    centrality_dict = {}

    #check for directed or undirected
    if (directed):
        centrality_dict['in_degree'] = nx.in_degree_centrality(G)
        centrality_dict['out_degree'] = nx.out_degree_centrality(G)
    else: 
        centrality_dict['degree'] = nx.degree_centrality(G)
    
    #print "Completed degree"

    #calculate harmonic if graph is disconnected
    if is_connected(G, directed):
        centrality_dict['closeness'] = nx.closeness_centrality(G)
    else:
        centrality_dict['harmonic'] = nx.harmonic_centrality(G)

    #print "Completed closeness_centrality"
    
    
    centrality_dict['betweenness'] = nx.betweenness_centrality(G)
    #print "Completed betweenness"

    centrality_dict['eigen'] = nx.eigenvector_centrality(G)

    centrality_dict['pagerank'] = nx.pagerank(G)

    G_prime = G
    if directed:
        G_prime = nx.read_edgelist(sys.argv[1], nodetype=int)
    
    centrality_dict['clustering'] = nx.clustering(G_prime)
    
    print_tsv(centrality_dict)
    

def read_communities(G, filename, isMetis):
    
    comm_dict = {}

    return comm_dict


def calculate_community_measures(G, comm_n_dict, n_comm_map):
    
    communities = comm_n_dict.keys()
    graph_nodes = G.nodes()
    conductance = {}
    modularity = {}
    n_cuts = {}

    for comm in communities:
        comm_nodes = comm_n_dict[comm]
        residual_nodes = list(set(graph_nodes) - set(comm_nodes))
        conductance[comm] = nx.conductance(G, comm_nodes, T=None)
        n_cuts[comm] = nx.    





def main(args):

    directed = False #(sys.argv[2].upper() == 'DIRECTED')

    create_using = nx.DiGraph() if directed else nx.Graph()

    G = nx.read_edgelist(sys.argv[1], create_using=create_using, nodetype=int)
    
    
    #calculate_centrality_measures(G, create_using, directed)
    isMetis = False
    comm_dict = read_communities(G, sys.argv[3], isMetis)
    calculate_community_measures(G, comm_dict)

     
    


    
if __name__ == "__main__":
    main(sys.argv)
