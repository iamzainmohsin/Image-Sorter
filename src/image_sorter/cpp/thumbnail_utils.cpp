#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include "ThumbnailResizer.h"

namespace py = pybind11;

py::array_t<uint8_t> get_resized_thumbnail(const std::string& imagePath, int maxWidth, int maxHeight) {
    cv::Mat resized = ThumbnailResizer::resize(imagePath, maxWidth, maxHeight);

    // Allocate new buffer and copy data
    std::vector<uint8_t> buffer(resized.data, resized.data + resized.total() * resized.elemSize());

    return py::array_t<uint8_t>(
        { resized.rows, resized.cols, resized.channels() },
        { static_cast<ssize_t>(resized.step[0]),
          static_cast<ssize_t>(resized.step[1]),
          static_cast<ssize_t>(1) },
        buffer.data()
    );
}

PYBIND11_MODULE(thumbnail_utils, m) {
    m.def("get_resized_thumbnail", &get_resized_thumbnail, "Resize image and return as NumPy array");
}
