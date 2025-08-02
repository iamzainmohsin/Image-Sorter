#include "ImageProcessor.h"
#include <iostream>

using namespace std;

bool ImageProcessor::loadImage(const string& path) {
    cv::Mat loaded = cv::imread(path, cv::IMREAD_COLOR);
    if (loaded.empty()) {
        cerr << "Failed to load image from " << path << endl;
        return false;
    }
    image = loaded;
    imagePath = path;
    return true;
}

bool ImageProcessor::resizeImage(double scaleFactor) {
    if (image.empty()) {
        cerr << "No image loaded to resize" << endl;
        return false;
    }

    int newWidth = static_cast<int>(image.cols * scaleFactor);
    int newHeight = static_cast<int>(image.rows * scaleFactor);
    cv::Size newSize(newWidth, newHeight);

    cv::Mat resized;
    cv::resize(image, resized, newSize);

    image = resized;
    return true;
}

bool ImageProcessor::saveImage(const string& outputPath) {
    if (image.empty()) {
        cerr << "No image to save." << endl;
        return false;
    }

    bool success = cv::imwrite(outputPath, image);
    if (!success) {
        cerr << "Failed to save image to " << outputPath << endl;
        return false;
    }

    return true;
}

cv::Mat ImageProcessor::getImageCopy() const {
    return image.clone();
}
