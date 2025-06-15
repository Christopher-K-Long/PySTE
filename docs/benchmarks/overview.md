# Benchmarks

Here we benchmark the runtime of PySTE against the vector space dimension for both [evolver initialisation](initialisation.md) and [state propagation](propagation.md). Additionally, we compare the runtime required by PySTE with [QuTiP](https://qutip.org) to solve the Schrödinger with a given infidelity: [PySTE *vs.* QuTiP](pyste_vs_qutip.md)

These benchmarks were performed with the default build options for PySTE. The hardware specifications were:

Redacted output of ``lscpu``:
```
Architecture:        x86_64
CPU op-mode(s):      32-bit, 64-bit
Byte Order:          Little Endian
Address sizes:       46 bits physical, 48 bits virtual
CPU(s):              28
On-line CPU(s) list: 0-27
Thread(s) per core:  2
Core(s) per socket:  14
Socket(s):           1
NUMA node(s):        1
Vendor ID:           GenuineIntel
CPU family:          6
Model:               85
Model name:          Intel(R) Core(TM) i9-10940X CPU @ 3.30GHz
Stepping:            7
CPU MHz:             4010.885
CPU max MHz:         4800.0000
CPU min MHz:         1200.0000
BogoMIPS:            6599.98
Virtualisation:      VT-x
L1d cache:           448 KiB
L1i cache:           448 KiB
L2 cache:            14 MiB
L3 cache:            19.3 MiB
NUMA node0 CPU(s):   0-27
```

All benchmarks were done without multithreading.