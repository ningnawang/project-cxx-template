// knn_binding.cpp
#include <pybind11/eigen.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "knn.h"

namespace py = pybind11;

void knn_binding(py::module& m) {
  m.def(
      "knn_search",
      [](const Eigen::MatrixXd& points, int k, bool is_debug) {
        std::vector<std::vector<uint32_t>> nn_idx;
        std::vector<std::vector<double>> nn_dist_sqr;
        knn_search(points, k, nn_idx, nn_dist_sqr, is_debug);
        return py::make_tuple(nn_idx, nn_dist_sqr);
      },
      py::arg("points"), py::arg("k"), py::arg("is_debug") = false,
      "Return indices and squared distances of k nearest neighbors for each "
      "row of points.");
}
