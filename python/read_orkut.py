#!/usr/bin/env python3
import csv
import numpy as np
import re
import networkx as nx
from scipy.sparse import lil_matrix
from common import log


def read_orkut(input_file: str, edge_file: str, degree_file: str):
    # Read max_user_ID from the Orkut file --> max_user_id
    graph: nx.Graph = nx.read_edgelist(input_file, nodetype=int)
    max_user_id = max(graph.nodes)
    user_num = max_user_id + 1
    edges_lil = lil_matrix((user_num, user_num))
    deg = np.zeros(user_num)

    # Read edges and degrees from the Orkut file --> edges_lil, deg
    for edge in graph.edges:
        user1 = edge[0] - 1
        user2 = edge[1] - 1
        edges_lil[user1, user2] = 1
        deg[user1] += 1
        deg[user2] += 1

    # Extract users with deg >= 1 and create new user IDs --> user_dic ({user_id, new_user_id})
    user_dic = {}
    new_user_id = 0
    for user_id in range(user_num):
        if deg[user_id] > 0:
            user_dic[user_id] = new_user_id
            new_user_id += 1
    log(f"#users: {len(user_dic)}")

    a1, a2 = edges_lil.nonzero()
    log(f"#edges: {len(a1)}")

    # Output edge information
    log("Outputting edge information")
    with open(edge_file, "w") as edge_handle:
        print("#nodes", file=edge_handle)
        print(len(user_dic), file=edge_handle)
        print("node,node", file=edge_handle)
        writer = csv.writer(edge_handle, lineterminator="\n")
        for i in range(len(a1)):
            # user_ids --> user_id1, user_id2
            user_id1 = a1[i]
            user_id2 = a2[i]
            # new_user_ids --> user1, user2
            user1 = user_dic[user_id1]
            user2 = user_dic[user_id2]
            edge = [user1, user2]
            writer.writerow(edge)

    # Output degree information
    print("Outputting degree information.")
    with open(degree_file, "w") as degree_handle:
        print("node,deg", file=degree_handle)
        writer = csv.writer(degree_handle, lineterminator="\n")
        for user_id in range(user_num):
            if deg[user_id] == 0:
                continue
            # new_user_id --> user1
            user1 = user_dic[user_id]
            # new_user_id and her deg --> lst
            lst = [user1, int(deg[user_id])]
            writer.writerow(lst)
