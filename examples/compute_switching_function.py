# examples/compute_switching_function.py
import numpy as np

from pyste import get_unitary_evolver

# Defining the Pauli matrices
X = np.array([[0,  1 ],  # Pauli X
              [1,  0 ]])
Y = np.array([[0, -1j],  # Pauli Y
              [1j, 0 ]])
Z = np.array([[1,  0 ],  # Pauli Z
              [0, -1 ]])

# Parameters
v: float = 1
f: float = 1
T: float = 1
N: int = 20
initial_state = np.array([1, 0], dtype=np.complex128)
O = np.array([[1,  1],
              [1, -1]],
             dtype=np.complex128)

# Setting up the evolver
drift_hamiltonian = v/2 * Z
control_hamiltonians = [X, Y]

evolver = get_unitary_evolver(drift_hamiltonian, control_hamiltonians)

# Specifying the control amplitudes
dt = T / N
ts = dt*np.arange(N, dtype=np.complex128)
ctrl_amp_X = f*np.cos(v * ts)
ctrl_amp_Y = np.zeros(N, dtype=np.complex128)
ctrl_amp = np.stack([ctrl_amp_X, ctrl_amp_Y], axis=-1)

# Computing the expectation value and the switching function
expval, switch_func = evolver.switching_function(ctrl_amp, initial_state, dt, O)

# Outputting the results
print("Expectation value:", expval.real)
print("Switching function:", switch_func, sep="\n")