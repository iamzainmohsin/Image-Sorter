#ifndef IMAGEPROCESSOR_H
#define IMAGEPROCESSOR_H

#include <opencv2/opencv.hpp>
#include <string>

class ImageProcessor {
private:
    cv::Mat image;
    std::string imagePath;

public:
    bool loadImage(const std::string& path);
    bool resizeImage(int maxWidth, int maxHeight);
    bool saveImage(const std::string& outputPath);
    cv::Mat getImageCopy() const;
    cv::Mat getThumbnailMat(const std::string& imagePath, int width, int height);
};

#endif 
