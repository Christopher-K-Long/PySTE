# Multithreading

Currently a few of PySTE's functions support multithreading. By default multithreading is turned off. This is because it is typically more efficient to parallelise a program at the highest level—for example, a loop over [``propagate()``](../reference/_autosummary/py_ste.evolvers.DenseUnitaryEvolver.rst#py_ste.evolvers.DenseUnitaryEvolver.propagate). However, if there will be times when PySTE function calls cannot be parallelised. In this case it makes sense to turn on multithreading. This can be done using [``set_threads()``](../reference/_autosummary/py_ste.set_threads.rst). For example
```python
import py_ste
py_ste.set_threads(2)
```
will allow PySTE to parallelise using 2 threads. Multithreading can be turned off again using:
```python
py_ste.set_threads(1)
```
If you wish to check how many threads are currently set to be used you can call [``get_threads()``](../reference/_autosummary/py_ste.get_threads.rst).

The functions that currently support multithreading are:
- [``DenseUnitaryEvolver()``](../reference/_autosummary/py_ste.evolvers.DenseUnitaryEvolver.rst#py_ste.evolvers.DenseUnitaryEvolver.__init__): Matrix multiplications during initialisation are parallelised.
- [``propagate_collection()``](../reference/_autosummary/py_ste.evolvers.DenseUnitaryEvolver.rst#py_ste.evolvers.DenseUnitaryEvolver.propagate_collection): Each state vector in the collection is evolved in parallel.
- [``evolved_expectation_value_all()``](../reference/_autosummary/py_ste.evolvers.DenseUnitaryEvolver.rst#py_ste.evolvers.DenseUnitaryEvolver.evolved_expectation_value_all): The expectation values for each time step is computed in parallel.


````{warning}
The number of threads should be less than or equal to the number of
physical cores and you should not attempt to make use of hyperthreading
by using twice the number of physical cores. PySTE uses [Eigen3](https://eigen.tuxfamily.org/) for
multithreading which provides the following warning:
```{admonition} Quote
On most OS it is very important to limit the number of threads to the
number of physical cores, otherwise significant slowdowns are expected
```
For more details see [https://eigen.tuxfamily.org/dox/TopicMultiThreading.html](https://eigen.tuxfamily.org/dox/TopicMultiThreading.html).
````

---
[Previous](switching_function.md) | [Next](examples.md)