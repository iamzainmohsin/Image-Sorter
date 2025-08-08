#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "ThumbnailResizer.h"

namespace py = pybind11;

py::array_t<unsigned char> resize_thumbnail(const std::string &image_path, int width, int height) {
    cv::Mat img = cv::imread(image_path, cv::IMREAD_COLOR);
    if (img.empty()) {
        throw std::runtime_error("Failed to load image: " + image_path);
    }

    cv::Mat resized;
    cv::resize(img, resized, cv::Size(width, height));

    // Ensure continuous memory layout for NumPy
    if (!resized.isContinuous()) {
        resized = resized.clone();
    }

    return py::array_t<unsigned char>(
        {resized.rows, resized.cols, resized.channels()},
        {resized.step[0], resized.step[1], sizeof(unsigned char)},
        resized.data
    );
}


PYBIND11_MODULE(thumbnail_utils, m) {
    m.def("get_resized_thumbnail", &resize_thumbnail, "Resize image and return as NumPy array");
}
