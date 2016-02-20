from sets import Set
import sys
import networkx as nx
import math
#import community
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
    

def create_comm_node_mapping(G, filename, isMetis):
    
    comm_n_dict = {}
    print filename
    if isMetis:
        #file is in a list of communities, with each line having exactly 1 community. mapping is line number == node number

        with open(filename) as f:
            node_num = 1
            for line in f:
                comm_id = int(line)
                if comm_id in comm_n_dict:
                    comm_n_dict[comm_id].append(node_num)
                else:
                    comm_n_dict[comm_id] = [node_num]
                node_num += 1

    else:
        with open(filename) as f:
            for line in f:
                if line[0] != '#':
                    node_num, comm_id = [int(x) for x in line.split()]
                    if comm_id in comm_n_dict:
                        comm_n_dict[comm_id].append(node_num)
                    else:
                        comm_n_dict[comm_id] = [node_num]
#                else:
 #                   print line
    print len(comm_n_dict)
    return comm_n_dict


def create_node_comm_mapping(comm_n_dict):

    n_comm_dict = {}
    for comm_id, nodes in comm_n_dict.iteritems():
        for node in nodes:
            if node not in n_comm_dict:
                n_comm_dict[node] = comm_id
            else:
                print 'this should not be printed. same node detected twice!'
    print len(n_comm_dict)
    return n_comm_dict

def calculate_entropy_of_youtube_communities(GT_filename, comm_n_dict):
    node_comm_GT_dict = {}
    with open(GT_filename) as f:
        comm_id = 0
        for line in f:
            for node_st in line.split():
                node = int(node_st)
                if node in node_comm_GT_dict :
                    node_comm_GT_dict[node].add(comm_id)
                else:
                    node_comm_GT_dict[node] = Set([comm_id])
        comm_id +=1

    num_nodes_GT = len(node_comm_GT_dict)
    comm_id = 0
    comm_entropies = {}
    entropy = 0
    for comm, nodes in comm_n_dict.iteritems():
        gtcomm_weighted_n_map = {}
        comm_entropy = 0
        unique_nodes_in_comm = 0
        for node in nodes:
            if node in node_comm_GT_dict:
                unique_nodes_in_comm+=1
                for gtcomm in node_comm_GT_dict[node]:
                    if gtcomm in gtcomm_weighted_n_map:
                        gtcomm_weighted_n_map[gtcomm] += 1/float(len(node_comm_GT_dict))
                    else:
                        gtcomm_weighted_n_map[gtcomm] = 1/float(len(node_comm_GT_dict))

        for distinct_comm in gtcomm_weighted_n_map:
            probability = gtcomm_weighted_n_map[distinct_comm]/float(unique_nodes_in_comm)
            comm_entropy += -1*probability*math.log(probability)
        entropy += (comm_entropy)*len(nodes)/float(num_nodes_GT)

    print 'entropy of clustering is ' + str(entropy)
#    print "len = " + str(len(node_comm_GT_dict))
#    print 'num_comms =' + str(comm_id)

def calculate_component_community_dict(G, comm_n_dict):
    
    components = nx.connected_components_subgraphs(G)
    comp_comm_dict = {}
    comp_dict = {}
    i = 0
    for comp in components:
        comp_dict[i] = comp
        comp_comm_dict[i] = []
        for comm in comm_n_dict:
            if len(set(comm_n_dict[comm]) - comp) <= 5:
                comp_comm_dict[i].append(comm) 
        i = i+1

    return (comp_dict, comp_comm_dict)

def calculate_component_wise_measures(G, comm_n_dict):

    comp_graphs = list(nx.connected_component_subgraphs(G))
    comp_wise_conductance = {}
    comp_wise_ncut = {}
    #comp_wise_conductance = {i:{} for i in range(len(comp_graphs))}
    i = 0
    
    for comp_id in range(len(comp_graphs)):
        graph = comp_graphs[comp_id]
        if len(list(graph.nodes())) > 1:
            for comm in comm_n_dict:
                if set(comm_n_dict[comm]).issubset(set(graph.nodes())) and len(list((graph.nodes()))) > len(comm_n_dict[comm]) and len(comm_n_dict[comm]) > 1:
                    if comp_id not in comp_wise_conductance:
                        comp_wise_conductance[comp_id] = {}
                    comp_wise_conductance[comp_id][comm] = nx.conductance(graph, comm_n_dict[comm])

    #print comp_wise_conductance
    comp_min_conductance = {}
    comp_num_communities = {}
    for comp_id in comp_wise_conductance:
        #print comp_wise_conductance[comp_id]
        if len(comp_wise_conductance[comp_id]) > 0:
            #comp_min_conductance[comp_id] = sum(comp_wise_conductance[comp_id].values())/ len(comp_wise_conductance[comp_id])
            comp_num_communities[comp_id] = len(comp_wise_conductance[comp_id])
            comp_min_conductance[comp_id] = sorted(comp_wise_conductance[comp_id].items(), key=lambda x: x[1])[0][1]
    

    return min(comp_min_conductance.values())


def calculate_component_wise_ncut(G, comm_n_dict):

    comp_graphs = list(nx.connected_component_subgraphs(G))
    comp_wise_conductance = {}
    comp_wise_ncut = {}
    #comp_wise_conductance = {i:{} for i in range(len(comp_graphs))}
    i = 0
    
    for comp_id in range(len(comp_graphs)):
        graph = comp_graphs[comp_id]
        if len(list(graph.nodes())) > 1:
            for comm in comm_n_dict:
                if set(comm_n_dict[comm]).issubset(set(graph.nodes())) and len(list((graph.nodes()))) > len(comm_n_dict[comm]) and len(comm_n_dict[comm]) > 1:
                    if comp_id not in comp_wise_conductance:
                        comp_wise_conductance[comp_id] = {}
                    comp_wise_conductance[comp_id][comm] = nx.normalized_cut_size(graph, comm_n_dict[comm])

    #print comp_wise_conductance
    comp_min_conductance = {}
    comp_num_communities = {}
    for comp_id in comp_wise_conductance:
        #print comp_wise_conductance[comp_id]
        if len(comp_wise_conductance[comp_id]) > 0:
            comp_min_conductance[comp_id] = sum(comp_wise_conductance[comp_id].values())/ len(comp_wise_conductance[comp_id])
            comp_num_communities[comp_id] = len(comp_wise_conductance[comp_id])
            #comp_min_conductance[comp_id] = sorted(comp_wise_conductance[comp_id].items(), key=lambda x: x[1])[0][1]
    
    #print comp_wise_conductance
    return sum(comp_min_conductance.values())/len(comp_min_conductance.values())

def calculate_community_measures(G, comm_n_dict, n_comm_map):
    
    communities = comm_n_dict.keys()
    graph_nodes = G.nodes()
    conductance = {}
    n_cuts = {}

    comp_conductance_dict = {}

    #comp_dict, comp_comm_dict = calculate_component_community_dict(G, comm_n_dict)

    '''
    for comp in comp_dict:
        conductance[comp] = {}
        for comm in comp_comm_dict[comp]:
            comm_nodes = comm_n_dict[comm]
            residual_nodes = list(comp_dict[comp] - set(comm_nodes))
            conductance[comp][comm] = nx.conductance(G, comm_nodes, residual_nodes)
    '''
    print "COnductance is " + str(calculate_component_wise_measures(G, comm_n_dict))
    print "Ncut is " + str(calculate_component_wise_ncut(G, comm_n_dict))
    measures = {}
    #measures['conductance'] = sorted(conductance.items(), key=lambda x: x[1])[0][1]
    print "Modularity is " + str(community.modularity(n_comm_map, G))
    


def main(args):

    directed = False #(sys.argv[2].upper() == 'DIRECTED')

    isMetis = False
    if "adjlist" in sys.argv[1].split("."):
        isMetis = True

    create_using = nx.DiGraph() if directed else nx.Graph()

    G = None
    if isMetis:
        G=nx.read_adjlist(sys.argv[1], nodetype=int)
    else:    
        G = nx.read_edgelist(sys.argv[1], create_using=create_using, nodetype=int)

    #print G.n

    #calculate_centrality_measures(G, create_using, directed)
    #isMetis = False
    comm_n_dict = create_comm_node_mapping(G, sys.argv[3], isMetis)
    n_comm_map = create_node_comm_mapping(comm_n_dict)
    #print comm_n_dict
    #print n_comm_map
    calculate_community_measures(G, comm_n_dict, n_comm_map)

    if(len(sys.argv) == 5):
        calculate_entropy_of_youtube_communities(sys.argv[4], comm_n_dict)
    
    
if __name__ == "__main__":
    main(sys.argv)
