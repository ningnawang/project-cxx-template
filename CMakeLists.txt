cmake_minimum_required(VERSION 3.16)
project(project_template)

# Default to Debug build if no build type is specified
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Debug CACHE STRING "Choose the build type" FORCE)
endif()

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

list(PREPEND CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake)

# Libigl
include(libigl)
igl_include(glfw)

# Polyscope
include(polyscope)

# nanoflann (header-only KD-tree)
include(nanoflann)

# pybind11 (Python bindings)
include(pybind11)

# ============================================
# C++ utilities (utility/cpp_utils)
#   - cpp_utils      : static library (knn, common headers, ...)
#   - utils_bindings : pybind11 Python module
# ============================================
add_subdirectory(utility/cpp_utils)

# ============================================
# Library: project_lib  (src/*.cpp + include/)
# Only built if there are source files in src/.
# ============================================
file(GLOB PROJECT_SRC_FILES
  ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
  ${CMAKE_CURRENT_SOURCE_DIR}/src/cpp/*.cpp
)

if(PROJECT_SRC_FILES)
  add_library(project_lib ${PROJECT_SRC_FILES})
  target_include_directories(project_lib PUBLIC
    ${CMAKE_CURRENT_SOURCE_DIR}/include
  )
  target_link_libraries(project_lib PUBLIC
    igl::glfw
    polyscope
    nanoflann::nanoflann
  )
endif()

# ============================================
# Executable: main (from main.cpp)
# ============================================
add_executable(main
  ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
)

target_include_directories(main PRIVATE
  ${CMAKE_CURRENT_SOURCE_DIR}/include
)

if(TARGET project_lib)
  target_link_libraries(main PRIVATE project_lib)
else()
  target_link_libraries(main PRIVATE igl::glfw polyscope nanoflann::nanoflann)
endif()

# main can also use the C++ utilities
target_link_libraries(main PRIVATE cpp_utils)

# ============================================
# Tests (Python / pytest, registered with CTest)
# ============================================
enable_testing()
add_subdirectory(tests)
