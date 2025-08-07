#include "include/thumbnailResizer.h"
#include <opencv2/opencv.hpp>
#include <opencv2/imgcodecs.hpp>
using namespace std;

vector<uint8_t> ImageProcessing::resizeAndEncodeWebp(const string& imagePath, int width, int height){

    //LoadingImage:
    cv::Mat image = cv::imread(imagePath, cv::IMREAD_COLOR);
    if(image.empty()){
        throw runtime_error("Failed to load image " + imagePath);
    }

    //ResizingImage:
    cv:: Mat resized;
    cv::resize(image, resized, cv::Size(width, height), 0, 0, cv::INTER_AREA);

    //ConvertingToWebp:
    vector<uint8_t> buffer;
    vector<int> compression_prams = {cv::IMWRITE_WEBP_QUALITY, 90};

    if(!cv::imencode(".webp", resized, buffer, compression_prams)){
        size_t lastDot = imagePath.find_last_of(".");
        string originalExtension = imagePath.substr(lastDot);
        
        if (!cv::imencode(originalExtension, resized, buffer)) {
        throw runtime_error("Failed to encode image to Webp and also failed to encode to original format: " + imagePath);
        }
    }

    return buffer;
}