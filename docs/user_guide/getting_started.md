# Getting Started

## What is PySTE

PySTE is a Python wrapper around [Suzuki-Trotter-Evolver](https://github.com/Christopher-K-Long/Suzuki-Trotter-Evolver): a header-only library for evolving states under the Schrödinger equation,

$$
\dot\psi=-iH\psi,
$$(getting_started_1)

using the first-order Suzuki-Trotter expansion and computing switching functions. This library assumes Hamiltonians take the form:

$$
H(t)=H_0+\sum_{j=1}^{\textrm{length}}a_j(t)H_j,
$$(getting_started_2)

where $H_0$ is called the drift Hamiltonian and $\left\{H_j\right\}_{j=1}^{\textrm{length}}$ are the control Hamiltonians which are modulated by the control amplitudes $\left\{a_j(t)\right\}_{j=1}^{\textrm{length}}$.
PySTE integrates the Schrödinger equation by diagonalising the drift and control
Hamiltonians ahead of time so that no matrix exponentials are required in the Suzuki-Trotter expansion. This
yields an upfront cost of $O(\dim^3)$ where $\dim$ is the dimension of the vector space the Hamiltonians act upon. However, integrating the Schrödinger equation will scale with $\dim$ as $O(\dim^2)$ opposed to $O(\dim^3)$.

This user guide is almost identical to the [user guide for Suzuki-Trotter-Evolver](https://suzuki-trotter-evolver.readthedocs.io/en/latest/user_guide) but with C++ examples replaced with Python examples. 

## Installation

```{include} ../../README.md
:start-after: "## Installation"
:end-before: "## Cloning the repository"
```

## Quick Start

A good starting point in experimenting with a new integrator for quantum systems is to try and reproduce a Rabi Oscillation. Consider the Hamiltonian

$$
H(t)=\frac{1}{2}vZ+f\cos(vt)X,
$$(getting_started_3)

where $X$ and $Z$ are the Pauli-$x$ and -$z$ matrices, respectively. This Hamiltonian produces on resonance Rabi-oscillations at a frequency $f$. Suppose we initialise a in the state $\psi(0)=\begin{pmatrix}1&0\end{pmatrix}^\intercal$ and want to know the state $\psi(t=T)$ at a time $t=T$. The following program will print this state to the console:

```{literalinclude} ../../examples/Rabi_oscillation.py
```

---
[Previous](overview.md) | [Next](state_vector_evolution.md)