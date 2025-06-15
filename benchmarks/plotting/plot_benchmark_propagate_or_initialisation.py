import argparse
import os

import pandas as pd

from matplotlib import pyplot as plt
from pyperf import BenchmarkSuite

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    df = pd.DataFrame(columns=["n_ctrl", "dim", "mean", "stdev", "force_dynamic", "sparse"])

    suite = BenchmarkSuite.load(args.filename)
    for bench in suite.get_benchmarks():
        name = bench.get_name().split("_")
        for i, item in enumerate(name):
            if item == "nctrl":
                n_ctrl = int(name[i+1])
            if item == "dim":
                dim = int(name[i+1])
            if item == "forcedynamic":
                force_dynamic = name[i+1] == "True"
            if item == "sparse":
                sparse = name[i+1] == "True"
        df.loc[len(df)] = [n_ctrl, dim, bench.mean(), bench.stdev(), force_dynamic, sparse]
    for sparse in [False, True]:
        for force_dynamic in [False, True]:
            label = ("sparse " if sparse else "dense ") + ("dynamic" if force_dynamic else "static")
            dff = df[df["force_dynamic"] == force_dynamic]
            dff = dff[dff["sparse"] == sparse]
            plt.fill_between(dff["dim"], dff["mean"]-dff["stdev"], dff["mean"]+dff["stdev"], alpha=0.5, label=label)
            plt.plot(dff["dim"], dff["mean"])
            plt.xscale('log', base=2)
            plt.yscale('log', base=10)
    plt.xlabel("Vector space dimension")
    plt.ylabel("Time / s")
    plt.legend()
    plt.tight_layout()
    plt.savefig(f"{os.path.splitext(args.filename)[0]}.png")
        
if __name__ == "__main__":
    main()