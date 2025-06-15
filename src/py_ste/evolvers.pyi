"A collection of evolver classes."

import numpy as np

class pybind11_object: pass

def _set_threads(threads: int):
    """
    Sets the number of threads to be used during multithreading.

    Parameters
    ----------
    threads : int
        The number of threads to be used during mutlithreading

        Warning
        -------
        The number of threads should be less than or equal to the number of
        physical cores and you should not attempt to make use of hyperthreading
        by using twice the number of physical cores. PySTE uses Eigen for
        multithreading which provides the following warning:

            Admonition
            ----------
            On most OS it is very important to limit the number of threads to
            the number of physical cores, otherwise significant slowdowns are
            expected

        For more details see
        https://eigen.tuxfamily.org/dox/TopicMultiThreading.html.

    See Also
    --------
    :func:`get_threads()`
    """
    pass

def _get_threads() -> int:
    """
    Gets the number of threads that will be used during multithreading.

    Returns
    -------
    int
        The number of threads that will be used during multithreading.

    See Also
    --------
    :func:`set_threads()`
    """
    pass

class UnitaryEvolver(pybind11_object):
    """
    A base class for
    :class:`DenseUnitaryEvolver`
    and
    :class:`SparseUnitaryEvolver`
    with no implemented functionality.
    
    The purpose of ``UnitaryEvolver`` is to allow for checks such as::

        isinstance(evolver, evolvers.UnitaryEvolver)

    See Also
    --------
    * :class:`DenseUnitaryEvolver`
    * :class:`SparseUnitaryEvolver`

        
    ---
    """
    pass

class DenseUnitaryEvolver(UnitaryEvolver):
    r"""
    A class to store the diagonalised drift and control Hamiltonians with dense
    matrices and dynamic values of ``n_ctrl`` and ``dim``. On initialisation the
    Hamiltonians are diagonalised and the eigenvectors and values stored as
    dense matrices. This initial diagonalisation may be slow and takes
    $O(\textrm{dim}^3)$
    time for a
    $\textrm{dim}\times \textrm{dim}$
    Hamiltonian. However, it  allows each step of the Suzuki-Trotter expansion
    to be implimented in
    $O(\textrm{dim}^2)$
    time with matrix multiplication and only scalar exponentiation opposed to
    matrix exponentiation which takes
    $O(\textrm{dim}^3)$
    time.

    Note
    ----
    This class is a Python wrapper around the C++ struct:

    .. code-block:: cpp
    
        Suzuki_Trotter_Evolver::UnitaryEvolver<Dynamic, Dynamic, DMatrix<Dynamic, Dynamic>>
        
    from
    `Suzuki-Trotter-Evolver <https://github.com/Christopher-K-Long/Suzuki-Trotter-Evolver>`__.

    Note
    ----
    Unlike :class:`DenseUnitaryEvolver_nctrl_dim`, :attr:`n_ctrl` and :attr:`dim`
    dynamically determined at runtime. :class:`DenseUnitaryEvolver_nctrl_dim` is
    typically more efficient as the values for :attr:`n_ctrl` and :attr:`dim`
    are baked in at compile time.

    See Also
    --------
    * :class:`DenseUnitaryEvolver_nctrl_dim`
    * :class:`SparseUnitaryEvolver`


    ---
    """
    
    n_ctrl: int = -1
    r"""
    The number of control Hamiltonians used to compile the C++ backend. A value
    of ``-1`` implies the value is not precompiled in the C++. This was the
    value at compile time while :attr:`length` is the value at runtime time.
    """
    
    dim: int = -1
    r"""
    The dimension of the vector space the Hamiltonians act upon used to compile
    the C++ backend. A value of ``-1`` implies the value is not precompiled in
    the C++.
    """
    
    dim_x_n_ctrl: int = -1
    r"""
    The dimension of rows in each control Hamiltonian multiplied by the
    number of control Hamiltonians upon used to compile the C++ backend. This is
    the number of rows for the ``control_hamiltonians`` argument for :meth:`__init__()`. A value
    of ``-1`` implies the value is not precompiled in the C++.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::dim_x_n_ctrl`.
    """
    
    length: int
    r"""
    The number of control Hamiltonians. This is the value at runtime while
    :attr:`n_ctrl` was the value at compile time. These two values will be equal
    unless ``n_ctrl==-1``. If ``n_ctrl==-1`` then `length` is the actual number
    of control Hamiltonians.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::length`.
    """
    
    d0: np.ndarray
    r"""
    The eigenvalues,
    $\operatorname{diag}(D_0)$,
    of the drift Hamiltonian:
    $H_0=U_0D_0U_0^\dagger$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::d0`.

    See Also
    --------
    * :attr:`ds`
    * :attr:`u0`
    * :attr:`u0_inverse`
    """
    
    ds: list[np.ndarray]
    r"""
    The eigenvalues,
    $\left(\operatorname{diag}(D_i)\right)_{i=1}^{\textrm{length}}$,
    of the control Hamiltonians:
    $H_i=U_iD_iU_i^\dagger$
    for all
    $i\in\left[\textrm{length}\right]$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::ds`.
    
    See Also
    --------
    * :attr:`d0`
    * :attr:`us_individual`
    * :attr:`us_inverse_individual`
    * :attr:`hs`
    """
    
    u0: np.ndarray
    r"""
    The unitary transformation,
    $U_0$,
    that diagonalises the drift Hamiltonian:
    $H_0=U_0D_0U_0^\dagger$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::u0`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`d0`
    * :attr:`u0_inverse`
    """
    
    u0_inverse: np.ndarray
    r"""
    The inverse of the unitary transformation,
    $U_0^\dagger$,
    that diagonalises the drift Hamiltonian:
    $H_0=U_0D_0U_0^\dagger$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::u0_inverse`.

    See Also
    --------
    * :attr:`us_inverse_individual`
    * :attr:`u0`
    * :attr:`d0`
    """
    
    us: list[np.ndarray]
    r"""
    The unitary transformations,
    $(U_i^\dagger U_{i-1})_{i=1}^{\textrm{length}}$,
    from the eigen basis of
    $H_{i-1}$
    to the eigen basis of
    $H_i$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::us`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`us_inverse_individual`
    """
    
    us_individual: list[np.ndarray]
    r"""
    The unitary transformations,
    $\left(U_i\right)_{i=1}^{\textrm{length}}$,
    that diagonalise the control Hamiltonians:
    $H_i=U_iD_iU_i^\dagger$
    for all
    $i\in\left[\textrm{length}\right]$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::us_individual`.

    See Also
    --------
    * :attr:`us_inverse_individual`
    * :attr:`us`
    * :attr:`ds`
    * :attr:`hs`
    """
    
    us_inverse_individual: list[np.ndarray]
    r"""
    The inverse of the unitary transformations,
    $(U_i^\dagger)_{i=1}^{\textrm{length}}$,
    that diagonalise the control Hamiltonians:
    $H_i=U_iD_iU_i^\dagger$
    for all
    $i\in\left[\textrm{length}\right]$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::us_inverse_individual`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`us`
    * :attr:`ds`
    * :attr:`hs`
    """
    
    hs: list[np.ndarray]
    r"""
    The control Hamiltonians:
    $H_i$
    for all
    $i\in\left[\textrm{length}\right]$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::hs`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`us_inverse_individual`
    * :attr:`ds`
    """
    
    u0_inverse_u_last: list[np.ndarray]
    r"""
    The unitary transformation,
    $U_0^\dagger U_{\textrm{length}}$,
    from the eigen basis of
    $H_{\textrm{length}}$
    to the eigen basis of
    $H_0$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::u0_inverse_u_last`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`us`
    * :attr:`u0_inverse`
    """
    
    def __init__(self,
                 drift_hamiltonian: np.ndarray[np.complex128],
                 control_hamiltonians: np.ndarray[np.complex128]):
        r"""
        Initialises a new unitary evolver with the Hamiltonian
        $$
        H(t)=H_0+\sum_{j=1}^{\textrm{length}}a_j(t)H_j,
        $$
        where $H_0$ is the drift Hamiltonian and $H_j$ are the control
        Hamiltonians modulated by control amplitudes $a_j(t)$ which need
        not be specified during initialisation.

        Parameters
        ----------
        drift_hamiltonian : NDArray[Shape[runtime_dim, runtime_dim], complex128]
            The drift Hamiltonian.
        control_hamiltonians : NDArray[Shape[runtime_dim * :attr:`length`, runtime_dim], complex128]
            The control Hamiltonians.
        """
        pass
    def propagate(self,
                  ctrl_amp: np.ndarray[np.complex128],
                  state: np.ndarray[np.complex128],
                  dt: float
                 ) -> np.ndarray[np.complex128]:
        r"""
        Propagates the state vector using the first-order Suzuki-Trotter
        expansion. More precisely, a state vector,
        $\psi(0)$,
        is evolved under the differential equation
        $$
        \dot\psi=-iH\psi
        $$
        using the first-order Suzuki-Trotter expansion:
        $$
        \begin{align}
        \psi(N\Delta t)&=\prod_{i=1}^N\prod_{j=0}^{\textrm{length}}
        e^{-ia_{ij}H_j\Delta t}\psi(0)+\mathcal E\\
        &=\prod_{i=1}^N\prod_{j=0}^{\textrm{length}}
        U_je^{-ia_{ij}D_j\Delta t}U_j^\dagger\psi(0)+\mathcal E.
        \end{align}
        $$
        where
        $a_{nj}\coloneqq a(n\Delta t)$,
        we set
        $a_{n0}=1$
        for notational ease, and the additive error
        $\mathcal E$
        is
        $$
        \begin{align}
        \mathcal E&=\mathcal O\left(
        \Delta t^2\left[\sum_{i=1}^N\sum_{j=1}^{\textrm{length}}\dot a_{ij}
        \norm{H_j}
        +\sum_{i=1}^N\sum_{j,k=0}^{\textrm{length}}a_{ij}a_{ik}
        \norm{[H_j,H_k]}\right]
        \right)\\
        &=\mathcal O\left(
        N\Delta t^2\textrm{length}\left[\omega E+\alpha^2+E^2\right]
        \right)
        \end{align}
        $$
        where $\dot a_{nj}\coloneqq\dot a_j(n\Delta t)$ and
        $$
        \begin{align}
        \omega&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[1,\textrm{length}\right]}}\left|\dot a_{ij}\right|,\\
        \alpha&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[0,\textrm{length}\right]}}\left|a_{ij}\right|,\\
        E&\coloneqq\max_{j\in\left[0,\textrm{length}\right]}\norm{H_j}.
        \end{align}
        $$
        Note the error is quadratic in $\Delta t$ but linear in $N$.
        We can also view this as being linear in $\Delta t$ and linear in
        total evolution time $N\Delta t$. Additionally, by Nyquist's theorem
        this asymptotic error scaling will not be achieved until the time step
        $\Delta t$ is smaller than $\frac{1}{2\Omega}$ where
        $\Omega$ is the largest energy or frequency in the system.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The state vector to propagate.
        dt : float
            ($\Delta t$) The time step to propagate by.

        Returns
        -------
        NDArray[Shape[runtime_dim], complex128]
            The propagated state vector, $\psi(N\Delta t)$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::propagate()`.

        See Also
        --------
        * :meth:`propagate_collection()`
        * :meth:`propagate_all()`
        """
        pass
    def propagate_collection(self,
                             ctrl_amp: np.ndarray[np.complex128],
                             states: np.ndarray[np.complex128],
                             dt: float
                            ) -> np.ndarray[np.complex128]:
        r"""
        Propagates a collection of state vectors using the first-order
        Suzuki-Trotter expansion. More precisely, a collection of state vectors,
        $\left(\psi_k(0)\right)_{k}$,
        are evolved under the differential equation
        $$
        \dot\psi_k=-iH\psi_k
        $$
        using the first-order Suzuki-Trotter expansion:     
        $$
        \begin{align}
        \psi_k(N\Delta t)&=\prod_{i=1}^N\prod_{j=0}^{\textrm{length}}
        e^{-ia_{ij}H_j\Delta t}\psi_k(0)+\mathcal E\\
        &=\prod_{i=1}^N\prod_{j=0}^{\textrm{length}}
        U_je^{-ia_{ij}D_j\Delta t}U_j^\dagger\psi_k(0)+\mathcal E.
        \end{align}
        $$
        where
        $a_{nj}\coloneqq a(n\Delta t)$,
        we set
        $a_{n0}=1$
        for notational ease, and the addative error
        $\mathcal E$
        is
        $$
        \begin{align}
        \mathcal E&=\mathcal O\left(
        \Delta t^2\left[\sum_{i=1}^N\sum_{j=1}^{\textrm{length}}\dot a_{ij}
        \norm{H_j}
        +\sum_{i=1}^N\sum_{j,k=0}^{\textrm{length}}a_{ij}a_{ik}
        \norm{[H_j,H_k]}\right]
        \right)\\
        &=\mathcal O\left(
        N\Delta t^2\textrm{length}\left[\omega E+\alpha^2+E^2\right]
        \right)
        \end{align}
        $$
        where $\dot a_{nj}\coloneqq\dot a_j(n\Delta t)$ and
        $$
        \begin{align}
        \omega&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[1,\textrm{length}\right]}}\left|\dot a_{ij}\right|,\\
        \alpha&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[0,\textrm{length}\right]}}\left|a_{ij}\right|,\\
        E&\coloneqq\max_{j\in\left[0,\textrm{length}\right]}\norm{H_j}.
        \end{align}
        $$
        Note the error is quadratic in $\Delta t$ but linear in $N$.
        We can also view this as being linear in $\Delta t$ and linear in
        total evolution time $N\Delta t$. Additionally, by Nyquist's theorem
        this asymptotic error scaling will not be achieved until the time step
        $\Delta t$ is smaller than $\frac{1}{2\Omega}$ where
        $\Omega$ is the largest energy or frequency in the system.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        states : NDArray[Shape[runtime_dim, number_of_states], complex128]
            $\left[\left(\psi(0)\right)_{k}\right]$ A collection of state
            vectors to propagate expressed as a matrix with each column
            corresponding to a state vector.
        dt : float
            ($\Delta t$) The time step to propagate by.

        Returns
        -------
        NDArray[Shape[runtime_dim, number_of_states], complex128]
            The propagated state vectors, $\left(\psi_k(N\Delta t)\right)_k$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::propagate_collection()`.

        See Also
        --------
        * :meth:`propagate()`
        * :meth:`propagate_all()`
        """
        pass
    def propagate_all(self,
                      ctrl_amp: np.ndarray[np.complex128],
                      state: np.ndarray[np.complex128],
                      dt: float
                     ) -> np.ndarray[np.complex128]:
        r"""
        Propagates the state vector using the first-order Suzuki-Trotter
        expansion and returns the resulting state vector at every time step.
        More precisely, a state vector,
        $\psi(0)$,
        is evolved under the differential equation
        $$
        \dot\psi=-iH\psi
        $$
        using the first-order Suzuki-Trotter expansion:     
        $$
        \begin{align}
        \psi(n\Delta t)&=\prod_{i=1}^n\prod_{j=0}^{\textrm{length}}
        e^{-ia_{ij}H_j\Delta t}\psi(0)+\mathcal E
        \quad\forall n\in\left[0, N\right]\\
        &=\prod_{i=1}^n\prod_{j=0}^{\textrm{length}}
        U_je^{-ia_{ij}D_j\Delta t}U_j^\dagger\psi(0)+\mathcal E
        \quad\forall n\in\left[0, N\right].
        \end{align}
        $$
        where
        $a_{nj}\coloneqq a(n\Delta t)$,
        we set
        $a_{n0}=1$
        for notational ease, and the additive error
        $\mathcal E$
        is
        $$
        \begin{align}
        \mathcal E&=\mathcal O\left(
        \Delta t^2\left[\sum_{i=1}^N\sum_{j=1}^{\textrm{length}}\dot a_{ij}
        \norm{H_j}
        +\sum_{i=1}^N\sum_{j,k=0}^{\textrm{length}}a_{ij}a_{ik}
        \norm{[H_j,H_k]}\right]
        \right)\\
        &=\mathcal O\left(
        N\Delta t^2\textrm{length}\left[\omega E+\alpha^2+E^2\right]
        \right)
        \end{align}
        $$
        where $\dot a_{nj}\coloneqq\dot a_j(n\Delta t)$ and
        $$
        \begin{align}
        \omega&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[1,\textrm{length}\right]}}\left|\dot a_{ij}\right|,\\
        \alpha&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[0,\textrm{length}\right]}}\left|a_{ij}\right|,\\
        E&\coloneqq\max_{j\in\left[0,\textrm{length}\right]}\norm{H_j}.
        \end{align}
        $$
        Note the error is quadratic in $\Delta t$ but linear in $N$.
        We can also view this as being linear in $\Delta t$ and linear in
        total evolution time $N\Delta t$. Additionally, by Nyquist's theorem
        this asymptotic error scaling will not be achieved until the time step
        $\Delta t$ is smaller than $\frac{1}{2\Omega}$ where
        $\Omega$ is the largest energy or frequency in the system.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The state vector to propagate.
        dt : float
            ($\Delta t$) The time step to propagate by.

        Returns
        -------
        NDArray[Shape[runtime_dim, time_steps + 1], complex128]
            The propagated state vector at each time step,
            $\left(\psi(n\Delta t)\right)_{n=0}^N$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::propagate_all()`.

        See Also
        --------
        * :meth:`propagate()`
        * :meth:`propagate_collection()`
        """
        pass
    def evolved_expectation_value(self,
                                  ctrl_amp: np.ndarray[np.complex128],
                                  state: np.ndarray[np.complex128],
                                  dt: float,
                                  observable: np.ndarray[np.complex128]
                                 ) -> complex:
        r"""
        Calculates the expectation value with respect to an observable of an
        evolved state vector evolved under a control Hamiltonian modulated by
        the control amplitudes. The integration is performed using
        :meth:`propagate()`.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The state vector to propagate.
        dt : float
            ($\Delta t$) The time step to propagate by.
        observable : NDArray[Shape[runtime_dim, runtime_dim], complex128]
            $(\hat O)$ The observable to calculate the expectation value of.

        Returns
        -------
        complex
            The expectation value of the observable, $\langle\hat O\rangle
            \equiv\psi^\dagger(N\Delta t)\hat O\psi(N\Delta t)$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::evolved_expectation_value()`.

        See Also
        --------
        * :meth:`evolved_expectation_value_all()`
        """
        pass
    def evolved_expectation_value_all(self,
                                      ctrl_amp: np.ndarray[np.complex128],
                                      state: np.ndarray[np.complex128],
                                      dt: float,
                                      observable: np.ndarray[np.complex128]
                                     ) -> np.ndarray[np.complex128]:
        r"""
        Calculates the expectation values with respect to an observable of a
        time series of state vectors evolved under a control Hamiltonian
        modulated by the control amplitudes. The integration is performed using
        :meth:`propagate_all()`.

        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The state vector to propagate.
        dt : float
            ($\Delta t$) The time step to propagate by.
        observable : NDArray[Shape[runtime_dim, runtime_dim], complex128]
            $(\hat O)$ The observable to calculate the expectation value of.

        Returns
        -------
        NDArray[Shape[time_steps + 1], complex128]
            The expectation value of the observable,
            $\left(\psi^\dagger(n\Delta t)\hat O\psi(N\Delta t)\right)_{n=0}^N$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::evolved_expectation_value_all()`.

        See Also
        --------
        * :meth:`evolved_expectation_value()`
        """
        pass
    def switching_function(self,
                           ctrl_amp: np.ndarray[np.complex128],
                           state: np.ndarray[np.complex128],
                           dt: float,
                           cost: np.ndarray[np.complex128]
                          ) -> tuple[complex, np.ndarray[np.float64]]:
        r"""
        Calculates the switching function for a Mayer problem with an
        expectation value as the cost function. More precisely if the cost
        function is
        $$
        J\left[\vec a(t)\right]\coloneqq\langle\hat O\rangle
        \equiv\psi^\dagger[\vec a(t);T]
        \hat O\psi[\vec a(t);T],
        $$
        where $T=N\Delta t$, then the switching function is
        $$
        \phi_j(t)\coloneqq\frac{\delta J}{\delta a_j(t)}
        =2\operatorname{Im}\left(\psi^\dagger[\vec a(t);T]
        \hat OU(t\to T)H_j\psi[\vec a(t);t]\right).
        $$
        using the first-order Suzuki-Trotter expansion we can express the
        switching function as
        $$
        \begin{align}
        &\phi_j(n\Delta t)=\frac{1}{\Delta t}\pdv{J}{a_{nj}}\\
        &=\!2\operatorname{Im}\!\left(\psi^\dagger(T)
        \hat O\!\!\left[\prod_{i>n}^N\prod_{k=1}^{\textrm{length}}
        e^{-ia_{ik}H_k\Delta t}\right]\!\!\!
        \left[\prod_{k=j}^{\textrm{length}}
        e^{-ia_{nk}H_k\Delta t}\right]\!H_j\!\!
        \left[\prod_{k=0}^{j-1}
        e^{-ia_{nk}H_k\Delta t}\right]
        \!\psi(\left[n-1\right]\Delta t)\right),
        \end{align}
        $$
        where for numerical efficiency we replace
        $e^{-ia_{ik}H_k\Delta t}$
        with
        $U_ke^{-ia_{ik}D_k\Delta t}U_k^\dagger$
        as in :meth:`propagate()`.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The initial state vector.
        dt : float
            ($\Delta t$) The time step.
        cost : NDArray[Shape[runtime_dim, runtime_dim], complex128]
            $(\hat O)$ The observable to calculate the expectation value of.

        Returns
        -------
        tuple[complex, NDArray[Shape[time_steps, :attr:`length`], float64]]
            The expectation value, $\psi^\dagger(T)\hat O\psi(T)$, and
            the switching function,
            $\phi_j(n\Delta t)$
            for all
            $j\in\left[1,\textrm{length}\right]$
            and
            $n\in\left[1,N\right]$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::switching_function()`.
        """
        pass

class SparseUnitaryEvolver(UnitaryEvolver):
    r"""
    A class to store the diagonalised drift and control Hamiltonians with sparse
    matrices and dynamic values of ``n_ctrl`` and ``dim``. On initialisation the
    Hamiltonians are diagonalised and the eigenvectors and values stored as
    sparse and dense matrices, respectively. This initial diagonalisation may be
    slow and takes
    $O(\textrm{dim}^3)$
    time for a
    $\textrm{dim}\times \textrm{dim}$
    Hamiltonian. However, it  allows each step of the Suzuki-Trotter expansion
    to be implimented with sparse matrix multiplication and only scalar
    exponentiation opposed to matrix exponentiation.

    Note
    ----
    This class is a Python wrapper around the C++ struct:

    .. code-block:: cpp
    
        Suzuki_Trotter_Evolver::UnitaryEvolver<Dynamic, Dynamic, SMatrix<Dynamic, Dynamic>>
        
    from
    `Suzuki-Trotter-Evolver <https://github.com/Christopher-K-Long/Suzuki-Trotter-Evolver>`__.

    Note
    ----
    Unlike :class:`SparseUnitaryEvolver_nctrl_dim`, :attr:`n_ctrl` and
    :attr:`dim` dynamically determined at runtime.
    :class:`SparseUnitaryEvolver_nctrl_dim` is typically more efficient as the
    values for :attr:`n_ctrl` and :attr:`dim` are baked in at compile time.

    See Also
    --------
    * :class:`SparseUnitaryEvolver_nctrl_dim`
    * :class:`DenseUnitaryEvolver`


    ---
    """
    
    n_ctrl: int = -1
    r"""
    The number of control Hamiltonians used to compile the C++ backend. A value
    of ``-1`` implies the value is not precompiled in the C++. This was the value
    at compile time while :attr:`length` is the value at runtime time.
    """
    
    dim: int = -1
    r"""
    The dimension of the vector space the Hamiltonians act upon used to compile
    the C++ backend. A value of ``-1`` implies the value is not precompiled in
    the C++.
    """
    
    dim_x_n_ctrl: int = -1
    r"""
    The dimension of rows in each control Hamiltonian multiplied by the
    number of control Hamiltonians upon used to compile the C++ backend. This is
    the number of rows for the ``control_hamiltonians`` argument for
    :meth:`__init__()`. A value of ``-1`` implies the value is not precompiled
    in the C++.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::dim_x_n_ctrl`.
    """
    
    length: int
    r"""
    The number of control Hamiltonians. This is the value at runtime while
    :attr:`n_ctrl` was the value at compile time. These two values will be equal
    unless ``n_ctrl==-1``. If ``n_ctrl==-1`` then `length` is the actual number
    of control Hamiltonians.
    
    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::length`.
    """
    
    d0: np.ndarray
    r"""
    The eigenvalues,
    $\operatorname{diag}(D_0)$,
    of the drift Hamiltonian:
    $H_0=U_0D_0U_0^\dagger$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::d0`.

    See Also
    --------
    * :attr:`ds`
    * :attr:`u0`
    * :attr:`u0_inverse`
    """
    
    ds: list[np.ndarray]
    r"""
    The eigenvalues,
    $\left(\operatorname{diag}(D_i)\right)_{i=1}^{\textrm{length}}$,
    of the control Hamiltonians:
    $H_i=U_iD_iU_i^\dagger$
    for all
    $i\in\left[\textrm{length}\right]$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::ds`.

    See Also
    --------
    * :attr:`d0`
    * :attr:`us_individual`
    * :attr:`us_inverse_individual`
    * :attr:`hs`
    """
    
    u0: np.ndarray
    r"""
    The unitary transformation,
    $U_0$,
    that diagonalises the drift Hamiltonian:
    $H_0=U_0D_0U_0^\dagger$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::u0`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`d0`
    * :attr:`u0_inverse`
    """
    
    u0_inverse: np.ndarray
    r"""
    The inverse of the unitary transformation,
    $U_0^\dagger$,
    that diagonalises the drift Hamiltonian:
    $H_0=U_0D_0U_0^\dagger$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::u0_inverse`.

    See Also
    --------
    * :attr:`us_inverse_individual`
    * :attr:`u0`
    * :attr:`d0`
    """
    
    us: list[np.ndarray]
    r"""
    The unitary transformations,
    $(U_i^\dagger U_{i-1})_{i=1}^{\textrm{length}}$,
    from the eigen basis of
    $H_{i-1}$
    to the eigen basis of
    $H_i$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::us`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`us_inverse_individual`
    """
    
    us_individual: list[np.ndarray]
    r"""
    The unitary transformations,
    $\left(U_i\right)_{i=1}^{\textrm{length}}$,
    that diagonalise the control Hamiltonians:
    $H_i=U_iD_iU_i^\dagger$
    for all
    $i\in\left[\textrm{length}\right]$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::us_individual`.

    See Also
    --------
    * :attr:`us_inverse_individual`
    * :attr:`us`
    * :attr:`ds`
    * :attr:`hs`
    """
    
    us_inverse_individual: list[np.ndarray]
    r"""
    The inverse of the unitary transformations,
    $(U_i^\dagger)_{i=1}^{\textrm{length}}$,
    that diagonalise the control Hamiltonians:
    $H_i=U_iD_iU_i^\dagger$
    for all
    $i\in\left[\textrm{length}\right]$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::us_inverse_individual`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`us`
    * :attr:`ds`
    * :attr:`hs`
    """
    
    hs: list[np.ndarray]
    r"""
    The control Hamiltonians:
    $H_i$
    for all
    $i\in\left[\textrm{length}\right]$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::hs`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`us_inverse_individual`
    * :attr:`ds`
    """
    
    u0_inverse_u_last: list[np.ndarray]
    r"""
    The unitary transformation,
    $U_0^\dagger U_{\textrm{length}}$,
    from the eigen basis of
    $H_{\textrm{length}}$
    to the eigen basis of
    $H_0$.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::u0_inverse_u_last`.

    See Also
    --------
    * :attr:`us_individual`
    * :attr:`us`
    * :attr:`u0_inverse`
    """
    
    def __init__(self,
                 drift_hamiltonian: np.ndarray[np.complex128],
                 control_hamiltonians: np.ndarray[np.complex128]):
        r"""
        Initialises a new unitary evolver with the Hamiltonian
        $$
        H(t)=H_0+\sum_{j=1}^{\textrm{length}}a_j(t)H_j,
        $$
        where $H_0$ is the drift Hamiltonian and $H_j$ are the control
        Hamiltonians modulated by control amplitudes $a_j(t)$ which need
        not be specified during initialisation.

        Parameters
        ----------
        drift_hamiltonian : NDArray[Shape[runtime_dim, runtime_dim], complex128]
            The drift Hamiltonian.
        control_hamiltonians : NDArray[Shape[runtime_dim * :attr:`length`, runtime_dim], complex128]
            The control Hamiltonians.
        """
        pass
    def propagate(self,
                  ctrl_amp: np.ndarray[np.complex128],
                  state: np.ndarray[np.complex128],
                  dt: float
                 ) -> np.ndarray[np.complex128]:
        r"""
        Propagates the state vector using the first-order Suzuki-Trotter
        expansion. More precisely, a state vector,
        $\psi(0)$,
        is evolved under the differential equation
        $$
        \dot\psi=-iH\psi
        $$
        using the first-order Suzuki-Trotter expansion:
        $$
        \begin{align}
        \psi(N\Delta t)&=\prod_{i=1}^N\prod_{j=0}^{\textrm{length}}
        e^{-ia_{ij}H_j\Delta t}\psi(0)+\mathcal E\\
        &=\prod_{i=1}^N\prod_{j=0}^{\textrm{length}}
        U_je^{-ia_{ij}D_j\Delta t}U_j^\dagger\psi(0)+\mathcal E.
        \end{align}
        $$
        where
        $a_{nj}\coloneqq a(n\Delta t)$,
        we set
        $a_{n0}=1$
        for notational ease, and the additive error
        $\mathcal E$
        is
        $$
        \begin{align}
        \mathcal E&=\mathcal O\left(
        \Delta t^2\left[\sum_{i=1}^N\sum_{j=1}^{\textrm{length}}\dot a_{ij}
        \norm{H_j}
        +\sum_{i=1}^N\sum_{j,k=0}^{\textrm{length}}a_{ij}a_{ik}
        \norm{[H_j,H_k]}\right]
        \right)\\
        &=\mathcal O\left(
        N\Delta t^2\textrm{length}\left[\omega E+\alpha^2+E^2\right]
        \right)
        \end{align}
        $$
        where $\dot a_{nj}\coloneqq\dot a_j(n\Delta t)$ and
        $$
        \begin{align}
        \omega&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[1,\textrm{length}\right]}}\left|\dot a_{ij}\right|,\\
        \alpha&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[0,\textrm{length}\right]}}\left|a_{ij}\right|,\\
        E&\coloneqq\max_{j\in\left[0,\textrm{length}\right]}\norm{H_j}.
        \end{align}
        $$
        Note the error is quadratic in $\Delta t$ but linear in $N$.
        We can also view this as being linear in $\Delta t$ and linear in
        total evolution time $N\Delta t$. Additionally, by Nyquist's theorem
        this asymptotic error scaling will not be achieved until the time step
        $\Delta t$ is smaller than $\frac{1}{2\Omega}$ where
        $\Omega$ is the largest energy or frequency in the system.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The state vector to propagate.
        dt : float
            ($\Delta t$) The time step to propagate by.

        Returns
        -------
        NDArray[Shape[runtime_dim], complex128]
            The propagated state vector, $\psi(N\Delta t)$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::propagate()`.

        See Also
        --------
        * :meth:`propagate_collection()`
        * :meth:`propagate_all()`
        """
        pass
    def propagate_collection(self,
                             ctrl_amp: np.ndarray[np.complex128],
                             states: np.ndarray[np.complex128],
                             dt: float
                            ) -> np.ndarray[np.complex128]:
        r"""
        Propagates a collection of state vectors using the first-order
        Suzuki-Trotter expansion. More precisely, a collection of state vectors,
        $\left(\psi_k(0)\right)_{k}$,
        are evolved under the differential equation
        $$
        \dot\psi_k=-iH\psi_k
        $$
        using the first-order Suzuki-Trotter expansion:     
        $$
        \begin{align}
        \psi_k(N\Delta t)&=\prod_{i=1}^N\prod_{j=0}^{\textrm{length}}
        e^{-ia_{ij}H_j\Delta t}\psi_k(0)+\mathcal E\\
        &=\prod_{i=1}^N\prod_{j=0}^{\textrm{length}}
        U_je^{-ia_{ij}D_j\Delta t}U_j^\dagger\psi_k(0)+\mathcal E.
        \end{align}
        $$
        where
        $a_{nj}\coloneqq a(n\Delta t)$,
        we set
        $a_{n0}=1$
        for notational ease, and the addative error
        $\mathcal E$
        is
        $$
        \begin{align}
        \mathcal E&=\mathcal O\left(
        \Delta t^2\left[\sum_{i=1}^N\sum_{j=1}^{\textrm{length}}\dot a_{ij}
        \norm{H_j}
        +\sum_{i=1}^N\sum_{j,k=0}^{\textrm{length}}a_{ij}a_{ik}
        \norm{[H_j,H_k]}\right]
        \right)\\
        &=\mathcal O\left(
        N\Delta t^2\textrm{length}\left[\omega E+\alpha^2+E^2\right]
        \right)
        \end{align}
        $$
        where $\dot a_{nj}\coloneqq\dot a_j(n\Delta t)$ and
        $$
        \begin{align}
        \omega&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[1,\textrm{length}\right]}}\left|\dot a_{ij}\right|,\\
        \alpha&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[0,\textrm{length}\right]}}\left|a_{ij}\right|,\\
        E&\coloneqq\max_{j\in\left[0,\textrm{length}\right]}\norm{H_j}.
        \end{align}
        $$
        Note the error is quadratic in $\Delta t$ but linear in $N$.
        We can also view this as being linear in $\Delta t$ and linear in
        total evolution time $N\Delta t$. Additionally, by Nyquist's theorem
        this asymptotic error scaling will not be achieved until the time step
        $\Delta t$ is smaller than $\frac{1}{2\Omega}$ where
        $\Omega$ is the largest energy or frequency in the system.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        states : NDArray[Shape[runtime_dim, number_of_states], complex128]
            $\left[\left(\psi(0)\right)_{k}\right]$ A collection of state
            vectors to propagate expressed as a matrix with each column
            corresponding to a state vector.
        dt : float
            ($\Delta t$) The time step to propagate by.

        Returns
        -------
        NDArray[Shape[runtime_dim, number_of_states], complex128]
            The propagated state vectors, $\left(\psi_k(N\Delta t)\right)_k$.
            
        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::propagate_collection()`.

        See Also
        --------
        * :meth:`propagate()`
        * :meth:`propagate_all()`
        """
        pass
    def propagate_all(self,
                      ctrl_amp: np.ndarray[np.complex128],
                      state: np.ndarray[np.complex128],
                      dt: float
                     ) -> np.ndarray[np.complex128]:
        r"""
        Propagates the state vector using the first-order Suzuki-Trotter
        expansion and returns the resulting state vector at every time step.
        More precisely, a state vector,
        $\psi(0)$,
        is evolved under the differential equation
        $$
        \dot\psi=-iH\psi
        $$
        using the first-order Suzuki-Trotter expansion:     
        $$
        \begin{align}
        \psi(n\Delta t)&=\prod_{i=1}^n\prod_{j=0}^{\textrm{length}}
        e^{-ia_{ij}H_j\Delta t}\psi(0)+\mathcal E
        \quad\forall n\in\left[0, N\right]\\
        &=\prod_{i=1}^n\prod_{j=0}^{\textrm{length}}
        U_je^{-ia_{ij}D_j\Delta t}U_j^\dagger\psi(0)+\mathcal E
        \quad\forall n\in\left[0, N\right].
        \end{align}
        $$
        where
        $a_{nj}\coloneqq a(n\Delta t)$,
        we set
        $a_{n0}=1$
        for notational ease, and the additive error
        $\mathcal E$
        is
        $$
        \begin{align}
        \mathcal E&=\mathcal O\left(
        \Delta t^2\left[\sum_{i=1}^N\sum_{j=1}^{\textrm{length}}\dot a_{ij}
        \norm{H_j}
        +\sum_{i=1}^N\sum_{j,k=0}^{\textrm{length}}a_{ij}a_{ik}
        \norm{[H_j,H_k]}\right]
        \right)\\
        &=\mathcal O\left(
        N\Delta t^2\textrm{length}\left[\omega E+\alpha^2+E^2\right]
        \right)
        \end{align}
        $$
        where $\dot a_{nj}\coloneqq\dot a_j(n\Delta t)$ and
        $$
        \begin{align}
        \omega&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[1,\textrm{length}\right]}}\left|\dot a_{ij}\right|,\\
        \alpha&\coloneqq\max_{\substack{i\in\left[1,N\right]\\
        j\in\left[0,\textrm{length}\right]}}\left|a_{ij}\right|,\\
        E&\coloneqq\max_{j\in\left[0,\textrm{length}\right]}\norm{H_j}.
        \end{align}
        $$
        Note the error is quadratic in $\Delta t$ but linear in $N$.
        We can also view this as being linear in $\Delta t$ and linear in
        total evolution time $N\Delta t$. Additionally, by Nyquist's theorem
        this asymptotic error scaling will not be achieved until the time step
        $\Delta t$ is smaller than $\frac{1}{2\Omega}$ where
        $\Omega$ is the largest energy or frequency in the system.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The state vector to propagate.
        dt : float
            ($\Delta t$) The time step to propagate by.

        Returns
        -------
        NDArray[Shape[runtime_dim, time_steps + 1], complex128]
            The propagated state vector at each time step,
            $\left(\psi(n\Delta t)\right)_{n=0}^N$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::propagate_all()`.

        See Also
        --------
        * :meth:`propagate()`
        * :meth:`propagate_collection()`
        """
        pass
    def evolved_expectation_value(self,
                                  ctrl_amp: np.ndarray[np.complex128],
                                  state: np.ndarray[np.complex128],
                                  dt: float,
                                  observable: np.ndarray[np.complex128]
                                 ) -> complex:
        r"""
        Calculates the expectation value with respect to an observable of an
        evolved state vector evolved under a control Hamiltonian modulated by
        the control amplitudes. The integration is performed using
        :meth:`propagate()`.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The state vector to propagate.
        dt : float
            ($\Delta t$) The time step to propagate by.
        observable : NDArray[Shape[runtime_dim, runtime_dim], complex128]
            $(\hat O)$ The observable to calculate the expectation value of.

        Returns
        -------
        complex
            The expectation value of the observable, $\langle\hat O\rangle
            \equiv\psi^\dagger(N\Delta t)\hat O\psi(N\Delta t)$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::evolved_expectation_value()`.

        See Also
        --------
        * :meth:`evolved_expectation_value_all()`
        """
        pass
    def evolved_expectation_value_all(self,
                                      ctrl_amp: np.ndarray[np.complex128],
                                      state: np.ndarray[np.complex128],
                                      dt: float,
                                      observable: np.ndarray[np.complex128]
                                     ) -> np.ndarray[np.complex128]:
        r"""
        Calculates the expectation values with respect to an observable of a
        time series of state vectors evolved under a control Hamiltonian
        modulated by the control amplitudes. The integration is performed using
        :meth:`propagate_all()`.

        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The state vector to propagate.
        dt : float
            ($\Delta t$) The time step to propagate by.
        observable : NDArray[Shape[runtime_dim, runtime_dim], complex128]
            $(\hat O)$ The observable to calculate the expectation value of.

        Returns
        -------
        NDArray[Shape[time_steps + 1], complex128]
            The expectation value of the observable,
            $\left(\psi^\dagger(n\Delta t)\hat O\psi(N\Delta t)\right)_{n=0}^N$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::evolved_expectation_value_all()`.

        See Also
        --------
        * :meth:`evolved_expectation_value()`
        """
        pass
    def switching_function(self,
                           ctrl_amp: np.ndarray[np.complex128],
                           state: np.ndarray[np.complex128],
                           dt: float,
                           cost: np.ndarray[np.complex128]
                          ) -> tuple[complex, np.ndarray[np.float64]]:
        r"""
        Calculates the switching function for a Mayer problem with an
        expectation value as the cost function. More precisely if the cost
        function is
        $$
        J\left[\vec a(t)\right]\coloneqq\langle\hat O\rangle
        \equiv\psi^\dagger[\vec a(t);T]
        \hat O\psi[\vec a(t);T],
        $$
        where $T=N\Delta t$, then the switching function is
        $$
        \phi_j(t)\coloneqq\frac{\delta J}{\delta a_j(t)}
        =2\operatorname{Im}\left(\psi^\dagger[\vec a(t);T]
        \hat OU(t\to T)H_j\psi[\vec a(t);t]\right).
        $$
        using the first-order Suzuki-Trotter expansion we can express the
        switching function as
        $$
        \begin{align}
        &\phi_j(n\Delta t)=\frac{1}{\Delta t}\pdv{J}{a_{nj}}\\
        &=\!2\operatorname{Im}\!\left(\psi^\dagger(T)
        \hat O\!\!\left[\prod_{i>n}^N\prod_{k=1}^{\textrm{length}}
        e^{-ia_{ik}H_k\Delta t}\right]\!\!\!
        \left[\prod_{k=j}^{\textrm{length}}
        e^{-ia_{nk}H_k\Delta t}\right]\!H_j\!\!
        \left[\prod_{k=0}^{j-1}
        e^{-ia_{nk}H_k\Delta t}\right]
        \!\psi(\left[n-1\right]\Delta t)\right),
        \end{align}
        $$
        where for numerical efficiency we replace
        $e^{-ia_{ik}H_k\Delta t}$
        with
        $U_ke^{-ia_{ik}D_k\Delta t}U_k^\dagger$
        as in :meth:`propagate()`.

        Parameters
        ----------
        ctrl_amp : NDArray[Shape[time_steps, :attr:`length`], complex128]
            $\left(a_{ij}\right)$ The control amplitudes at each time step
            expressed as an $N\times\textrm{length}$ matrix where the element
            $a_{ij}$ corresponds to the control amplitude of the $j$th control
            Hamiltonian at the $i$th time step.
        state : NDArray[Shape[runtime_dim], complex128]
            $\left[\psi(0)\right]$ The initial state vector.
        dt : float
            ($\Delta t$) The time step.
        cost : NDArray[Shape[runtime_dim, runtime_dim], complex128]
            $(\hat O)$ The observable to calculate the expectation value of.

        Returns
        -------
        tuple[complex, NDArray[Shape[time_steps, :attr:`length`], float64]]
            The expectation value, $\psi^\dagger(T)\hat O\psi(T)$, and
            the switching function,
            $\phi_j(n\Delta t)$
            for all
            $j\in\left[1,\textrm{length}\right]$
            and
            $n\in\left[1,N\right]$.

        Note
        ----
        This function is a wrapper around the C++ function
        :cpp:func:`Suzuki_Trotter_Evolver::UnitaryEvolver::switching_function()`.
        """
        pass

class DenseUnitaryEvolver_nctrl_dim(DenseUnitaryEvolver):
    r"""
    A class to store the diagonalised drift and control Hamiltonians with dense
    matrices and precompiled values of ``n_ctrl`` and ``dim``.

    Important
    ---------
    This is not the actual class name ``nctrl`` and ``dim`` should be replaced
    with positive integers to specify their values. For example,
    ``DenseUnitaryEvolver_3_2`` is a valid class name with :attr:`n_ctrl`
    ``=3`` control Hamiltonians acting on a :attr:`dim` ``=2`` dimensional
    vector space. If only one of ``nctrl`` and ``dim`` is precompiled the other
    should be specified as `Dynamic`. For example,
    ``DenseUnitaryEvolver_Dynamic_2`` is a valid class name with a dynamic
    number of control Hamiltonians (:attr:`n_ctrl` ``=-1``) acting on a
    :attr:`dim` ``=2`` dimensional vector space.


    On initialisation the Hamiltonians are diagonalised and the eigenvectors and
    values stored as dense matrices. This initial diagonalisation may be slow
    and takes
    $O(\textrm{dim}^3)$
    time for a
    $\textrm{dim}\times \textrm{dim}$
    Hamiltonian. However, it  allows each step of the Suzuki-Trotter expansion
    to be implimented in
    $O(\textrm{dim}^2)$
    time with matrix multiplication and only scalar exponentiation opposed to
    matrix exponentiation which takes
    $O(\textrm{dim}^3)$
    time.

    Note
    ----
    This class is a Python wrapper around the C++ struct:

    .. code-block:: cpp
    
        Suzuki_Trotter_Evolver::UnitaryEvolver<n_ctrl, dim, DMatrix<dim, dim>>
        
    from
    `Suzuki-Trotter-Evolver <https://github.com/Christopher-K-Long/Suzuki-Trotter-Evolver>`__.

    Note
    ----
    Unlike :class:`DenseUnitaryEvolver`, :attr:`n_ctrl` and :attr:`dim` are
    baked into the class when the C++ code is compiled allowing for more
    efficient state propagation.

    See Also
    --------
    * :class:`SparseUnitaryEvolver_nctrl_dim`
    * :class:`DenseUnitaryEvolver`


    ---
    """
    
    n_ctrl: int = None
    r"""
    The number of control Hamiltonians used to compile the C++ backend. Equal to
    the value in the class name. A value of ``-1`` represents ``Dynamic`` in the
    class name and implies the value is not precompiled in the C++. This was the
    value at compile time while :attr:`length` is the value at runtime time.
    """
    
    dim: int = None
    r"""
    The dimension of the vector space the Hamiltonians act upon used to compile
    the C++ backend. Equal to the value in the class name. A value of ``-1``
    represents ``Dynamic`` in the class name and implies the value is not
    precompiled in the C++.
    """

    dim_x_n_ctrl: int = None
    r"""
    The dimension of rows in each control Hamiltonian multiplied by the
    number of control Hamiltonians upon used to compile the C++ backend. This is
    the number of rows for the ``control_hamiltonians`` argument for
    :meth:`__init__()`. A value of ``-1`` implies the value is not precompiled
    in the C++.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::dim_x_n_ctrl`.
    """

class SparseUnitaryEvolver_nctrl_dim(SparseUnitaryEvolver):
    r"""
    A class to store the diagonalised drift and control Hamiltonians with sparse
    matrices and precompiled values of ``n_ctrl`` and ``dim``.

    Important
    ---------
    This is not the actual class name ``nctrl`` and ``dim`` should be replaced
    with positive integers to specify their values. For example,
    ``SparseUnitaryEvolver_3_2`` is a valid class name with :attr:`n_ctrl`
    ``=3`` control Hamiltonians acting on a :attr:`dim` ``=2`` dimensional
    vector space. If only one of ``nctrl`` and ``dim`` is precompiled the other
    should be specified as `Dynamic`. For example,
    ``SparseUnitaryEvolver_Dynamic_2`` is a valid class name with a dynamic
    number of control Hamiltonians (:attr:`n_ctrl` ``=-1``) acting on a
    :attr:`dim` ``=2`` dimensional vector space.


    On initialisation the Hamiltonians are diagonalised and the eigenvectors and
    values stored as sparse and dense matrices, respectively. This initial
    diagonalisation may be slow and takes
    $O(\textrm{dim}^3)$
    time for a
    $\textrm{dim}\times \textrm{dim}$
    Hamiltonian. However, it  allows each step of the Suzuki-Trotter expansion
    to be implimented with sparse matrix multiplication and only scalar
    exponentiation opposed to matrix exponentiation.

    Note
    ----
    This class is a Python wrapper around the C++ struct:

    .. code-block:: cpp
    
        Suzuki_Trotter_Evolver::UnitaryEvolver<n_ctrl, dim, SMatrix>
        
    from
    `Suzuki-Trotter-Evolver <https://github.com/Christopher-K-Long/Suzuki-Trotter-Evolver>`__.

    Note
    ----
    Unlike :class:`SparseUnitaryEvolver`, :attr:`n_ctrl` and :attr:`dim` are
    baked into the class when the C++ code is compiled allowing for more
    efficient state propagation.

    See Also
    --------
    * :class:`DenseUnitaryEvolver_nctrl_dim`
    * :class:`SparseUnitaryEvolver`


    ---
    """
    
    n_ctrl: int = None
    r"""
    The number of control Hamiltonians used to compile the C++ backend. Equal to
    the value in the class name. A value of ``-1`` represents ``Dynamic`` in the
    class name and implies the value is not precompiled in the C++. This was the
    value at compile time while :attr:`length` is the value at runtime time.
    """
    
    dim: int = None
    r"""
    The dimension of the vector space the Hamiltonians act upon used to compile
    the C++ backend. Equal to the value in the class name. A value of ``-1``
    represents ``Dynamic`` in the class name and implies the value is not
    precompiled in the C++.
    """
    
    dim_x_n_ctrl: int = None
    r"""
    The dimension of rows in each control Hamiltonian multiplied by the
    number of control Hamiltonians upon used to compile the C++ backend. This is
    the number of rows for the ``control_hamiltonians`` argument for :meth:`__init__()`. A value
    of ``-1`` implies the value is not precompiled in the C++.

    Note
    ----
    This is a wrapper around the C++ member
    :cpp:member:`Suzuki_Trotter_Evolver::UnitaryEvolver::dim_x_n_ctrl`.
    """