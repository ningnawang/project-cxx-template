#include "knn.h"

#include <igl/parallel_for.h>

#include <algorithm>
#include <array>
#include <cstddef>
#include <cstdint>
#include <vector>

#include "nanoflann.hpp"

void knn_search(const Eigen::MatrixXd& points, const int num_neighbors,
                std::vector<std::vector<uint32_t>>& rets_index,
                std::vector<std::vector<double>>& rets_dist_sqr,
                bool is_debug) {
  (void)is_debug;
  using Adaptor = PointAdaptor<double>;
  using KDTree = nanoflann::KDTreeSingleIndexAdaptor<
      nanoflann::L2_Simple_Adaptor<double, Adaptor>, Adaptor, 3>;

  const int N = static_cast<int>(points.rows());
  if (N == 0 || num_neighbors <= 0) {
    rets_index.clear();
    rets_dist_sqr.clear();
    return;
  }

  Adaptor adapt;
  adapt.init_points(points);
  KDTree index(3, adapt, {10});
  index.buildIndex();

  const int k_excl = std::min(num_neighbors, std::max(0, N - 1));
  const int k_query = std::min(N, k_excl + 1);

  rets_index.assign(N, std::vector<uint32_t>());
  rets_dist_sqr.assign(N, std::vector<double>());

  auto run_thread = [&](int i) {
    std::array<double, 3> q{points(i, 0), points(i, 1), points(i, 2)};
    std::vector<uint32_t> tmp_index(k_query);
    std::vector<double> tmp_dist_sqr(k_query);

    size_t num_found = index.knnSearch(q.data(), k_query, tmp_index.data(),
                                       tmp_dist_sqr.data());

    auto& idx_vec = rets_index[i];
    auto& d2_vec = rets_dist_sqr[i];
    idx_vec.reserve(k_excl);
    d2_vec.reserve(k_excl);

    // filter out itself
    for (size_t t = 0; t < num_found; ++t) {
      uint32_t j = static_cast<uint32_t>(tmp_index[t]);
      if (j == static_cast<uint32_t>(i)) continue;
      idx_vec.push_back(j);
      d2_vec.push_back(tmp_dist_sqr[t]);
      if (static_cast<int>(idx_vec.size()) >= k_excl) break;
    }
  };
  igl::parallel_for(N, run_thread);
}

void knn_search_for_query(const Eigen::MatrixXd& queries,
                          const Eigen::MatrixXd& points,
                          const int num_neighbors,
                          std::vector<std::vector<uint32_t>>& rets_index,
                          std::vector<std::vector<double>>& rets_dist_sqr,
                          bool is_debug) {
  (void)is_debug;
  using Adaptor = PointAdaptor<double>;
  using KDTree = nanoflann::KDTreeSingleIndexAdaptor<
      nanoflann::L2_Simple_Adaptor<double, Adaptor>, Adaptor, 3>;

  const int num_points = static_cast<int>(points.rows());
  const int num_queries = static_cast<int>(queries.rows());
  if (num_points == 0 || num_neighbors <= 0 || num_queries == 0) {
    rets_index.clear();
    rets_dist_sqr.clear();
    return;
  }

  Adaptor adapt;
  adapt.init_points(points);
  KDTree index(3, adapt, {10});
  index.buildIndex();

  const int k_query = std::min(num_neighbors, num_points);

  rets_index.assign(num_queries, std::vector<uint32_t>());
  rets_dist_sqr.assign(num_queries, std::vector<double>());

  auto run_thread = [&](int i) {
    std::array<double, 3> q{queries(i, 0), queries(i, 1), queries(i, 2)};
    std::vector<uint32_t> tmp_index(k_query);
    std::vector<double> tmp_dist_sqr(k_query);

    size_t num_found = index.knnSearch(q.data(), k_query, tmp_index.data(),
                                       tmp_dist_sqr.data());

    auto& idx_vec = rets_index[i];
    auto& d2_vec = rets_dist_sqr[i];
    idx_vec.resize(num_found);
    d2_vec.resize(num_found);
    std::copy_n(tmp_index.data(), num_found, idx_vec.data());
    std::copy_n(tmp_dist_sqr.data(), num_found, d2_vec.data());
  };
  igl::parallel_for(num_queries, run_thread);
}
