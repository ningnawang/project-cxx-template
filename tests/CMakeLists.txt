# Register the Python test-suite with CTest so it runs via `ctest`.
# The tests import the `python_utils` package and `utils_bindings` module,
# both reachable from the repo root (which is added to sys.path in context.py /
# via PYTHONPATH below).

find_package(Python3 COMPONENTS Interpreter REQUIRED)

add_test(
  NAME python_tests
  COMMAND ${Python3_EXECUTABLE} -m pytest -v ${CMAKE_CURRENT_SOURCE_DIR}
  WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}
)

# Make the repo root importable so `import python_utils` / `import utils_bindings`
# resolve (utils_bindings is built into utility/python_utils/).
set_tests_properties(python_tests PROPERTIES
  ENVIRONMENT "PYTHONPATH=${CMAKE_SOURCE_DIR}:${CMAKE_SOURCE_DIR}/utility"
)
