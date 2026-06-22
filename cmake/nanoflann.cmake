if(TARGET nanoflann::nanoflann)
    return()
endif()

include(FetchContent)
FetchContent_Declare(
    nanoflann
    GIT_REPOSITORY https://github.com/jlblancoc/nanoflann.git
    GIT_TAG v1.5.5
)
# nanoflann is header-only; skip building its examples/tests/benchmarks.
set(NANOFLANN_BUILD_EXAMPLES OFF CACHE BOOL "" FORCE)
set(NANOFLANN_BUILD_TESTS OFF CACHE BOOL "" FORCE)
set(NANOFLANN_BUILD_BENCHMARKS OFF CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(nanoflann)
