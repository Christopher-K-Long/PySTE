import pyperf
from py_ste import get_unitary_evolver
import numpy as np

VALUES = 3
RUNS = 20
N_CTRL = 10
DIM_MAX = 64
runner = pyperf.Runner(values=VALUES, processes = RUNS)
for sparse in [False, True]:
    for force_dynamic in [False, True]:
        for dim in range(1, DIM_MAX+1):
            H0 = np.identity(dim)
            Hs = np.concatenate([np.identity(dim)]*N_CTRL, axis=0)
            evolver = get_unitary_evolver(H0, Hs, force_dynamic=force_dynamic)

            def stmt():
                get_unitary_evolver(H0, Hs, force_dynamic=force_dynamic, sparse=sparse)

            runner.bench_func(f"initialise_dim_{dim}_nctrl_{N_CTRL}_compiledim_{evolver.dim}_compilenctrl_{evolver.n_ctrl}_forcedynamic_{force_dynamic}_sparse_{sparse}", stmt)