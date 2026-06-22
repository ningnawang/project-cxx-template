cmake_minimum_required(VERSION 3.16)

# include(pybind11) # already included in the parent CMakeLists.txt
add_library(cpp_utils
	STATIC
	# Headers
		"common.h"
		"common_cxx.h"
		"knn.h"
	# Source
		"knn.cpp"
)
# Consumers should be able to #include "knn.h", "common.h", etc.
target_include_directories(cpp_utils PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}
)

target_link_libraries(cpp_utils PUBLIC igl::core Eigen3::Eigen nanoflann)
set_property(TARGET cpp_utils PROPERTY INTERPROCEDURAL_OPTIMIZATION TRUE)

# ============================================
# Python bindings module: utils_bindings
# (bindings_core_utils.cpp registers all sub-bindings, e.g. knn_binding.cpp)
# ============================================
if(TARGET pybind11::module)
  pybind11_add_module(utils_bindings
    bindings_core_utils.cpp
    knn_binding.cpp
  )
  target_link_libraries(utils_bindings PRIVATE cpp_utils)

  # Place the compiled module next to the Python package so it can be imported
  # as `utils_bindings` once utility/ (repo root) is on sys.path.
  set_target_properties(utils_bindings PROPERTIES
    LIBRARY_OUTPUT_DIRECTORY ${CMAKE_SOURCE_DIR}/utility/python_utils
  )
endif()
