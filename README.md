# PySTE
A Python package for evolving states under the Schrödinger equation using first-order Suzuki-Trotter and computing switching functions.

[![Unit Tests](https://github.com/Christopher-K-Long/PySTE/actions/workflows/test-python-package.yml/badge.svg)](https://github.com/Christopher-K-Long/PySTE/actions/workflows/test-python-package.yml)

PySTE stands for Python Suzuki-Trotter-Evolver and is a Python interface to the C++ header-only library [https://github.com/Christopher-K-Long/Suzuki-Trotter-Evolver](https://github.com/Christopher-K-Long/Suzuki-Trotter-Evolver).

While PySTE has limited functionality in comparison to more fleshed out quantum simulation packages such as [QuTiP](https://qutip.org), it is faster at some tasks:

![benchmark PySTE vs QuTiP](https://pyste.readthedocs.io/en/latest/_images/benchmark_against_qutip.png)

More detailed benchmarks can be found here: [https://PySTE.readthedocs.io/en/latest/benchmarks/index.html](https://PySTE.readthedocs.io/en/latest/benchmarks/index.html)

## Installation

PySTE can be installed as follows:

```bash
pip install py-ste
```

However, the package should be imported as:

```python
import py_ste
```

### Support

Current support:

|                    | macOS Intel | macOS Apple Silicon | Windows 64bit | Windows 32bit | Windows Arm64 | manylinux<br/>musllinux x86_64 | Other Linux |
|--------------------|-----|-----|-----|------|-----|-----|-----|
| CPython 3.8        | ✅ | ✅  | ✅  | ✅  | Build from source | ✅ | Build from source |
| CPython 3.9        | ✅ | ✅  | ✅  | ✅  | Build from source | ✅ | Build from source |
| CPython 3.10       | ✅ | ✅  | ✅  | ✅  | Build from source | ✅ | Build from source |
| CPython 3.11       | ✅ | ✅  | ✅  | ✅  | Build from source | ✅ | Build from source |
| CPython 3.12       | ✅ | ✅  | ✅  | ✅  | Build from source | ✅ | Build from source |
| CPython 3.13       | ✅ | ✅  | ✅  | ✅  | Build from source | ✅ | Build from source |

Currently, the pre-built wheels only include the dynamic evolvers. For the faster static evolvers please build from source.

### Requirements

Requires:
- [NumPy](https://numpy.org/)

Note that [Suzuki-Trotter-Evolver](https://github.com/Christopher-K-Long/Suzuki-Trotter-Evolver) and [Eigen3](https://eigen.tuxfamily.org/) are packaged with PySTE and so do not need to be installed separately.

If on Linux and using a conda environment you may encounter an error
```
version `GLIBCXX_...' not found
```
to fix this you also need to execute:
```bash
conda install -c conda-forge libstdcxx-ng
```

#### Additional requirements for testing

- [toml](https://github.com/uiri/toml)
- [PyYAML](https://pyyaml.org/)
- [SciPy](https://scipy.org/)

#### Additional requirements for benchmarking

- [pyperf](https://github.com/psf/pyperf)
- [Matplotlib](https://matplotlib.org/)
- [pandas](https://pandas.pydata.org/)
- [QuTiP](https://qutip.org/)
- [Cython](https://cython.org/)
- [Setuptools](https://setuptools.pypa.io/)
- [filelock](https://github.com/tox-dev/filelock)

### Build from source

There are several flags that can be passed which will rebuild PySTE from source using various optimisations. The flags are:
- ``--config-setting="cmake.define.NCTRL_FIXED_SIZES=RANGE"``\
Defines the strategy used to compile evolvers with a fixed number of controls. The options are:
    - ``OFF``: There will only be evolvers with a dynamic number of controls.
    - ``SINGLE``: There will only be a single evolver with a fixed number of controls specified by ``--config-setting="cmake.define.NCTRL=..."``.
    - ``RANGE`` (**default option**): There will be evolvers with a fixed number of controls in the range $[1,$ ``MAX_NCTRL``$]$ where ``MAX_NCTRL`` can be set with ``--config-setting="cmake.define.MAX_NCTRL=..."``
    - ``POWER``: The evolvers with a fixed number of controls will have a number of controls given by powers in the range $[1,$ ``MAX_POWER_NCTRL``$]$ of the base ``BASE_NCTRL`` where ``MAX_POWER_NCTRL`` can be set with ``--config-setting="cmake.define.MAX_POWER_NCTRL=..."`` and ``BASE_NCTRL`` with ``--config-setting="cmake.define.BASE_NCTRL=..."``
- ``--config-setting="cmake.define.NCTRL=1"``\
The number of controls when using ``--config-setting="cmake.define.NCTRL_FIXED_SIZES=SINGLE"``. A positive integer, by default 1.
- ``--config-setting="cmake.define.MAX_NCTRL=14"``\
The maximum number of controls when using ``--config-setting="cmake.define.NCTRL_FIXED_SIZES=RANGE"``. A positive integer, by default 14.
- ``--config-setting="cmake.define.MAX_POWER_NCTRL=3"``\
The maximum power when using ``--config-setting="cmake.define.NCTRL_FIXED_SIZES=POWER"``. A positive integer, by default 3.
- ``--config-setting="cmake.define.BASE_NCTRL=2"``\
The base of the powers when using ``--config-setting="cmake.define.NCTRL_FIXED_SIZES=POWER"``. A positive integer, by default 2.
- ``--config-setting="cmake.define.DIM_FIXED_SIZES=RANGE"``\
Defines the strategy used to compile evolvers with a fixed vector space dimension. The options are:
    - ``OFF``: There will only be evolvers with a dynamic vector space dimension.
    - ``SINGLE``: There will only be a single evolver with a fixed vector space dimension specified by ``--config-setting="cmake.define.DIM=..."``.
    - ``RANGE`` (**default option**): There will be evolvers with a fixed vector space dimension in the range $[1,$ ``MAX_DIM``$]$ where ``MAX_DIM`` can be set with ``--config-setting="cmake.define.MAX_DIM=..."``
    - ``POWER``: The evolvers with a fixed vector space dimension will have a vector space dimension given by powers in the range $[1,$ ``MAX_POWER_DIM``$]$ of the base ``BASE_DIM`` where ``MAX_POWER_DIM`` can be set with ``--config-setting="cmake.define.MAX_POWER_DIM=..."`` and ``BASE_DIM`` with ``--config-setting="cmake.define.BASE_DIM=..."``
- ``--config-setting="cmake.define.DIM=2"``\
The vector space dimension when using ``--config-setting="cmake.define.DIM_FIXED_SIZES=SINGLE"``. A positive integer, by default 2.
- ``--config-setting="cmake.define.MAX_DIM=16"``\
The maximum vector space dimension when using ``--config-setting="cmake.define.DIM_FIXED_SIZES=RANGE"``. A positive integer, by default 16.
- ``--config-setting="cmake.define.MAX_POWER_DIM=4"``\
The maximum power when using ``--config-setting="cmake.define.DIM_FIXED_SIZES=POWER"``. A positive integer, by default 4.
- ``--config-setting="cmake.define.BASE_DIM=2"``\
The base of the powers when using ``--config-setting="cmake.define.DIM_FIXED_SIZES=POWER"``. A positive integer, by default 2.


For example,
```bash
pip install py-ste \
--config-setting="cmake.define.NCTRL_FIXED_SIZES=SINGLE" \
--config-setting="cmake.define.NCTRL=2" \
--config-setting="cmake.define.DIM_FIXED_SIZES=POWER" \
--config-setting="cmake.define.MAX_POWER_DIM=3" \
--verbose
```
will build PySTE from source and optimises evolvers at compile time with 2 control Hamiltonians acting on a vector space of dimensions 2, 4, and 8. Increasing the number of optimised evolvers increases the compile time. The ``--verbose`` flag allows the progress of the build to be seen. This is useful as the builds can often take a long time.

*Note building from source requires approximately 16GB of RAM.*

## Cloning the repository

PySTE uses git submodules and so should be cloned with the flag `--recurse-submodules` as follows:

```bash
git clone --recurse-submodules https://github.com/Christopher-K-Long/PySTE
```

Alternatively, you can clone the repository normally and then initialise the submodules as follows
```bash
git clone https://github.com/Christopher-K-Long/PySTE
git submodule update --init --recursive
```

## Documentation

Documentation including worked examples can be found at: [https://PySTE.readthedocs.io](https://PySTE.readthedocs.io)

## Source Code

Source code can be found at: [https://github.com/Christopher-K-Long/PySTE](https://github.com/Christopher-K-Long/PySTE)

## Version and Changes

The current version is [`1.0.1`](ChangeLog.md#release-101). Please see the [Change Log](ChangeLog.md) for more details. PySTE uses [semantic versioning](https://semver.org/).