// ThumbnailResizer.h
#ifndef THUMBNAIL_RESIZER_H
#define THUMBNAIL_RESIZER_H

#include <opencv2/opencv.hpp>
#include <string>

class ThumbnailResizer {
public:
    static cv::Mat resize(const std::string& imagePath, int maxWidth, int maxHeight);
};

#endif
