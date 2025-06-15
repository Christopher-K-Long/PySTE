import argparse
import os

import pandas as pd

from matplotlib import pyplot as plt

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()
    path = args.filename
    df = pd.read_csv(path)
    groups = df.groupby("Integrator")

    for name, group in groups:
        plt.scatter(group["Infidelity"], group["Time"], alpha=0.25, label=name)
    plt.xscale("log")
    plt.yscale("log")
    plt.xlim([1e-11,1])
    plt.legend()
    plt.xlabel("Infidelity")
    plt.ylabel("Runtime / s")
    plt.savefig(f"{os.path.splitext(path)[0]}.png")

if __name__ == "__main__":
    main()