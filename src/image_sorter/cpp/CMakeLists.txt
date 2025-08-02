cmake_minimum_required(VERSION 3.14)
project(image_utils)

set(CMAKE_CXX_STANDARD 17)

# Find pybind11 and OpenCV
find_package(pybind11 REQUIRED)
find_package(OpenCV REQUIRED)

include_directories(include)

pybind11_add_module(image_utils
    image_utils.cpp
    ImageProcessor.cpp
)

target_link_libraries(image_utils PRIVATE ${OpenCV_LIBS})