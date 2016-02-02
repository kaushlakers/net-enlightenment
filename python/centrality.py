import sys
import networkx as nx
import numpy as np
import plotly.plotly as py 
import plotly.graph_objs as go


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
        for node, value in value_dict.iteritems():
            print str(node) + "\t" + str(value)
        print "\n\n\n"
    


def main(args):
    G = nx.read_edgelist(sys.argv[1])
    centrality_dict = {}

    #check for directed or undirected
    if (sys.argv[2].upper() == 'DIRECTED'):
        centrality_dict['in_degree'] = nx.in_degree_centrality(G)
        centrality_dict['out_degree'] = nx.out_degree_centrality(G)
    else: 
        centrality_dict['degree'] = nx.degree_centrality(G)
    
    #calculate harmonic if graph is disconnected
    if nx.is_connected(G):
        centrality_dict['closeness'] = nx.closeness_centrality(G)
    else:
        centrality_dict['closeness'] = nx.harmonic_centrality(G)

    centrality_dict['betweenness'] = nx.betweenness_centrality(G)

    centrality_dict['eigen'] = nx.eigenvector_centrality(G)

    centrality_dict['pagerank'] = nx.pagerank(G)

    centrality_dict['clustering'] = nx.clustering(G)
    
    print_dict(centrality_dict)
    
    #this seems to be giving disappointing results 
    #common_central_nodes = get_common_nodes_across_measures(centrality_dict, 1000)

if __name__ == "__main__":
    main(sys.argv)