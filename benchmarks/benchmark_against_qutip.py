import argparse
import os
import time

import numpy as np
import pandas as pd
from qutip import sesolve, Qobj
from tqdm import tqdm

from pyste import get_unitary_evolver
from pyste import evolvers

DIM = 32
T = 10
SEED = 2
RUNS = 10

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--output', required=True)
    args = parser.parse_args()
    path = args.output
    if os.path.exists(path):
        df = pd.read_csv(path, index_col="Unnamed: 0")
    else:
        df = pd.DataFrame(columns=["Integrator", "Seed", "Dim", "N_CTRL", "tol or N", "Infidelity", "Time"])
        dir = os.path.dirname(path)
        if dir and not os.path.exists(dir):
            os.makedirs(dir, exist_ok=True)
        df.to_csv(path)

    np.random.seed(SEED)
    H0 = np.random.rand(DIM, DIM)+1j*np.random.rand(DIM, DIM)
    H0 = H0 + H0.T.conj()
    Hs = np.random.rand(DIM, DIM)+1j*np.random.rand(DIM, DIM)
    Hs = Hs + Hs.T.conj()
    state = np.random.rand(DIM).astype(np.complex128)
    state /= np.linalg.norm(state)
    evolver1 = get_unitary_evolver(H0, Hs)
    evolver2 = get_unitary_evolver(-H0, -Hs)

    H1 = [Qobj(H0), [Qobj(Hs), "cos(2*pi*t)"]]
    H2 = [Qobj(-H0), [Qobj(-Hs), f"cos(2*pi*({T}-t))"]]
    qutip_state = Qobj(state)
    t_list = [0, T]
    # compile
    sesolve(H2, qutip_state, [0])

    for _ in tqdm(range(RUNS)):
        for N in tqdm(np.logspace(0, 5, 100)):
            N = int(N)
            ts = np.linspace(0, T, N+1)[:-1]
            ctrl_amp = np.cos(2*np.pi*ts).astype(np.complex128)
            start = time.time()
            inter_state = evolver1.propagate(ctrl_amp, state, T/N)
            end = time.time()
            runtime = end-start
            result = evolver2.propagate(np.flip(ctrl_amp), inter_state, T/N)
            infidelity = 1-np.square(np.abs(result.conj()@state))
            df.loc[len(df)] = ["PySTE", SEED, DIM, 1, N, infidelity, runtime]
            df.to_csv(path)

        for method in ["adams", "bdf", "lsoda", "dop853", "vern7", "vern9"]:
            for tol in tqdm(reversed(np.logspace(-7, 0, 100)), total=100):
                options = {"method": method, "atol": tol, "rtol": tol, "nsteps": 1e7}
                start = time.time()
                output = sesolve(H1, qutip_state, t_list, options=options)
                end = time.time()
                runtime = end-start
                inter_state = output.final_state.full().flatten()
                output = sesolve(H2, Qobj(inter_state), t_list, options=options)
                result = output.final_state.full().flatten()
                infidelity = 1-np.square(np.abs(result.conj()@state))
                df.loc[len(df)] = [method, SEED, DIM, 1, tol, infidelity, runtime]
                df.to_csv(path)

if __name__ == "__main__":
    main()