import subprocess
import os
import csv
from read_orkut import read_orkut
from ba_graph import ba_graph
from common import *

if __name__ == "__main__":
    log("Running ldp statistics")

    args = parse_args()
    input_file: str = args.input_file
    output_file: str = args.output_file
    epsilon: float = args.epsilon
    delta: float = args.delta
    replications: int = args.replications
    disable: bool = args.disable

    if disable:
        log("Disabled by user input")
        log()
        alert = "disabled"
        write_results(output_file, args, alert)
        status = 0
        log(f"********** Exit Status {status} **********")
        exit({status})

    log("Running edge table and degree distribution setup")
    edge_file = "../data/Orkut/edges.csv"
    degree_file = "../data/Orkut/deg.csv"
    read_orkut(input_file, edge_file, degree_file)
    log("Running edge table and degree distribution setup - Done")
    log()

    log("Creating Barabasi Albert graph")
    n_nodes = 1000000
    n_edges_on_new_node = 10
    edge_file = f"../data/BAGraph-m{n_edges_on_new_node}/edges.csv"
    degree_file = f"../data/BAGraph-m{n_edges_on_new_node}/deg.csv"
    ba_graph(n_nodes, n_edges_on_new_node, edge_file, degree_file)
    log("Creating Barabasi Albert graph - Done")
    log()

    log("Running statistics calculations")
    n = 100
    noise_type = 1
    algorithm = 0
    print("", flush=True)
    os.chdir("../cpp")
    statistics_calculation_args = [
        "./EvalLossLocal",
        "Orkut",
        f"{n}",
        f"{epsilon}",
        f"{noise_type}",
        f"{replications}",
        f"{algorithm}",
    ]
    subprocess.run(statistics_calculation_args)
    os.chdir("../python")
    log("Running statistics calculations - Done")
    log()
