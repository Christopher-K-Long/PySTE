# Running Benchmarks

You can find pre-executed benchmarking data and descriptions of each benchmark [here](../benchmarks/index.md). Additionally, you can run the benchmarks yourself by executing
```bash
python benchmarks/run_all_benchmarks_and_plot.py
```
from the root directory of PySTE. This will generate the following file structure:
```
results/
├─ data/
│  ├─ benchmark_propagate.json
│  ├─ benchmark_propagate_sparse_Hamiltonian.json
│  ├─ benchmark_initialisation.json
│  ├─ benchmark_initialisation_sparse.json
│  └─ benchmark_against_qutip.csv
└─ plots/
   ├─ benchmark_propagate.png
   ├─ benchmark_propagate_sparse_Hamiltonian.png
   ├─ benchmark_initialisation.png
   ├─ benchmark_initialisation_sparse.png
   └─ benchmark_against_qutip.png
```

Alternatively,
```bash
python benchmarks/benchmark_propagate.py -o results/data/benchmark_propagate.json

python benchmarks/benchmark_propagate_sparse_Hamiltonian.py -o results/data/benchmark_propagate_sparse_Hamiltonian.json

python benchmarks/benchmark_initialisation.py -o results/data/benchmark_initialisation.json

python benchmarks/benchmark_initialisation_sparse.py -o results/data/benchmark_initialisation_sparse.json

python benchmarks/benchmark_against_qutip.py -o results/data/benchmark_against_qutip.csv
```
can be run individually to execute specific benchmarks.

Finally, the data from the benchmarks can be plotted using
```bash
# replace DATAFILE with the .json file you wish to plot
python benchmarks/plotting/plot_benchmark_propagate_or_initialisation.py results/data/DATAFILE.json

python benchmarks/plotting/plot_benchmark_against_qutip.py results/data/benchmark_against_qutip.csv
```
The plots will be output into the same directory as the input data file with the same name but the extension changed to ``.png``.

[Previous](running_tests.md)