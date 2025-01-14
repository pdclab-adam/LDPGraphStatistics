#!/usr/bin/env python3
import csv
import numpy as np
import networkx as nx


def ba_graph(n_nodes: int, n_edges_on_new_node: int, edge_file: str, degree_file: str):
    # Fix a seed
    seed = 1

    # Generate a random graph according to the Barabasi-Albert model
    graph = nx.barabasi_albert_graph(n_nodes, n_edges_on_new_node, seed)

    # Calculate a degree for each node --> deg
    deg = np.zeros(n_nodes, dtype=int)
    for i, j in graph.edges():
        deg[i] += 1
        deg[j] += 1

    # Output edge information
    print("Outputting edge information.")
    with open(edge_file, "w") as edge_handle:
        print("#nodes", file=edge_handle)
        print(graph.number_of_nodes(), file=edge_handle)
        print(f"#nodes: {graph.number_of_nodes()}")
        print("node,node", file=edge_handle)
        writer = csv.writer(edge_handle, lineterminator="\n")
        for i, j in graph.edges():
            lst = [i, j]
            writer.writerow(lst)

    # Output degree information
    print("Outputting degree information.")
    with open(degree_file, "w") as degree_handle:
        print("node,deg", file=degree_handle)
        writer = csv.writer(degree_handle, lineterminator="\n")
        for i in range(n_nodes):
            # actor index and her degree --> lst
            lst = [i, deg[i]]
            writer.writerow(lst)
