#include <pybind11/numpy.h>
#include <pybind11/stl.h>
#include <opencv2/opencv.hpp>
#include "ImageProcessor.h"

namespace py = pybind11;

PYBIND11_MODULE(image_utils, m){
    py::class_<ImageProcessor>(m, "ImageProcessor")
        .def(py::init<>())
        .def("load_image", &ImageProcessor::loadImage)
        .def("resize_image", &ImageProcessor::resizeImage)
        .def("save_image", &ImageProcessor::saveImage)
        .def("get_image_copy", [](const ImageProcessor& proc){
            cv::Mat mat = proc.getImageCopy();

        return py::array_t<uint8_t>(
                { mat.rows, mat.cols, mat.channels() },
                { static_cast<ssize_t>(mat.step[0]),
                  static_cast<ssize_t>(mat.step[1]),
                  static_cast<ssize_t>(1) },
                mat.data,
                py::capsule(mat.data, [](void*) {})  // no deletion, OpenCV owns data
            );
        });
}