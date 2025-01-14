import subprocess
import sys
import os
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

    read_orkut(input_file, "../data/Orkut/edges.csv", "../data/Orkut/deg.csv")
    ba_graph(
        1000000, 10, "../data/BAGraph-m10/edges.csv", "../data/BAGraph-m10/deg.csv"
    )

    os.chdir("..")
    subprocess.run(["./run_EvalLossLocal.sh", "Orkut"])
