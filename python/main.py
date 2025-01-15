import subprocess
import os
import csv
import re
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
    n = 10000
    noise_type = 1
    algorithm = 0
    print("", flush=True)
    os.chdir("../cpp")
    statistics_calculation_args = [
        "./EvalLossLocal",
        "../data/Orkut/edges.csv",
        f"{n}",
        f"{epsilon}",
        f"{noise_type}",
        f"{replications}",
        f"{algorithm}",
    ]
    subprocess.run(statistics_calculation_args)
    print("", flush=True)
    os.chdir("../python")
    log("Running statistics calculations - Done")
    log()

    log("Finding statistics file")
    results_csv_files = [
        file for file in os.listdir("../data/Orkut/") if re.match(r"^res.*\.csv$", file)
    ]

    if len(results_csv_files) == 0:
        error = "Error: no intermediate results file generated"
        log(error)
        raise FileNotFoundError(error)

    if len(results_csv_files) > 1:
        error = "Error: multiple intermediate results file generated"
        log(error)
        raise FileNotFoundError(error)
    log("Finding statistics file - Done")
    log()

    log("Reading statistics file")
    results_csv_file = results_csv_files[0]
    with open(
        os.path.join("../data/Orkut", results_csv_file), "r"
    ) as results_csv_handle:
        header = next(results_csv_handle)
        csv_reader = csv.reader(results_csv_handle)
        results = []
        for i, line in enumerate(csv_reader):
            if i == replications:
                break
            result = {}
            result["id"] = i
            result["n_triangles_true"] = line[0]
            result["n_triangles_estimate"] = line[1]
            result["n_triangles_relative_error"] = line[2]
            result["n_triangles_l2_loss"] = line[3]

            result["n_2_stars_true"] = line[4]
            result["n_2_stars_estimate"] = line[5]
            result["n_2_stars_relative_error"] = line[6]
            result["n_2_stars_l2_loss"] = line[7]

            result["n_3_stars_true"] = line[8]
            result["n_3_stars_estimate"] = line[9]
            result["n_3_stars_relative_error"] = line[10]
            result["n_3_stars_l2_loss"] = line[11]

            result["clustering_coefficient_true"] = line[12]
            result["clustering_coefficient_estimate"] = line[13]
            result["clustering_coefficient_relative_error"] = line[14]
            result["clustering_coefficient_l2_loss"] = line[15]

            result["n_triangles_sensitivity"] = line[16]
            result["n_2_stars_sensitivity"] = line[17]
            result["n_3_stars_sensitivity"] = line[18]
            results.append(result)
    log("Reading statistics file - Done")
    log()

    alert = None
    write_results(output_file, args, alert, results)

    log("************** Done! **************")
