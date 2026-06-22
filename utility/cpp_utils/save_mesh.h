#pragma once

#include <igl/writeOBJ.h>

#include <Eigen/Core>
#include <Eigen/Eigen>
#include <iostream>
#include <stdexcept>

inline void save_mesh_obj(const std::string& filename, const Eigen::MatrixXd& V,
                          const Eigen::MatrixXi& F) {
  if (V.cols() != 3) {
    throw std::runtime_error("save_mesh: V must have shape (N, 3)");
  }
  // Able to save quads
  // if (F.cols() < 3) {
  //   throw std::runtime_error("save_mesh: F must have at least 3 columns");
  // }

  if (!igl::writeOBJ(filename, V, F)) {
    throw std::runtime_error("save_mesh: failed to write obj file: " +
                             filename);
  }

  std::cout << "Mesh saved to " << filename << std::endl;
}