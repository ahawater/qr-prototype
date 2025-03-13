#include <pybind11/embed.h>
#include <pybind11/numpy.h>
#include <opencv2/opencv.hpp>

namespace py = pybind11;

void processImageWithPython(const cv::Mat& inputImage) {
    py::scoped_interpreter guard{};  // Start Python interpreter

    // Convert cv::Mat to numpy array
    std::cout << "started python interpreter" << std::endl;

    py::module_ np = py::module_::import("numpy");

    std::cout << "imported numpy" << std::endl;

    py::module_ cv2 = py::module_::import("cv2");

    std::cout << "imported cv2" << std::endl;

    auto img = py::array_t<unsigned char>(
        {inputImage.rows, inputImage.cols, inputImage.channels()},
        inputImage.data
    );

    std::cout << "converted cv::Mat to numpy array" << std::endl;

    // Import the Python script 'qrcodereader' which contains 'detect_qr'
    // Import the sys module to manipulate sys.path
    py::module_ sys = py::module_::import("sys");

    // Add the parent directory to the sys.path
    sys.attr("path").attr("append")("../");

    py::module_ script = py::module_::import("qrcodereader");

    std::cout << "imported qrcodereader" << std::endl;

    // Call the Python 'detect_qr' function
    py::object result = script.attr("detect_qr")(img);

}

int main() {
    std::cout << "OpenCV version: " << CV_VERSION << std::endl;
    cv::Mat image = cv::imread("../data/v.12 lower camera crop.jpg");
    if (image.empty()) {
        std::cerr << "Error loading image" << std::endl;
        return -1;
    }
    std::cout << "Image size: " << image.size() << std::endl;

    // Process image with Python function
    processImageWithPython(image);

    return 0;
}
