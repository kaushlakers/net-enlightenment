import networkx as nx
import time
import sys


from utils import read_graphml_file

def main(args):
    filename = '/home/shridhar/Acads/5245/net-enlightenment/python/graphml-data/113_session_1.graphml' 

    G1 = read_graphml_file(filename)

    print G1.nodes()
    filename = '/home/shridhar/Acads/5245/net-enlightenment/python/graphml-data/113_session_2.graphml' 
    G2 = read_graphml_file(filename)
    print G2.nodes()

if __name__ == "__main__":
    main(sys.argv)
