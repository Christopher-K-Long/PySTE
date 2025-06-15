import os
import subprocess

from .unique_names import get_unique_name

DIR = os.path.dirname(os.path.abspath(__file__))

class VEnv():
    def __init__(self, path):
        self.path = path
    def __enter__(self):
        subprocess.run(f"python -m venv {self.path}", shell=True)
    def __exit__(self, exception_type, exception_value, exception_traceback):
        subprocess.run(f"rm -rf {self.path}", shell=True)

def isolated_build_and_test(name, options, allowed_specs):
    path = os.path.join(DIR, "__envs__", "."+name)
    python = os.path.join(path, "bin", "python")
    install_path = os.path.join(DIR, '..')
    test_path = os.path.join(DIR, "fixed_size_compilation_check.py")
    options = [f'--config-setting="{option}"' for option in options]
    with VEnv(path):
        subprocess.run(f"{python} -m pip install --upgrade pip", shell=True)
        subprocess.check_output(f"{python} -m pip install {install_path} --verbose {' '.join(options)}", shell=True)
        subprocess.check_output(f"{python} {test_path} {' '.join(allowed_specs)}", shell=True)

def test_nctrl_off_dim_off():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=OFF',
                             'cmake.define.DIM_FIXED_SIZES=OFF'],
                            [])

def test_nctrl_range_dim_off():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=RANGE',
                             'cmake.define.MAX_NCTRL=3',
                             'cmake.define.DIM_FIXED_SIZES=OFF'],
                            ["1_Dynamic",
                             "2_Dynamic",
                             "3_Dynamic"])

def test_nctrl_off_dim_range():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=OFF',
                             'cmake.define.DIM_FIXED_SIZES=RANGE',
                             'cmake.define.MAX_DIM=3'],
                            ["Dynamic_1",
                             "Dynamic_2",
                             "Dynamic_3"])

def test_nctrl_range_dim_range():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=RANGE',
                             'cmake.define.MAX_NCTRL=2',
                             'cmake.define.DIM_FIXED_SIZES=RANGE',
                             'cmake.define.MAX_DIM=3'],
                            ["Dynamic_1",
                             "Dynamic_2",
                             "Dynamic_3",
                             "1_Dynamic",
                             "1_1",
                             "1_2",
                             "1_3",
                             "2_Dynamic",
                             "2_1",
                             "2_2",
                             "2_3"])

def test_nctrl_off_dim_single():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=OFF',
                             'cmake.define.DIM_FIXED_SIZES=SINGLE',
                             'cmake.define.DIM=10'],
                            ["Dynamic_10"])

def test_nctrl_single_dim_off():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=SINGLE',
                             'cmake.define.NCTRL=10',
                             'cmake.define.DIM_FIXED_SIZES=OFF'],
                            ["10_Dynamic"])

def test_nctrl_range_dim_single():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=RANGE',
                             'cmake.define.MAX_NCTRL=2',
                             "cmake.define.DIM_FIXED_SIZES=SINGLE",
                             'cmake.define.DIM=10'],
                            ["Dynamic_10",
                             "1_Dynamic",
                             "1_10",
                             "2_Dynamic",
                             "2_10"])

def test_nctrl_single_dim_range():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=SINGLE',
                             'cmake.define.NCTRL=10',
                             'cmake.define.DIM_FIXED_SIZES=RANGE',
                             'cmake.define.MAX_DIM=2'],
                            ["10_Dynamic",
                             "Dynamic_1",
                             "10_1",
                             "Dynamic_2",
                             "10_2"])

def testt_nctrl_single_dim_single():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=SINGLE',
                             'cmake.define.NCTRL=10',
                             'cmake.define.DIM_FIXED_SIZES=SINGLE',
                             'cmake.define.DIM=5'],
                            ["10_Dynamic",
                             "Dynamic_5",
                             "10_5"])


def test_nctrl_power_dim_single():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=POWER',
                             'cmake.define.MAX_POWER_NCTRL=2',
                             'cmake.define.DIM_FIXED_SIZES=SINGLE',
                             'cmake.define.DIM=10'],
                            ["Dynamic_10",
                             "2_Dynamic",
                             "2_10",
                             "4_Dynamic",
                             "4_10"])

def test_nctrl_single_dim_power():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=SINGLE',
                             'cmake.define.NCTRL=10',
                             'cmake.define.DIM_FIXED_SIZES=POWER',
                             'cmake.define.MAX_POWER_DIM=2'],
                            ["10_Dynamic",
                             "Dynamic_2",
                             "10_2",
                             "Dynamic_4",
                             "10_4"])

def test_nctrl_power_dim_off():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=POWER',
                             'cmake.define.MAX_POWER_NCTRL=2',
                             'cmake.define.DIM_FIXED_SIZES=OFF'],
                            ["2_Dynamic",
                             "4_Dynamic"])

def test_nctrl_off_dim_power():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=OFF',
                             'cmake.define.DIM_FIXED_SIZES=POWER',
                             'cmake.define.MAX_POWER_DIM=2'],
                            ["Dynamic_2",
                             "Dynamic_4"])

def test_nctrl_power_dim_power():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=POWER',
                             'cmake.define.MAX_POWER_NCTRL=2',
                             'cmake.define.DIM_FIXED_SIZES=POWER',
                             'cmake.define.MAX_POWER_DIM=3'],
                            ["Dynamic_2",
                             "Dynamic_4",
                             "Dynamic_8",
                             "2_Dynamic",
                             "2_2",
                             "2_4",
                             "2_8",
                             "4_Dynamic",
                             "4_2",
                             "4_4",
                             "4_8"])

def test_nctrl_range_dim_power():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=RANGE',
                             'cmake.define.MAX_NCTRL=2',
                             'cmake.define.DIM_FIXED_SIZES=POWER',
                             'cmake.define.MAX_POWER_DIM=3'],
                            ["Dynamic_2",
                             "Dynamic_4",
                             "Dynamic_8",
                             "1_Dynamic",
                             "1_2",
                             "1_4",
                             "1_8",
                             "2_Dynamic",
                             "2_2",
                             "2_4",
                             "2_8"])

def test_nctrl_power_dim_range():
    isolated_build_and_test(get_unique_name(),
                            ['cmake.define.NCTRL_FIXED_SIZES=POWER',
                             'cmake.define.MAX_POWER_NCTRL=2',
                             'cmake.define.DIM_FIXED_SIZES=RANGE',
                             'cmake.define.MAX_DIM=3'],
                            ["Dynamic_1",
                             "Dynamic_2",
                             "Dynamic_3",
                             "2_Dynamic",
                             "2_1",
                             "2_2",
                             "2_3",
                             "4_Dynamic",
                             "4_1",
                             "4_2",
                             "4_3"])