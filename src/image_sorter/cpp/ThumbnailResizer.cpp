#include "ThumbnailResizer.h"
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
using namespace std;

cv::Mat ThumbnailResizer::resize(const string& imagePath, int maxWidth, int maxHeight){
    cv::Mat image = cv::imread(imagePath, cv::IMREAD_COLOR);
    if(image.empty()){
         throw runtime_error("Failed to load image: " + imagePath);
    } 

    int originalWidth = image.cols;
    int originalHeight = image.rows;

    double widthScale = static_cast<double>(maxWidth) / originalWidth;
    double heightScale = static_cast<double>(maxHeight) / originalHeight;
    double scale = std::min(widthScale, heightScale);

    int newWidth = static_cast<int>(originalWidth * scale);
    int newHeight = static_cast<int>(originalHeight * scale);

    cv::Mat resized;
    cv::resize(image, resized, cv::Size(newWidth, newHeight), 0, 0, cv::INTER_AREA);

    return resized;
}
