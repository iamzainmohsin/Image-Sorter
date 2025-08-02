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

bool ImageProcessor::resizeImage(int maxWidth, int maxHeight) {
    if (image.empty()) {
        cerr << "No image loaded to resize" << endl;
        return false;
    }

    int originalWidth = image.cols;
    int originalHeight = image.rows;

    if (originalWidth <= maxWidth && originalHeight <= maxHeight){
        return true;
    }
    
    double widthScale = static_cast<double>(maxWidth) / originalWidth;
    double heightScale = static_cast<double>(maxHeight) / originalHeight;
    double scaleFactor = std::min(widthScale, heightScale);

    int newWidth = static_cast<int>(originalWidth * scaleFactor);
    int newHeight = static_cast<int>(originalHeight * scaleFactor);

    cv::resize(image, image, cv::Size(newWidth, newHeight), 0, 0, cv::INTER_AREA);
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
