import numpy as np
import pickle as pkl
from .unique_names import UniquePath
from pyste import get_unitary_evolver

X = np.array([[0, 1],
              [1, 0]],
             dtype=np.complex128)
Y = np.array([[0, -1j],
              [1j, 0 ]],
             dtype=np.complex128)
Z = np.array([[1,  0],
              [0, -1]],
             dtype=np.complex128)

def isApprox(a, b, prec=1e-12):
    # Note that prec=1e-12 is the same default value used for complex<double> in
    #   in Eigen.
    return np.linalg.norm(a-b) <= prec*np.min([np.linalg.norm(a), np.linalg.norm(b)])


# Initialisation Tests
def test_dense_Hamiltonian_initialisation():
    h0 = X
    hs = [-Z, -Y]
    H = np.array([[-1, 1],
                  [ 1, 1]],
                 dtype=np.float64)
    H /= np.sqrt(2)
    SH = np.array([[1,   1],
                   [1j, -1j]])
    SH /= np.sqrt(2)
    eigs = [1j, -1j]
    evolver = get_unitary_evolver(h0, hs)

    assert evolver.length == 2

    assert isApprox(evolver.d0, eigs)

    assert len(evolver.ds) == evolver.length
    assert isApprox(evolver.ds[0], eigs)
    assert isApprox(evolver.ds[1], eigs)

    assert isApprox(evolver.u0, H)

    assert isApprox(evolver.u0_inverse, H)

    assert len(evolver.us) == evolver.length + 1
    assert isApprox(evolver.us[0], H)
    assert isApprox(evolver.us[1], SH.T.conj())
    assert isApprox(evolver.us[2], SH)

    assert len(evolver.us_individual) == evolver.length
    assert isApprox(evolver.us_individual[0], np.identity(2))
    assert isApprox(evolver.us_individual[1], SH)

    assert len(evolver.us_inverse_individual) == evolver.length
    assert isApprox(evolver.us_inverse_individual[0], np.identity(2))
    assert isApprox(evolver.us_inverse_individual[1], SH.T.conj())

    assert len(evolver.hs) == evolver.length
    assert isApprox(evolver.hs[0], hs[0])
    assert isApprox(evolver.hs[1], hs[1])

    assert isApprox(evolver.u0_inverse_u_last, H @ SH)

def test_dense_Hamiltonian_initialisation_no_controls():
    h0 = X
    hs = []
    H = np.array([[-1, 1],
                  [ 1, 1]],
                 dtype=np.float64)
    H /= np.sqrt(2)
    eigs = [1j, -1j]
    evolver = get_unitary_evolver(h0, hs)

    assert evolver.length == 0

    assert isApprox(evolver.d0, eigs)

    assert len(evolver.ds) == evolver.length

    assert isApprox(evolver.u0, H)

    assert isApprox(evolver.u0_inverse, H)

    assert len(evolver.us) == evolver.length + 1
    assert isApprox(evolver.us[0], H)

    assert len(evolver.us_individual) == evolver.length

    assert len(evolver.us_inverse_individual) == evolver.length

    assert len(evolver.hs) == evolver.length

    assert isApprox(evolver.u0_inverse_u_last, np.identity(2))

def test_sparse_Hamiltonian_initialisation():
    h0 = X
    hs = [-Z, -Y]
    H = np.array([[-1, 1],
                  [ 1, 1]],
                 dtype=np.float64)
    H /= np.sqrt(2)
    SH = np.array([[1,   1],
                   [1j, -1j]])
    SH /= np.sqrt(2)
    eigs = [1j, -1j]
    evolver = get_unitary_evolver(h0, hs, sparse=True)

    assert evolver.length == 2

    assert isApprox(evolver.d0, eigs)

    assert len(evolver.ds) == evolver.length
    assert isApprox(evolver.ds[0], eigs)
    assert isApprox(evolver.ds[1], eigs)

    assert isApprox(evolver.u0.toarray(), H)

    assert isApprox(evolver.u0_inverse.toarray(), H)

    assert len(evolver.us) == evolver.length + 1
    assert isApprox(evolver.us[0].toarray(), H)
    assert isApprox(evolver.us[1].toarray(), SH.T.conj())
    assert isApprox(evolver.us[2].toarray(), SH)

    assert len(evolver.us_individual) == evolver.length
    assert isApprox(evolver.us_individual[0].toarray(), np.identity(2))
    assert isApprox(evolver.us_individual[1].toarray(), SH)

    assert len(evolver.us_inverse_individual) == evolver.length
    assert isApprox(evolver.us_inverse_individual[0].toarray(), np.identity(2))
    assert isApprox(evolver.us_inverse_individual[1].toarray(), SH.T.conj())

    assert len(evolver.hs) == evolver.length
    assert isApprox(evolver.hs[0].toarray(), hs[0])
    assert isApprox(evolver.hs[1].toarray(), hs[1])

    assert isApprox(evolver.u0_inverse_u_last.toarray(), H @ SH)

def test_sparse_Hamiltonian_initialisation_no_controls():
    h0 = X
    hs = []
    H = np.array([[-1, 1],
                  [ 1, 1]],
                 dtype=np.float64)
    H /= np.sqrt(2)
    eigs = [1j, -1j]
    evolver = get_unitary_evolver(h0, hs, sparse=True)

    assert evolver.length == 0

    assert isApprox(evolver.d0, eigs)

    assert len(evolver.ds) == evolver.length

    assert isApprox(evolver.u0.toarray(), H)

    assert isApprox(evolver.u0_inverse.toarray(), H)

    assert len(evolver.us) == evolver.length + 1
    assert isApprox(evolver.us[0].toarray(), H)

    assert len(evolver.us_individual) == evolver.length

    assert len(evolver.us_inverse_individual) == evolver.length

    assert len(evolver.hs) == evolver.length

    assert isApprox(evolver.u0_inverse_u_last.toarray(), np.identity(2))

def test_pickling():
    h0 = X
    hs = [-Z, -Y]
    H = np.array([[-1, 1],
                  [ 1, 1]],
                 dtype=np.float64)
    H /= np.sqrt(2)
    SH = np.array([[1,   1],
                   [1j, -1j]])
    SH /= np.sqrt(2)
    eigs = [1j, -1j]
    initial_evolver = get_unitary_evolver(h0, hs)

    with UniquePath() as path:
        with open(path, "wb") as file:
            pkl.dump(initial_evolver, file, pkl.HIGHEST_PROTOCOL)
        with open(path, "rb") as file:
            evolver = pkl.load(file)

    assert evolver.length == 2

    assert isApprox(evolver.d0, eigs)

    assert len(evolver.ds) == evolver.length
    assert isApprox(evolver.ds[0], eigs)
    assert isApprox(evolver.ds[1], eigs)

    assert isApprox(evolver.u0, H)

    assert isApprox(evolver.u0_inverse, H)

    assert len(evolver.us) == evolver.length + 1
    assert isApprox(evolver.us[0], H)
    assert isApprox(evolver.us[1], SH.T.conj())
    assert isApprox(evolver.us[2], SH)

    assert len(evolver.us_individual) == evolver.length
    assert isApprox(evolver.us_individual[0], np.identity(2))
    assert isApprox(evolver.us_individual[1], SH)

    assert len(evolver.us_inverse_individual) == evolver.length
    assert isApprox(evolver.us_inverse_individual[0], np.identity(2))
    assert isApprox(evolver.us_inverse_individual[1], SH.T.conj())

    assert len(evolver.hs) == evolver.length
    assert isApprox(evolver.hs[0], hs[0])
    assert isApprox(evolver.hs[1], hs[1])

    assert isApprox(evolver.u0_inverse_u_last, H @ SH)

def test_pickling_no_controls():
    h0 = X
    hs = []
    H = np.array([[-1, 1],
                  [ 1, 1]],
                 dtype=np.float64)
    H /= np.sqrt(2)
    eigs = [1j, -1j]
    initial_evolver = get_unitary_evolver(h0, hs)

    with UniquePath() as path:
        with open(path, "wb") as file:
            pkl.dump(initial_evolver, file, pkl.HIGHEST_PROTOCOL)
        with open(path, "rb") as file:
            evolver = pkl.load(file)

    assert evolver.length == 0

    assert isApprox(evolver.d0, eigs)

    assert len(evolver.ds) == evolver.length

    assert isApprox(evolver.u0, H)

    assert isApprox(evolver.u0_inverse, H)

    assert len(evolver.us) == evolver.length + 1
    assert isApprox(evolver.us[0], H)

    assert len(evolver.us_individual) == evolver.length

    assert len(evolver.us_inverse_individual) == evolver.length
    
    assert len(evolver.hs) == evolver.length
    
    assert isApprox(evolver.u0_inverse_u_last, np.identity(2))


# Evolution Tests
def test_propagate_identity():
    h0 = np.zeros((2, 2))
    hs = [-Z, -Y]

    evolver = get_unitary_evolver(h0, hs)
    
    ctrl_amp = np.zeros((100, 2), dtype=np.complex128)
    dt = 0.1

    initial_state = np.array([1, 0], dtype=np.complex128)

    output_state = evolver.propagate(ctrl_amp, initial_state, dt)

    assert isApprox(output_state, initial_state)

def test_propagate_constant_evolution():
    h0 = Z
    hs = [-Z, -Y]

    evolver = get_unitary_evolver(h0, hs)

    ctrl_amp = np.zeros((100, 2), dtype=np.complex128)
    dt = 0.1
    
    initial_state = np.array([1, 0], dtype=np.complex128)

    output_state = evolver.propagate(ctrl_amp, initial_state, dt)

    assert isApprox(output_state, [np.exp(-1j*dt*100), 0])

def test_propagate_no_control_Hamiltonians():
    h0 = Z
    hs = []

    evolver = get_unitary_evolver(h0, hs)

    ctrl_amp = np.zeros((100, 0), dtype=np.complex128)
    dt = 0.1

    initial_state = np.array([1, 0], dtype=np.complex128)

    output_state = evolver.propagate(ctrl_amp, initial_state, dt)

    assert isApprox(output_state, [np.exp(-1j*dt*100), 0])

def test_propagate_Rabi_oscillation():
    # This test takes the rotating wave approximation in the analytics and so
    #   `isApprox`` is vital.
    h0 = Z
    hs = [X]

    evolver = get_unitary_evolver(h0, hs)

    dt = 0.001
    omega = 2*np.pi*0.001

    initial_state = np.array([1, 0], dtype=np.complex128)
    N = 1000000
    n = 100000
    ts = dt*np.arange(N, dtype=np.complex128)
    ctrl_amp = omega*np.cos(2*ts)
    for k in range(n, N+n, n):
        output_state = evolver.propagate(ctrl_amp[:k], initial_state, dt)
        rwa_analytic_output_state = np.array([    np.exp(-1j*k*dt)*np.cos(omega*k*dt/2),
                                              -1j*np.exp( 1j*k*dt)*np.sin(omega*k*dt/2)])
        assert isApprox(output_state, rwa_analytic_output_state, 5e-3)


def test_propagate_collection_identity():
    h0 = np.zeros((2, 2))
    hs = [-Z, -Y]

    evolver = get_unitary_evolver(h0, hs)
    
    ctrl_amp = np.zeros((100, 2), dtype=np.complex128)
    dt = 0.1

    initial_states = np.identity(2, dtype=np.complex128)

    output_states = evolver.propagate_collection(ctrl_amp, initial_states, dt)

    assert isApprox(output_states, initial_states)

def test_propagate_collection_constant_evolution():
    h0 = Z
    hs = [-Z, -Y]

    evolver = get_unitary_evolver(h0, hs)

    ctrl_amp = np.zeros((100, 2), dtype=np.complex128)
    dt = 0.1
    
    initial_states = np.identity(2, dtype=np.complex128)

    output_states = evolver.propagate_collection(ctrl_amp, initial_states, dt)

    assert isApprox(output_states, [[np.exp(-1j*dt*100), 0],
                                   [0, np.exp(1j*dt*100)]])

def test_propagate_collection_no_control_Hamiltonians():
    h0 = Z
    hs = []

    evolver = get_unitary_evolver(h0, hs)

    ctrl_amp = np.zeros((100, 0), dtype=np.complex128)
    dt = 0.1

    initial_states = np.identity(2, dtype=np.complex128)

    output_states = evolver.propagate_collection(ctrl_amp, initial_states, dt)

    assert isApprox(output_states, [[np.exp(-1j*dt*100), 0],
                                   [0, np.exp(1j*dt*100)]])

def test_propagate_collection_Rabi_oscillation():
    h0 = Z
    hs = [X]

    evolver = get_unitary_evolver(h0, hs)

    dt = 0.001
    omega = 2*np.pi*0.001

    initial_states = np.identity(2, dtype=np.complex128)
    N = 10000
    n = 1000
    ts = dt*np.arange(N, dtype=np.complex128)
    ctrl_amp = omega*np.cos(2*ts)
    for k in range(n, N+n, n):
        output_states = evolver.propagate_collection(ctrl_amp[:k], initial_states, dt)
        propagate_output = np.stack([evolver.propagate(ctrl_amp[:k], initial_states[:,0], dt),
                                     evolver.propagate(ctrl_amp[:k], initial_states[:,1], dt)],
                                    axis=-1)
        assert isApprox(output_states, propagate_output)


def test_propagate_all_identity():
    h0 = np.zeros((2, 2))
    hs = [-Z, -Y]

    evolver = get_unitary_evolver(h0, hs)
    
    ctrl_amp = np.zeros((100, 2), dtype=np.complex128)
    dt = 0.1

    initial_state = np.array([1, 0], dtype=np.complex128)

    output_states = evolver.propagate_all(ctrl_amp, initial_state, dt)

    target_output_states = np.stack([np.ones(101), np.zeros(101)], axis=0)

    assert isApprox(output_states, target_output_states)

def test_propagate_all_constant_evolution():
    h0 = Z
    hs = [-Z, -Y]

    evolver = get_unitary_evolver(h0, hs)

    ctrl_amp = np.zeros((100, 2), dtype=np.complex128)
    dt = 0.1
    
    initial_state = np.array([1, 0], dtype=np.complex128)

    output_states = evolver.propagate_all(ctrl_amp, initial_state, dt)

    ts = dt*np.arange(101)

    target_output_states = np.stack([np.exp(-1j*ts), np.zeros(101)], axis=0)

    assert isApprox(output_states, target_output_states)

def test_propagate_all_no_control_Hamiltonians():
    h0 = Z
    hs = []

    evolver = get_unitary_evolver(h0, hs)

    ctrl_amp = np.zeros((100, 0), dtype=np.complex128)
    dt = 0.1

    initial_state = np.array([1, 0], dtype=np.complex128)

    output_states = evolver.propagate_all(ctrl_amp, initial_state, dt)

    ts = dt*np.arange(101)

    target_output_states = np.stack([np.exp(-1j*ts), np.zeros(101)], axis=0)

    assert isApprox(output_states, target_output_states)

def test_propagate_all_Rabi_oscillation():
    h0 = Z
    hs = [X]

    evolver = get_unitary_evolver(h0, hs)

    dt = 0.001
    omega = 2*np.pi*0.001

    initial_state = np.array([1, 0], dtype=np.complex128)
    
    N = 100
    n = 1
    ts = dt*np.arange(N, dtype=np.complex128)
    ctrl_amp = omega*np.cos(2*ts)
    
    output_states = evolver.propagate_all(ctrl_amp, initial_state, dt)

    target_output_states = np.empty((2, N+1), dtype=np.complex128)
    target_output_states[:, 0] = initial_state
    for k in range(n, N+n, n):
        target_output_states[:, k] = evolver.propagate(ctrl_amp[:k], initial_state, dt)
    assert isApprox(output_states, target_output_states)


# Test Expectation Values
def test_evolved_expectation_value():
    h0 = Z
    hs = [X]

    evolver = get_unitary_evolver(h0, hs)

    dt = 0.001
    omega = 2*np.pi*0.1

    initial_state = np.array([1, 0], dtype=np.complex128)
    N = 2500
    ts = dt*np.arange(N, dtype=np.complex128)
    ctrl_amp = omega*np.cos(2*ts)

    expval = evolver.evolved_expectation_value(ctrl_amp, initial_state, dt, Y)
    state = evolver.propagate(ctrl_amp, initial_state, dt)
    target_expval = state.T.conj() @ Y @ state

    assert np.abs(expval - target_expval) <= 1e-15

def test_evolved_expectation_value_all():
    h0 = Z
    hs = [X]

    evolver = get_unitary_evolver(h0, hs)

    dt = 0.001
    omega = 2*np.pi*0.1

    initial_state = np.array([1, 0], dtype=np.complex128)
    N = 2500
    ts = dt*np.arange(N, dtype=np.complex128)
    ctrl_amp = omega*np.cos(2*ts)

    expvals = evolver.evolved_expectation_value_all(ctrl_amp, initial_state, dt, Y)
    states = evolver.propagate_all(ctrl_amp, initial_state, dt)
    target_expvals = [state.T.conj() @ Y @ state for state in states.T]

    assert isApprox(expvals, target_expvals)


# Test Switching Function
def test_switching_function():
    h0 = Z
    hs = [X, Y]
    H = np.array([[1, 1],
                  [1, -1]],
                 dtype=np.complex128)
    
    evolver = get_unitary_evolver(h0, hs)

    dt = 0.1
    omega = 2*np.pi*0.1

    initial_state = np.array([1, 0], dtype=np.complex128)
    N = 100
    ts = dt*np.arange(N, dtype=np.complex128)
    ctrl_amp = np.stack([omega*np.cos(2*ts), np.zeros(N)], axis=-1)
    
    expval, switching_function = evolver.switching_function(ctrl_amp, initial_state, dt, H)

    expval1 = evolver.evolved_expectation_value(ctrl_amp, initial_state, dt, H)

    assert isApprox(expval, expval1)

    eps = 1e-6
    fd_expval = np.empty((N, 2))
    for j in range(N):
        for k in range(2):
            new_ctrl_amp = ctrl_amp.copy()
            new_ctrl_amp[j, k] += eps
            expval2 = evolver.evolved_expectation_value(new_ctrl_amp, initial_state, dt, H)
            fd_expval[j, k] = (expval2.real - expval1.real) / eps
    fd_expval /= dt
    assert isApprox(switching_function, fd_expval, eps)