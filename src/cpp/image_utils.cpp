#include <pybind11/pybind11.h>
#include <pybind11/stl.h> 

namespace py = pybind11;

float add(float a, float b, float c) {
    return a + b + c;
}

PYBIND11_MODULE(image_utils, m) {
    m.doc() = "Image utility functions using C++ and pybind11";
    m.def("add", &add, "A function that adds two numbers");
}
