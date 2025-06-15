import pyperf
from pyste import get_unitary_evolver
import numpy as np

VALUES = 3
RUNS = 5
N_CTRL = 10
DIM_MAX = 64
TIME_STEPS = 100
DT = 0.1
runner = pyperf.Runner(values=VALUES, processes = RUNS)
for sparse in [False, True]:
    for force_dynamic in [False, True]:
        for dim in range(1, DIM_MAX+1):
            H0 = np.random.rand(dim, dim)+1j*np.random.rand(dim, dim)
            H0 = H0 + H0.T.conj()
            Hs = []
            for _ in range(N_CTRL):
                H = np.random.rand(dim, dim)+1j*np.random.rand(dim, dim)
                H = H + H.T.conj()
                Hs.append(H)
            Hs = np.concatenate(Hs, axis=0)
            ctrl_amp = np.random.rand(TIME_STEPS, N_CTRL).astype(np.complex128)
            state = np.random.rand(dim).astype(np.complex128)
            state /= np.linalg.norm(state)
            evolver = get_unitary_evolver(H0, Hs, force_dynamic=force_dynamic, sparse=sparse)

            def stmt():
                evolver.propagate(ctrl_amp, state, DT)

            runner.bench_func(f"propagate_dim_{dim}_nctrl_{N_CTRL}_compiledim_{evolver.dim}_compilenctrl_{evolver.n_ctrl}_forcedynamic_{force_dynamic}_sparse_{sparse}", stmt)