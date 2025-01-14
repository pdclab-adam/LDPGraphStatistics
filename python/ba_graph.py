#!/usr/bin/env python3
import csv
import sys
import numpy as np
import networkx as nx


#################################### Main #####################################
def ba_graph(n_nodes: int, n_edges_on_new_node: int, edge_file: str, degree_file: str):
    # Fix a seed
    seed = 1

    # Generate a random graph according to the Barabasi-Albert model
    G = nx.barabasi_albert_graph(n_nodes, n_edges_on_new_node, seed)

    # Calculate a degree for each node --> deg
    deg = np.zeros(n_nodes, dtype=int)
    for i, j in G.edges():
        deg[i] += 1
        deg[j] += 1

    # Output edge information
    print("Outputting edge information.")
    f = open(edge_file, "w")
    print("#nodes", file=f)
    print(G.number_of_nodes(), file=f)
    print(f"#nodes: {G.number_of_nodes()}")
    print("node,node", file=f)
    writer = csv.writer(f, lineterminator="\n")
    for i, j in G.edges():
        lst = [i, j]
        writer.writerow(lst)
    f.close()

    # Output degree information
    print("Outputting degree information.")
    f = open(degree_file, "w")
    print("node,deg", file=f)
    writer = csv.writer(f, lineterminator="\n")
    for i in range(n_nodes):
        # actor index and her degree --> lst
        lst = [i, deg[i]]
        writer.writerow(lst)
    f.close()
