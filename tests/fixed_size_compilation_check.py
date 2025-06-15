from argparse import ArgumentParser

from pyste import evolvers

parser = ArgumentParser()
parser.add_argument('allowed_specs',
                    nargs='*',
                    help="A list of the nctrl and dim pairs that should have been compiled as fixed sizes. Each entry should be specified as: nctrl_dim.")
allowed_specs = parser.parse_args().allowed_specs
found = [0]*len(allowed_specs)

for key, item in evolvers.__dict__.items():
    if "UnitaryEvolver_" in key:
        spec = key.split("UnitaryEvolver_")[1]
        assert spec in allowed_specs, f"{[spec]} not in allowed_specs"
        found[allowed_specs.index(spec)] += 1
        n_ctrl, dim = spec.split("_")
        if n_ctrl == "Dynamic":
            n_ctrl = 1
        if dim == "Dynamic":
            dim = 1
        n_ctrl = int(n_ctrl)
        dim = int(dim)
        h0 = [[1]*dim]*dim
        hs = [[1]*dim]*dim*n_ctrl
        item(h0, hs)
assert all([f == 2 for f in found])