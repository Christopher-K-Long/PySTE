import os
import sys
FILE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(os.path.dirname(FILE_DIR), "examples"))


def test_Rabi_oscillation():
    import Rabi_oscillation

def test_compute_switching_function():
    import compute_switching_function