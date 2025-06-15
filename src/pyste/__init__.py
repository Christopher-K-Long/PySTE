"""
A Python package for evolving states under the Schrödinger equation using
first-order Suzuki-Trotter and computing switching functions.
"""
from ._wrapper import get_unitary_evolver
from .evolvers import _set_threads as set_threads, \
                      _get_threads as get_threads