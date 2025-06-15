#include "evolvers.hpp"

void get_name(std::string &name_string, int n_ctrl, int dim);


template <int n_ctrl, int dim, typename Matrix>
void generate_evolver_class(py::module_ m,
                            std::string string_name,
                            py::class_<ste::UnitaryEvolver<n_ctrl, dim, Matrix>> parent) {
    get_name(string_name, n_ctrl, dim);
    const char* name = string_name.c_str();
    py::class_<ste::UnitaryEvolver<n_ctrl, dim, Matrix>>
        sparse_evolver(m, name, parent);
    add_attributes<n_ctrl, dim, Matrix>(sparse_evolver);
};