#!/usr/bin/python
import networkx as nx
import random
from net_enlightener import create_comm_node_mapping
from net_enlightener import create_node_comm_mapping
from utils import read_graphml_file 

cntt =0

def weighted_cons (Glist, nodeClusterList, numnodes):
    clust_rel_list =[]		#used for total list of each set's cluster relience
    totalSets = len(Glist)	
    for k in range(0,totalSets):			#iterate over each set of node cluster dictionaries (dictionary within list)
        totalNodes = len(nodeClusterList[k])
        print 'on set ', k, 'total nodes = ', totalNodes
        
        clust_rel_dict= {}				#contains this sets cluster relience
        sp_sum_dict = {}				#used for relience eq numerator
        clust_size_dict= {}				#used for the relience eq denominator 
        diameter =0
        for i in range(0,totalNodes):	#iterate over each node (element within dictionary)
            clust = nodeClusterList[k][i]
            print 'node ', i, 'cluster ', clust
            if(clust_size_dict.get(clust)):			#if the cluster already exists, increase size
                clust_size_dict[clust]+=1
            else:									#otherwise initialize cluster 
                clust_size_dict[clust] = 1	
                sp_sum_dict[clust] = 0
                clust_rel_dict[clust] = 0

            for j in range(i+1,len(nodeClusterList[k])):				#iterate over each node pair
                if(clust == nodeClusterList[k][j]):	#if the pair is in the same cluster, perform sp calculations
                    shortest_path_len= 0
                    try:
                        shortest_path_len = (len(nx.shortest_path(Glist[k],source='n'+str(i),target='n'+str(j)))-1)
                        sp_sum_dict[clust] += shortest_path_len
                    except:
                        #do nothing
                        pass
                    diameter = max(diameter, shortest_path_len)
        for cluster in clust_rel_dict:				#computes the reliability for each cluster
            
            if(sp_sum_dict[cluster] !=0):
                clust_rel_dict[cluster] = 1.0/(sp_sum_dict[cluster]/(clust_size_dict[cluster] * 1.0 * diameter))
                #clust_rel_dict[cluster] = 1.0/(sp_sum_dict[cluster]/(clust_size_dict[cluster] * 1.0 * nx.diameter(Glist[k])))
            else:
                clust_rel_dict[cluster] = 0 		#not sure what to do here: when there is only 1 node in a 
                                                    #cluster the relience equals infinity (divide by 0)
        clust_rel_list.append(clust_rel_dict)		#adds reliability to a list for consensus

    #after reliability is computed for every set and every cluster, the weight of each edge is computed
    weighted_edge_list = []
    for i in range(0,numnodes):							#initialization step for weighted edge list
        for j in range(i+1,numnodes):					#made a tuple to for networkx to iterate over
            weighted_edge_list.append((i,j,{'weight':0.0}))
    for p in range(0,totalSets):							#summation step for weights
        index = 0
        for i in range(0,numnodes):
            for j in range(i+1,numnodes):
                if(nodeClusterList[p][i] == nodeClusterList[p][j]):
                    weight = clust_rel_list[p][nodeClusterList[p][i]]
                    weighted_edge_list[index][2]['weight'] += weight
                index+=1
    return weighted_edge_list

#tests
path = "/home/shridhar/Acads/5245/net-enlightenment/python/intermediate_graphs/"
orig_graph_name = "127_session_2"
num_sets = 10
num_nodes = 116
Glist = []
n_c_map_list = []
for i in range(0,num_sets):
    graph_file = path+orig_graph_name + "-certain-" + str(i) + ".graphml"
    G = read_graphml_file(graph_file)
    community_file = path+orig_graph_name+"-certain-" + str(i) + ".edgelist.txt.communities"

    c_n_map = create_comm_node_mapping(G,community_file,False)
    n_c_map = create_node_comm_mapping(c_n_map)
    Glist.append(G)
    n_c_map_list.append(n_c_map)

final_map = weighted_cons(Glist, n_c_map_list, num_nodes)
G = nx.from_edgelist(final_map)
out_f = orig_graph_name+"consensus_weighted_graph.gexf"
nx.write_gexf(G,out_f)

#for tup in final_map:
#    out_f.write(str(tup)+"\n")
#print ("\n".join(final_map))

'''
list = []
for i in range (0,100):
    dict={}
    for j in range(0,115):
        dict[j] = random.randint(0,20) 
    list.append(dict)
list
#G = nx.complete_graph(115)
Glist= []
for i in range(0,6):
    G = nx.gnp_random_graph(115,0.5)
    Glist.append(G)

weighted_cons(Glist,list)'''
