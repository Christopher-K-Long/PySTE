# Partialy written by claude-opus-5 and veified by author

import os

def available_threads():
    """
    The number of threads OpenMP will make available to Eigen.

    ``omp_get_max_threads()`` defaults to the number of processors this process
    may run on, but ``OMP_NUM_THREADS`` overrides it.
    """
    omp_num_threads = os.environ.get("OMP_NUM_THREADS")
    if omp_num_threads:
        # OMP_NUM_THREADS may be a comma separated list, one entry per nesting
        #   level, in which case only the outermost level is relevant here.
        try:
            return int(omp_num_threads.split(",")[0])
        except ValueError:
            pass
    try:
        # Respects cgroup and taskset limits, unlike os.cpu_count().
        return len(os.sched_getaffinity(0))
    except AttributeError:
        # sched_getaffinity() is unavailable on macOS and Windows.
        return os.cpu_count() or 1


def test_get_threads_initial():
    import py_ste
    assert py_ste.get_threads() == 1

def test_get_and_set_threads():
    import py_ste
    original = py_ste.get_threads()
    try:
        assert py_ste.get_threads() == 1
        py_ste.set_threads(2)
        assert py_ste.get_threads() == 2
        py_ste.set_threads(1)
        assert py_ste.get_threads() == 1
    finally:
        py_ste.set_threads(original)

def test_openmp_enabled():
    import py_ste
    if available_threads() <= 1:
        # Only one thread is available, so OpenMP being enabled is
        #   indistinguishable from it being disabled.
        return
    original = py_ste.get_threads()
    try:
        # Eigen maps 0 onto omp_get_max_threads(). Without OpenMP,
        #   set_threads() discards its argument and get_threads() is hardcoded
        #   to return 1, so anything above 1 proves the extension was compiled
        #   with OpenMP enabled.
        py_ste.set_threads(0)
        assert py_ste.get_threads() > 1
    finally:
        py_ste.set_threads(original)