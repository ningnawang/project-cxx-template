# C++ Project Template

A starter C++ project template using [libigl](http://libigl.github.io/libigl/)
and [Polyscope](https://polyscope.run/), wired up with CMake. Copy or fork this
project as a starting point for a new personal project.

## Structure

```
.
├── cmake/            # CMake dependency modules (libigl.cmake, polyscope.cmake)
├── external/         # Third-party submodules / vendored code
├── include/          # Public headers
├── render_utility/   # Rendering / visualization helpers
├── results/          # Output artifacts (kept empty)
├── scripts/          # Helper scripts
├── src/              # Library source files (src/*.cpp or src/cpp/*.cpp)
├── tests/            # Tests
├── utility/          # Miscellaneous utilities
├── CMakeLists.txt
└── main.cpp          # Entry point: prints "Hello, world!" and opens Polyscope
```

## Compile

Compile this project using the standard CMake routine:

    mkdir build
    cd build
    cmake ..
    make

This downloads and builds the dependencies (libigl and Polyscope) and creates a
`main` binary. The first configure may take a few minutes while dependencies are
fetched.

## Run

From within the `build` directory:

    ./main

This prints `Hello, world!` to the terminal and then launches a Polyscope window
displaying a small point cloud.

## Dependencies

Dependencies are downloaded automatically via
[CMake FetchContent](https://cmake.org/cmake/help/latest/module/FetchContent.html),
so no manual setup is required:

- [libigl](http://libigl.github.io/libigl/) (with the `glfw` module)
- [Polyscope](https://polyscope.run/)
- their transitive dependencies (Eigen, OpenGL, glad, GLFW, ImGui)

### Adding your own code

Drop `.cpp` files into `src/` (or `src/cpp/`) and headers into `include/`.
The build automatically compiles them into a `project_lib` library that `main`
links against.
