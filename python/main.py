import subprocess
import sys
import os
from read_orkut import read_orkut
from ba_graph import ba_graph

if __name__ == "__main__":

    ################################# Parameters ##################################
    if len(sys.argv) < 4:
        print(
            "Usage:", sys.argv[0], "[OrkutFile (in)] [EdgeFile (out)] [DegFile (out)]"
        )
        sys.exit(0)

    # Orkut File (input)
    orkut_file = sys.argv[1]
    # Edge File (output)
    edge_file = sys.argv[2]
    # Degree File (output)
    degree_file = sys.argv[3]

    read_orkut(orkut_file, "../data/Orkut/edges.csv", "../data/Orkut/deg.csv")
    ba_graph(
        1000000, 10, "../data/BAGraph-m10/edges.csv", "../data/BAGraph-m10/deg.csv"
    )

    os.chdir("..")
    subprocess.run(["./run_EvalLossLocal.sh", "Orkut"])
