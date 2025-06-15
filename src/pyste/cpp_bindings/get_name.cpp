#include "single_evolver.hpp"

void get_name(std::string &name_string, int n_ctrl, int dim) {
    name_string += "_";
    if (n_ctrl == Eigen::Dynamic) {
        name_string += "Dynamic";
    } else {
        name_string += std::to_string(n_ctrl);
    }
    name_string += "_";
    if (dim == Eigen::Dynamic) {
        name_string += "Dynamic";
    } else {
        name_string += std::to_string(dim);
    }
};