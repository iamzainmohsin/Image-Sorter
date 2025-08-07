#ifndef THUMBNAIL_RESIZER_H
#define THUMBNAIL_RESIZER_H

#include <string>
#include <vector>

namespace ImageProcessing {
    std::vector<u_int8_t> resizeAndEncodeWebp(const std::string& imagePath, int width, int height);
}

#endif 
