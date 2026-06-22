#include <pybind11/eigen.h>
#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

// forward declare all bindings
void knn_binding(py::module& m);

PYBIND11_MODULE(utils_bindings, m) {
  m.def("help", [&]() { printf("hi utils"); });

  // call all bindings declared above
  knn_binding(m);
}
