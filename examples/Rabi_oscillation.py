# examples/Rabi_oscillation.py
import numpy as np

from pyste import get_unitary_evolver

X = np.array([[0,  1],  # Pauli X
              [1,  0]])
Z = np.array([[1,  0],  # Pauli Z
              [0, -1]])

# Parameters
v: float = 1
f: float = 1
T: float = 1
N: int = 1000
initial_state = np.array([1, 0], dtype=np.complex128)

# Setting up the evolver
drift_hamiltonian = v/2 * Z
control_hamiltonian = X

evolver = get_unitary_evolver(drift_hamiltonian, control_hamiltonian)

# Specifying the control amplitudes
dt = T / N
ts = dt*np.arange(N, dtype=np.complex128)
ctrl_amp = f*np.cos(v * ts)

# Propagating the initial state
psi = evolver.propagate(ctrl_amp, initial_state, dt)

# Outputting the final state
print(psi)