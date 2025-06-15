import numpy as np
from numpy.typing import ArrayLike
# import os
# os.environ["OMP_NUM_THREADS"] = "2"
from . import evolvers

def get_unitary_evolver(drift_hamiltonian: ArrayLike,
                        control_hamiltonians: ArrayLike,
                        sparse: bool = False,
                        force_dynamic: bool = False
                       ) -> evolvers.UnitaryEvolver:
    """
    Initialises a class to store the diagonalised drift and control
    Hamiltonians. On initialisation the Hamiltonians are diagonalised and the
    eigenvectors and values stored. This initial diagonalisation may be slow and
    takes
    $O(\\textrm{dim}^3)$
    time for a
    $\\textrm{dim}\\times \\textrm{dim}$
    Hamiltonian. However, it  allows each step of the Suzuki-Trotter expansion
    to be implimented in
    $O(\\textrm{dim}^2)$
    time with matrix multiplication and only scalar exponentiation opposed to
    matrix exponentiation which takes
    $O(\\textrm{dim}^3)$
    time.

    Parameters
    ----------
    drift_hamiltonian : ArrayLike
        The drift Hamiltonian. Must be a square matrix of dimension ``dim``.
    control_hamiltonians : ArrayLike
        The control Hamiltonians. Can either by a 3D array with shape
        ``(n_ctrl, dim, dim)`` representing a stack of control Hamiltonians
        indexed by the first axis. Alternatively a 3D array with shape
        ``(n_ctrl * dim, dim)`` can be passed with the control Hamiltonians
        being concatenated along the first axis.
    sparse : bool, optional
        Whether to use sparse matrices for the evolution. The default is False.
    force_dynamic : bool, optional
        Whether to force the use of dynamically sized matrices for the
        evolution. The default is False.

    Returns
    -------
    evolvers.UnitaryEvolver
        An instance of a child class of
        :class:`evolvers.UnitaryEvolver <pyste.evolvers.UnitaryEvolver>`.
        If ``sparse == False`` then the returned instance will be a child class
        of
        :class:`evolvers.DenseUnitaryEvolver <pyste.evolvers.DenseUnitaryEvolver>`
        else
        :class:`evolvers.SparseUnitaryEvolver <pyste.evolvers.SparseUnitaryEvolver>`
        is returned. Both
        :class:`evolvers.DenseUnitaryEvolver <pyste.evolvers.DenseUnitaryEvolver>`
        and
        :class:`evolvers.SparseUnitaryEvolver <pyste.evolvers.SparseUnitaryEvolver>`
        are dynamic evolvers: evolvers for which the number of control
        Hamiltonians and the vector space dimension are determined at runtime
        based on the shapes of ``drift_hamiltonian`` and ``control_hamiltonians``. If possible
        ``get_unitary_evolver()`` will return an instance of
        :class:`evolvers.DenseUnitaryEvolver_nctrl_dim <pyste.evolvers.DenseUnitaryEvolver_nctrl_dim>`
        or 
        :class:`evolvers.SparseUnitaryEvolver_nctrl_dim <pyste.evolvers.SparseUnitaryEvolver_nctrl_dim>`,
        where ``nctrl`` and ``dim`` are substituted for their corresponding
        values.
        These are fixed evolvers where the number of controls (``nctrl``) and
        the vector space dimension (``dim``) are know at the C++ compile time
        allowing for more efficient C++ methods to be compiled.

        Note
        ----
        An instance of
        :class:`evolvers.UnitaryEvolver <pyste.evolvers.UnitaryEvolver>`
        itself will never be returned.
        :class:`evolvers.UnitaryEvolver <pyste.evolvers.UnitaryEvolver>`
        is simply a base class for all evolvers allowing for checks such as::

            isinstance(evolver, evolvers.UnitaryEvolver)
        
    Raises
    ------
    ValueError
        ``drift_hamiltonian`` must be 2D.
    ValueError
        ``drift_hamiltonian`` must be square.
    ValueError
        The control Hamiltonians (``control_hamiltonians``) must have the same number of columns as
        ``drift_hamiltonian``.
    ValueError
        ``control_hamiltonians`` must be 2D or 3D.
    ValueError
        Each control Hamiltonian in ``control_hamiltonians`` must have the same dimension as ``drift_hamiltonian``.
    """
    drift_hamiltonian = np.array(drift_hamiltonian, dtype=np.complex128)
    control_hamiltonians = np.array(control_hamiltonians, dtype=np.complex128)
    
    if drift_hamiltonian.ndim != 2:
        raise ValueError("``drift_hamiltonian`` must be 2D.")
    
    dim: int = drift_hamiltonian.shape[0]
    if drift_hamiltonian.shape[1] != dim:
        raise ValueError("``drift_hamiltonian`` must be square.")
    
    if control_hamiltonians.ndim == 3:
        control_hamiltonians = control_hamiltonians.reshape((-1, dim))
    elif control_hamiltonians.ndim == 2:
        if control_hamiltonians.shape[1] != dim:
            raise ValueError("The control Hamiltonians (``control_hamiltonians``) must have the same number of columns as ``drift_hamiltonian``.")
    elif control_hamiltonians.size == 0:
        control_hamiltonians = np.zeros((0, dim), dtype=np.complex128)
    else:
        raise ValueError("``control_hamiltonians`` must be 2D or 3D.")

    if control_hamiltonians.shape[0] % dim != 0:
        raise ValueError("Each control Hamiltonian in control_hamiltonians must have the same dimension as ``drift_hamiltonian``.")

    n_ctrl: int = control_hamiltonians.shape[0]//dim
    name: str = ("Sparse" if sparse else "Dense") + "UnitaryEvolver"
    if force_dynamic:
        Evolver = getattr(evolvers, name)
    else:
        try:
            Evolver = getattr(evolvers, name+f"_{n_ctrl}_{dim}")
        except AttributeError:
            try:
                Evolver = getattr(evolvers, name+f"_Dynamic_{dim}")
            except AttributeError:
                try:
                    Evolver = getattr(evolvers, name+f"_{n_ctrl}_Dynamic")
                except AttributeError:
                    Evolver = getattr(evolvers, name)
    return Evolver(drift_hamiltonian, control_hamiltonians)