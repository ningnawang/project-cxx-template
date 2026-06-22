#pragma once

#include <Eigen/Core>
#include <array>
#include <cassert>
#include <cstddef>
#include <cstdlib>
#include <vector>

// And this is the "dataset to kd-tree" Adaptor class:
template <typename T>
struct PointAdaptor {
  struct Point {
    T x, y, z;
  };
  std::vector<Point> pts;

  inline void init_points(const Eigen::MatrixXd& samples) {  //(N,dim)
    pts.resize(samples.rows());
    for (int i = 0; i < samples.rows(); ++i) {
      pts[i].x = static_cast<T>(samples(i, 0));
      pts[i].y = static_cast<T>(samples(i, 1));
      pts[i].z = static_cast<T>(samples(i, 2));
    }
  }

  inline void clear() { pts.clear(); }

  // Must return the number of data points
  inline size_t kdtree_get_point_count() const { return pts.size(); }

  // Returns the dim'th component of the idx'th point in the class:
  // Since this is inlined and the "dim" argument is typically an immediate
  // value, the "if/else's" are actually solved at compile time.
  inline T kdtree_get_pt(const size_t idx, const size_t dim) const {
    return dim == 0 ? pts[idx].x : (dim == 1 ? pts[idx].y : pts[idx].z);
  }

  // Optional bounding-box computation: return false to default to a standard
  // bbox computation loop.
  //   Return true if the BBOX was already computed by the class and returned
  //   in "bb" so it can be avoided to redo it again. Look at bb.size() to
  //   find out the expected dimensionality (e.g. 2 or 3 for point clouds)
  template <class BBOX>
  bool kdtree_get_bbox(BBOX& /* bb */) const {
    return false;
  }

  auto const* elem_ptr(const unsigned idx) const { return &pts[idx].x; }
};

//////////////////////////////////////////////////////////////////////
// unit test: test_knn_search.py
void knn_search(const Eigen::MatrixXd& points, const int num_neighbors,
                std::vector<std::vector<uint32_t>>& rets_index,
                std::vector<std::vector<double>>& rets_dist_sqr, bool is_debug);

void knn_search_for_query(const Eigen::MatrixXd& queries,
                          const Eigen::MatrixXd& points,
                          const int num_neighbors,
                          std::vector<std::vector<uint32_t>>& rets_index,
                          std::vector<std::vector<double>>& rets_dist_sqr,
                          bool is_debug);
