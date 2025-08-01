cmake_minimum_required(VERSION 3.14)
project(image_utils)

set(CMAKE_CXX_STANDARD 17)

# Handle Python detection properly
cmake_policy(SET CMP0148 NEW)
set(PYBIND11_FINDPYTHON ON)

cmake_policy(SET CMP0148 NEW)
set(PYBIND11_FINDPYTHON ON)

# Find pybind11
find_package(pybind11 REQUIRED)

# Build the Python module
pybind11_add_module(image_utils image_utils.cpp)
