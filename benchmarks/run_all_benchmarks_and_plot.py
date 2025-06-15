import os
import subprocess

DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DIR, "results", "data")
PLOTS_DIR = os.path.join(DIR, "results", "plots")
PLOTTING_SCRIPT = f"python {os.path.join('plotting', 'plot_benchmark_propagate_or_initialisation.py')}"

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(PLOTS_DIR, exist_ok=True)

def benchmark_with_pyperf_and_plot(name):
    subprocess.check_call(f"cd {DIR}; python {name}.py -o {os.path.join(DATA_DIR, f'{name}.json')}", shell=True)
    subprocess.check_call(f"cd {DIR}; {PLOTTING_SCRIPT} {os.path.join(DATA_DIR, f'{name}.json')}", shell=True)
    os.rename(os.path.join(DATA_DIR, f'{name}.png'), os.path.join(PLOTS_DIR, f'{name}.png'))

benchmark_with_pyperf_and_plot("benchmark_propagate")
benchmark_with_pyperf_and_plot("benchmark_propagate_sparse_Hamiltonian")
benchmark_with_pyperf_and_plot("benchmark_initialisation")
benchmark_with_pyperf_and_plot("benchmark_initialisation_sparse_Hamiltonian")

subprocess.check_call(f"cd {DIR}; python benchmark_against_qutip.py -o {os.path.join(DATA_DIR, 'benchmark_against_qutip.csv')}", shell=True)
subprocess.check_call(f"cd {DIR}; python {os.path.join('plotting', 'plot_benchmark_againt_qutip.py')} {os.path.join(DATA_DIR, 'benchmark_against_qutip.csv')}", shell=True)
os.rename(os.path.join(DATA_DIR, 'benchmark_against_qutip.png'), os.path.join(PLOTS_DIR, 'benchmark_against_qutip.png'))